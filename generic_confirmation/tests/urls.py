from django.conf.urls.defaults import *

urlpatterns = patterns('generic_confirmation.views',
    url(r'^by-form/$', 'confirm_by_form', 
        {}, 
        name="generic_confirmation_by_form"),
        
    url(r'^by-form-with-message/$', 'confirm_by_form', 
        {'success_message': "This is a success message"}, 
        name="generic_confirmation_by_form_with_message"),
        
    url(r'^by-form-with-url/$', 'confirm_by_form', 
        {'success_url': "/success/"}, 
        name="generic_confirmation_by_form_with_url"),
        
    url(r'^by-form-with-url-and-message/$', 'confirm_by_form', 
        {'success_url': "/success/",
         'success_message': "This is a success message"}, 
        name="generic_confirmation_by_form_with_url_and_message"),
        
        
            
    url(r'^by-get/(?P<token>\w+)$', 'confirm_by_get', 
        {}, 
        name="generic_confirmation_by_get"),
    
    url(r'^by-get-with-message/(?P<token>\w+)$', 'confirm_by_get', 
        {'success_message': "This is a success message"}, 
        name="generic_confirmation_by_get_with_message"),
    
    url(r'^by-get-with-url/(?P<token>\w+)$', 'confirm_by_get', 
        {'success_url': "/success/"}, 
        name="generic_confirmation_by_get_with_url"),
        
    url(r'^by-get-with-url-and-message/(?P<token>\w+)$', 'confirm_by_get', 
        {'success_url': "/success/",
         'success_message': "This is a success message"}, 
        name="generic_confirmation_by_get_with_url_and_message"),
)
