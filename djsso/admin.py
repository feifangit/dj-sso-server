from django.contrib import admin
from django.forms import ModelForm
from .models import SSO


class SSOForm(ModelForm):
    class Meta:
        model = SSO
        exclude = ("credential",)


class SSOAdmin(admin.ModelAdmin):
    form = SSOForm
    list_display = ('host', 'note', 'get_apikey', 'get_seckey')

    def get_apikey(self, obj):
        return obj.credential.apikey

    def get_seckey(self, obj):
        return obj.credential.seckey

    get_apikey.short_description = 'API key'
    get_seckey.short_description = 'SEC key'


admin.site.register(SSO, SSOAdmin)
