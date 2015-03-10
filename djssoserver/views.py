import urlparse
import json
from functools import partial

from django.http import HttpResponse
from djapiauth.auth import api_auth
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.forms import AuthenticationForm
try:
    from django.contrib.sites.shortcuts import get_current_site
except:
    from django.contrib.sites.models import get_current_site
from django.contrib.auth.models import AnonymousUser

try:
    from django.http import JsonResponse
except ImportError:
    from .utility import JsonResponse

from sso import gen_auth_token, RequestToken, SSO_REQUEST_TOKEN_TTL
from .models import SSO
from utility import jsonify, append_tokens

JsonResponse403 = partial(JsonResponse, status=403)


@api_auth
@jsonify
def api_requesttoken(request):
    return {"request_token": RequestToken.generate()}


@api_auth
def api_authtoken(request):
    _request_token = request.GET.get("request_token")
    _auth_token = request.GET.get("auth_token")

    try:
        if not (_request_token and _auth_token):
            raise Exception("parameter missing")

        # make sure the request token is generated from this server
        userinfo = RequestToken.load_info(_request_token)
        if not userinfo:
            raise Exception("request token not found")
        userobj = json.loads(userinfo)
        if not userobj:
            raise Exception("request token error")
        RequestToken.revoke(_request_token)  # delete used request token

        # verify auth token
        if _auth_token != gen_auth_token(_request_token):
            raise Exception("auth token error")

        return JsonResponse({"user": userobj})
    except Exception as e:
        # return JsonResponse({"error": str(e)}, status=403)
        return JsonResponse403({"error": str(e)})


def login(request):
    redirect_to = request.POST.get("next", request.GET.get("next"))
    request_token = request.POST.get("request_token", request.GET.get("request_token"))
    api_key = request.POST.get("api_key", request.GET.get("api_key"))

    if not (redirect_to and request_token and api_key):
        return HttpResponse("parameter missing", status=403)

    rt = RequestToken.load_info(request_token)
    if not rt:
        return HttpResponse("invalid request token", status=403)

    # verify remote host
    url_info_to = urlparse.urlparse(redirect_to)
    try:
        SSO.objects.get(host=url_info_to.netloc, credential__apikey=api_key)
    except SSO.DoesNotExist:
        return HttpResponse("request deny for remote host", status=403)

    okresp = HttpResponseRedirect(append_tokens(redirect_to,
                                                request_token=request_token,
                                                auth_token=gen_auth_token(request_token)))

    ssouser = request.user  # current logged-in user by default

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            RequestToken.bind_info(request_token, form.get_user())
            return okresp
    else:  # GET
        form = AuthenticationForm(request)
        bContinueWithCurrentAccount = request.GET.get("cwca", None)

        if bContinueWithCurrentAccount == "yes":  # confirmed: continue with logged in account
            RequestToken.bind_info(request_token, request.user)
            return okresp
        elif bContinueWithCurrentAccount == "no":  # confirmed: login with another account
            ssouser = AnonymousUser()
        else:  # ask to login with current account or switch to a new account, or login form if not logged-in
            pass

    current_site = get_current_site(request)

    context = {
        'form': form,
        "next": redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        'remote_app': url_info_to.netloc,
        "sso_timeout": SSO_REQUEST_TOKEN_TTL,
        "ssouser": ssouser,
        "req": request  # name req will not confilict with request if django.core.context_processors.request enabled

    }

    return TemplateResponse(request, 'djssoserver/ssologin.html', context)
