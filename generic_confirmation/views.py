from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from generic_confirmation.forms import ConfirmationForm


def confirm_by_form(request, template_name='confirm.html',
                    success_template_name='confirmed.html',
                    success_url=None, success_message=None,
                    form_class=ConfirmationForm):
    """
    If ``success_url`` is not None a redirect to ``success_url`` will
    be issued, once the entered confirmation code was confirmed successfully.
    Optionally, of ``success_message`` is not None, it will be set via
    Django's message system.

    If ``success_url`` is None the template ``success_template_name`` will
    be rendered once the confirmation is complete. The ``success_message``
    will then be added to the template context instead of the message_set.

    """
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            if success_url is None:
                return render(request, success_template_name, {'success_message': success_message})
            else:
                if success_message is not None and request.user.is_authenticated:
                    messages.add_message(request, messages.SUCCESS, success_message)
                return HttpResponseRedirect(success_url)
    else:
        form = form_class()
    return render(request, template_name, {'form': form})


def confirm_by_get(request, token, template_name='confirm.html',
                   success_template_name="confirmed.html",
                   success_url=None, success_message=None,
                   form_class=ConfirmationForm):
    form = form_class({'token': token})
    if form.is_valid():
        form.save()
        if success_url is None:
            return render(request, success_template_name, {'success_message': success_message})
        else:
            if success_message is not None and request.user.is_authenticated:
                messages.add_message(request, messages.SUCCESS, success_message)
            return HttpResponseRedirect(success_url)
    else:
        return render(request, template_name, {})
