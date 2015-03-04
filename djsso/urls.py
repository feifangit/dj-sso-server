from django.conf.urls import patterns, url
from . import views, MAGIC_ID

from djapiauth.utility import reg_api

_MODULE_MAGIC_ID_ = MAGIC_ID

urlpatterns = patterns('',
                       url(r'^login/$', views.login, name="sso_login"),
                       reg_api(r'^reqeusttoken/$', views.api_requesttoken, name="sso_requesttoken"),
                       reg_api(r'^authtoken/$', views.api_authtoken, name="sso_authtoken"))
