import base64
# based on djangosnippets.org/snippets/513 by obeattie
from django.db import models
from django.utils.encoding import smart_bytes

try:
    import cPickle as pickle
except ImportError:
    import pickle


class PickledObject(bytes):
    """
    A subclass of bytes (str in python2) so it can be told whether a string is
    a pickled object or not (if the object is an instance of this class then
    it must [well, should] be a pickled one).

    """
    pass


class PickledObjectField(models.Field):

    def from_db_value(self, value, expression, connection, context=None):
        if isinstance(value, PickledObject):
            # If the value is a definite pickle; and an error is raised in de-pickling
            # it should be allowed to propogate.
            return pickle.loads(smart_bytes(base64.b64decode(value)))
        else:
            try:
                return pickle.loads(smart_bytes(base64.b64decode(value)))
            except:
                # If an error was raised, just return the plain value
                return value

    def get_prep_value(self, value):
        if value is not None and not isinstance(value, PickledObject):
            value = base64.b64encode(PickledObject(pickle.dumps(value))).decode()
        return value

    def get_internal_type(self):
        return 'TextField'

    def get_lookup(self, lookup_name):
        if lookup_name in ('exact', 'in'):
            return super(PickledObjectField, self).get_lookup(lookup_name)
        else:
            raise TypeError('Lookup type %s is not supported.' % lookup_name)
