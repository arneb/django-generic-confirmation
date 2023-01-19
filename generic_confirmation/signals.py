from django.dispatch import Signal

# sender is the class which is edited, instance is the DeferedAction instance
# user is the user who edited the sender instance or None. user is only not
# None if passed to form form.save(user=request.user) method ... 
# deprecated in Django4
#confirmation_required = Signal(providing_args=["instance", "user"])

confirmation_required = Signal()

# sender is the class which is edited, instance is the DeferedAction instance
# deprecated in Django4
#change_confirmed = Signal(providing_args=["instance"])

change_confirmed = Signal()
