from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()  # for django 1.6

urlpatterns = patterns('',
    url(r'^$', 'djssoserverapp.views.home', name='home'),
    url(r'^sso/', include('djssoserver.urls')),
    # url('^', include('django.contrib.auth.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

    url(r'^admin/', include(admin.site.urls)),
)
