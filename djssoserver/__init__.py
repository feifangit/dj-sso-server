from django.conf import settings
default_app_config = 'djssoserver.apps.SSOConfig'
MAGIC_ID = "sso19841108"  # used to detect app's position in an url tree


def _load_setting(n, default):
    return getattr(settings, n) if hasattr(settings, n) else default

SSO_SERVER_USER_MODEL_TO_DICT_CLS = _load_setting("SSO_SERVER_USER_MODEL_TO_DICT_CLS", "djssoserver.utility.DjangoJSONEncoder")