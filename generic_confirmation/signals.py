from django.dispatch import Signal

# sender is the class which is edited, instance is the DeferedAction instance
# user is the user who edited the sender instance or None. user is only not
# None if passed to form form.save(user=request.user) method ...
# "instance", "user"
confirmation_required = Signal()

# sender is the class which is edited, instance is the DeferedAction instance
# "instance"
change_confirmed = Signal()
