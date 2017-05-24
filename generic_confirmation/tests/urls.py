from django.conf.urls import url
from generic_confirmation import views

urlpatterns = [
    url(r'^by-form/$', views.confirm_by_form,
        {},
        name="generic_confirmation_by_form"),

    url(r'^by-form-with-message/$', views.confirm_by_form,
        {'success_message': "This is a success message"},
        name="generic_confirmation_by_form_with_message"),

    url(r'^by-form-with-url/$', views.confirm_by_form,
        {'success_url': "/success/"},
        name="generic_confirmation_by_form_with_url"),

    url(r'^by-form-with-url-and-message/$', views.confirm_by_form,
        {'success_url': "/success/",
         'success_message': "This is a success message"},
        name="generic_confirmation_by_form_with_url_and_message"),



    url(r'^by-get/(?P<token>\w+)$', views.confirm_by_get,
        {},
        name="generic_confirmation_by_get"),

    url(r'^by-get-with-message/(?P<token>\w+)$', views.confirm_by_get,
        {'success_message': "This is a success message"},
        name="generic_confirmation_by_get_with_message"),

    url(r'^by-get-with-url/(?P<token>\w+)$', views.confirm_by_get,
        {'success_url': "/success/"},
        name="generic_confirmation_by_get_with_url"),

    url(r'^by-get-with-url-and-message/(?P<token>\w+)$', views.confirm_by_get,
        {'success_url': "/success/",
         'success_message': "This is a success message"},
        name="generic_confirmation_by_get_with_url_and_message"),
]