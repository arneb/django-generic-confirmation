from django.template import Library
from generic_confirmation.models import DeferredAction

register = Library()

@register.simple_tag
def pending_confirmations(instance):
    """
    {% load generic_confirmation_tags %}
    Pending: {% pending_confirmations object %}
    """
    return DeferredAction.objects.pending_for(instance)
