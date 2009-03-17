from django.conf.urls.defaults import *

urlpatterns = patterns('generic_confirmation.views',
    url(r'^$', 'confirm_by_form', {}, name="generic_confirmation_by_form"),
    url(r'^(?P<token>\w+)$', 'confirm_by_get', {}, name="generic_confirmation_by_get"),
)
