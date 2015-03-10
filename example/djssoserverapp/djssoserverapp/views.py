from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from djssoserver.models import SSO


def home(request):
    return render_to_response("index.html",
                              {"ssoapi": SSO.objects},
                              context_instance=RequestContext(request))
