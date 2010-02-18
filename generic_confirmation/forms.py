import random
from django import forms
from django.db import models
from generic_confirmation.models import DeferredAction
from generic_confirmation.main import LONG
from generic_confirmation import signals



class DeferredFormMixIn(object):
    """
    This is a MixIn class, so that you can also build deferred forms
    from already existing modified ModelForm classes. 
    If you build your form from scratch you want to use the ``DeferredForm``
    class.
     
    """
    
    token_format = LONG
    
    def _gen_token(self, format=None, step=0):
        """
        generates a unique (in terms of DeferredAction objects) token based
        on the format tuple in the form of (alphabet, length).
        """
        if format is None:
            format = self.token_format
        chars, length = format
        token = u''.join([random.choice(chars) for i in range(length)])
        try:
            DeferredAction.objects.get(token=token)
        except DeferredAction.DoesNotExist:
            return token
        if step > 9:
            raise Exception("10 attempts to generate a unique token failed.")
        return self._gen_token(format=format, step=step+1)

    def save(self, user=None, **kwargs):
        """
        replaces the ModelForm save method with our own to defer the action
        by storing the data in the db.
        Returns a unique token which is needed to confirm the action and
        resume it.
        """
        if not self.is_valid():
            raise Exception("only call save() on a form after calling is_valid().")

        form_class_name = u"%s.%s" % (self.__class__.__module__, 
                                      self.__class__.__name__)

        # we save the uncleaned data here, because form.full_clean() will 
        # alter the data in cleaned_data and a second run with cleaned_data as 
        # form input will fail for foreignkeys and manytomany fields. 
        # additionally, storing the original input is a bit safer, because 
        # this is only data which was transfered over http, so we won't 
        # get any pickle errors here
        data = {'form_class':form_class_name, 'form_input':self.data, 
                'token':self._gen_token(),}
        valid_until = kwargs.pop('valid_until', None)
        if valid_until is not None:
            data.update({'valid_until': valid_until})
        defer = DeferredAction.objects.create(**data)

        if self.instance is not None:
            # this extra step makes sure that ModelForms for editing and for
            # creating objects both work.
            defer.instance_object = self.instance
            defer.save()

        # inform anyone else that confirmation is requested
        signals.confirmation_required.send(sender=self._meta.model, 
                                        instance=defer, user=user)
        
        if hasattr(self, 'send_notification') and callable(self.send_notification):
            self.send_notification(user, instance=defer)
            
        return defer.token
        
    def save_original(self, *args, **kwargs):
        """
        triggr the original ModelForm save
        """
        return forms.ModelForm.save(self, *args, **kwargs)


class DeferredForm(DeferredFormMixIn, forms.ModelForm):
    """
    Inherit from this form to get a ModelForm which will
    automatically defer it's save method until the action
    is confirmed.
    """

            
class ConfirmationForm(forms.Form):
    """
    Form to use in views to confirm an action with a token.
    Makes sure the token exists and on calling ``save()``
    will resume the defered action.
    
    """
    token = forms.CharField(required=True)
    
    def clean_token(self):
        try:
            obj = DeferredAction.objects.get(token=self.cleaned_data['token'])
            return self.cleaned_data['token']
        except DeferredAction.DoesNotExist:
            raise forms.ValidationError(u"wrong token") #FIXME: i18n
        
    def save(self):
        return DeferredAction.objects.confirm(token=self.cleaned_data['token'])
    
    