from django.urls import path

from generic_confirmation import views

urlpatterns = [
    path('by-form/', views.confirm_by_form, name="generic_confirmation_by_form"),

    path('by-form-with-message/', views.confirm_by_form, {'success_message': "This is a success message"}, name="generic_confirmation_by_form_with_message"),

    path('by-form-with-url/', views.confirm_by_form, {'success_url': "/success/"}, name="generic_confirmation_by_form_with_url"),

    path('by-form-with-url-and-message/', views.confirm_by_form,
         {
             'success_url': "/success/",
             'success_message': "This is a success message"
         },
         name="generic_confirmation_by_form_with_url_and_message"),

    path('by-get/<token:str>', views.confirm_by_get, name="generic_confirmation_by_get"),

    path('by-get-with-message/<token:str>', views.confirm_by_get, {'success_message': "This is a success message"}, name="generic_confirmation_by_get_with_message"),

    path('by-get-with-url/<token:str>', views.confirm_by_get, {'success_url': "/success/"}, name="generic_confirmation_by_get_with_url"),

    path('by-get-with-url-and-message/<token:str>', views.confirm_by_get,
         {
             'success_url': "/success/",
             'success_message': "This is a success message"
         },
         name="generic_confirmation_by_get_with_url_and_message"),
]
