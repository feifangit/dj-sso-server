from django.conf import settings
default_app_config = 'djssoserver.apps.SSOConfig'
MAGIC_ID = "sso19841108"  # used to detect app's position in an url tree


def _load_setting(n, default):
    return getattr(settings, n) if hasattr(settings, n) else default

SSO_SERVER_USER_TO_JSON_FUNC = _load_setting("SSO_SERVER_USER_TO_JSON_FUNC", "djssoserver.utility.default_user_to_json")


__version__ = '0.6'
VERSION = tuple(map(int, __version__.split('.')))