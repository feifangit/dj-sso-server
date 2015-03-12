import hmac
import hashlib
import json
import uuid

from django.forms.models import model_to_dict
from django.conf import settings
from django.core.cache import cache
from . import SSO_SERVER_USER_TO_JSON_FUNC
from django.utils.module_loading import import_by_path


SSO_SEC_KEY = settings.SECRET_KEY
SSO_REQUEST_TOKEN_TTL = 240


def gen_auth_token(request_token):
    return hmac.new(str(SSO_SEC_KEY), request_token, digestmod=hashlib.sha256).hexdigest()


class RequestToken(object):
    @staticmethod
    def bind_info(request_token, user):
        # bind request token with user object
        cachedreqtoken = RequestToken.gen_cached_key(request_token)
        cache.set(cachedreqtoken, import_by_path(SSO_SERVER_USER_TO_JSON_FUNC)(user))

    @staticmethod
    def load_info(_request_token):
        return cache.get(RequestToken.gen_cached_key(_request_token))

    @staticmethod
    def generate():
        rt = uuid.uuid4().hex[:8]
        cache.set(RequestToken.gen_cached_key(rt), "{}", SSO_REQUEST_TOKEN_TTL)
        return rt

    @staticmethod
    def gen_cached_key(_request_token):
        return "sso::%s" % _request_token

    @staticmethod
    def revoke(_request_token):
        cache.delete(RequestToken.gen_cached_key(_request_token))
