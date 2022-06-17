from django.urls import path
from generic_confirmation import views

urlpatterns = [
    path('', views.confirm_by_form, name="generic_confirmation_by_form"),
    path('<str:token>', views.confirm_by_get, name="generic_confirmation_by_get"),
]
