from django.urls import path, re_path
from generic_confirmation import views

urlpatterns = [
    path('', views.confirm_by_form, {}, name="generic_confirmation_by_form"),
    re_path(r'^(?P<token>\w+)$', views.confirm_by_get, {}, name="generic_confirmation_by_get"),
]
