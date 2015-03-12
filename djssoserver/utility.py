import cPickle
import json
import datetime
import decimal
import urllib
import urlparse

from django.core.cache import cache
from django.http import HttpResponse
from django.forms.models import model_to_dict


def is_aware(value):
    """
    Determines if a given datetime.datetime is aware.

    The logic is described in Python's docs:
    http://docs.python.org/library/datetime.html#datetime.tzinfo
    """
    return value.tzinfo is not None and value.tzinfo.utcoffset(value) is not None


class DjangoJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time and decimal types.
    """

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, decimal.Decimal):
            return str(o)
        else:
            return super(DjangoJSONEncoder, self).default(o)


class JsonResponse(HttpResponse):
    """
    An HTTP response class that consumes data to be serialized to JSON.

    :param data: Data to be dumped into json. By default only ``dict`` objects
      are allowed to be passed due to a security flaw before EcmaScript 5. See
      the ``safe`` parameter for more information.
    :param encoder: Should be an json encoder class. Defaults to
      ``django.core.serializers.json.DjangoJSONEncoder``.
    :param safe: Controls if only ``dict`` objects may be serialized. Defaults
      to ``True``.
    """

    def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, **kwargs):
        if safe and not isinstance(data, dict):
            raise TypeError('In order to allow non-dict objects to be '
                            'serialized set the safe parameter to False')
        kwargs.setdefault('content_type', 'application/json')
        data = json.dumps(data, cls=encoder)
        super(JsonResponse, self).__init__(content=data, **kwargs)


def jsonify(function=None, options={}):
    def real_decorator(func):
        def wrapped(*args, **kwargs):
            resp = HttpResponse(json.dumps(func(*args, **kwargs), **options))
            resp["Content-Type"] = "application/json"
            return resp
        return wrapped
    return real_decorator if not function else real_decorator(function)


def generalcache(cachekey, ttl=1200):
    def real_decorator(func):
        def wrapper(*args, **kwargs):
            cachedvalue = cache.get(cachekey)
            if cachedvalue:
                return cPickle.loads(cachedvalue)
            else:
                result = func(*args, **kwargs)
                cache.set(cachekey, cPickle.dumps(result), ttl)
                return result
        return wrapper
    return real_decorator


def append_tokens(url, **kwargs):
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(kwargs)
    url_parts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(url_parts)


def default_user_to_json(user):
    return json.dumps(model_to_dict(user, exclude=["password", "user_permissions"]), 
        cls=DjangoJSONEncoder)
    
    

