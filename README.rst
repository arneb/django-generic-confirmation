===========================
django-generic-confirmation
===========================

Django-generic-confirmation makes it easy for developers to add forms to a
webapplication where the submitted data should only be used after an out-of-band
confirmation was done. For example if a user wants to change his email address,
generic-confirmation will make it really easy for the developer to add an
out-of-band confirmation process (sending an email with a random link to the 
user) before saving the new email address to the database.

The core of django-generic-confirmation is fully unit-tested and the app is in
use at a few real-world projects confirming email addresses and mobile phone
numbers. Feel free to read about the usage in `docs/usage.txt`.