from django.db import models
from django.conf import settings
from django.utils.module_loading import import_by_path
from django.db.models import Q

from .utility import generalcache
from djapiauth.models import APIEntryPoint, APIKeys
from djapiauth.utility import traverse_urls
from . import MAGIC_ID


class SSO(models.Model):
    class Meta:
        verbose_name = "Single sign-on"

    credential = models.ForeignKey(APIKeys)
    host = models.CharField(max_length=100, unique=True)
    note = models.CharField(max_length=80, null=True, blank=True)

    @staticmethod
    @generalcache(cachekey="ssoapi")
    def sso_api_list():
        """
        return sso related API
        """
        ssourls = []

        def collect(u, prefixre, prefixname):
            _prefixname = prefixname + [u._regex, ]
            urldisplayname = " ".join(_prefixname)

            if hasattr(u.urlconf_module, "_MODULE_MAGIC_ID_") \
                    and getattr(u.urlconf_module, "_MODULE_MAGIC_ID_") == MAGIC_ID:  # find aap name sso
                ssourls.append(urldisplayname)

        rooturl = import_by_path(settings.ROOT_URLCONF + ".urlpatterns")
        # traverse url matching tree to find the url statement including sso app,
        # should be 1 element in the ssourls unless you assigned 1+ prefix url for sso app
        traverse_urls(rooturl, resolverFunc=collect)

        finalQ = Q()  # filter to get full url of all registered sso api
        for prefix in ssourls:
            finalQ |= Q(name__startswith=prefix)
        return APIEntryPoint.objects.filter(finalQ)

    def save(self, *args, **kwargs):
        if not self.id:  # new creating
            c = APIKeys(note="for host: %s SSO login" % self.host)
            c.save()
            c.apis = SSO.sso_api_list()
            self.credential = c
        return super(SSO, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.host)
