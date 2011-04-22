import base64
# based on djangosnippets.org/snippets/513 by obeattie
from django.db import models

try:
	import cPickle as pickle
except ImportError:
	import pickle

class PickledObject(str):
	"""A subclass of string so it can be told whether a string is
	   a pickled object or not (if the object is an instance of this class
	   then it must [well, should] be a pickled one)."""
	pass

class PickledObjectField(models.Field):
	__metaclass__ = models.SubfieldBase
	
	def to_python(self, value):
		if isinstance(value, PickledObject):
			# If the value is a definite pickle; and an error is raised in de-pickling
			# it should be allowed to propogate.
			return pickle.loads(str(base64.b64decode(value)))
		else:
			try:
				return pickle.loads(str(base64.b64decode(value)))
			except:
				# If an error was raised, just return the plain value
				return value
	
	def get_prep_value(self, value):
		if value is not None and not isinstance(value, PickledObject):
			value = base64.b64encode(PickledObject(pickle.dumps(value)))
		return value
	
	def get_internal_type(self): 
		return 'TextField'

	def get_prep_lookup(self, lookup_type, value):
		if lookup_type == 'exact':
			return self.get_prep_value(value)
		elif lookup_type == 'in':
			return [self.get_prep_value(v) for v in value]
		else:
			raise TypeError('Lookup type %s is not supported.' % lookup_type)
