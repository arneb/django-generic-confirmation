# -*- coding: utf-8 -*-
"""Unit testing for django-generic-confirmation."""

from django import forms
from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.db import models
from django.core import mail
from django.conf import settings
from generic_confirmation.fields import PickledObjectField
from generic_confirmation.forms import DeferredForm, ConfirmationForm
from generic_confirmation.models import DeferredAction
from generic_confirmation.main import LONG, SHORT, SHORT_UPPER
from generic_confirmation import signals


class EmailChangeForm(DeferredForm):
        class Meta:
            model = User
            fields = ('email',)

class GroupNameChangeForm(DeferredForm):
    token_format = SHORT
    class Meta:
        model = Group
        fields = ('name',)
        
class UserCreateForm(DeferredForm):
    token_format = SHORT_UPPER
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class GroupChangeForm(DeferredForm):
    class Meta:
        model = User
        fields = ('groups',)
        

class EmailChangeWithMailForm(DeferredForm):
    def send_notification(self, user=None, instance=None):
        mail.send_mail("please confirm your new address", "Please confirm %s" % instance.token,
            settings.DEFAULT_FROM_EMAIL, [self.cleaned_data['email'],])
            
    class Meta:
        model = User
        fields = ('email',)

class DeferFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user1', 'user1@example.com', '123456')
        
    def testEmailChange(self):
        form = EmailChangeForm({'email': 'xxx@example.com'}, instance=self.user)
        self.assertTrue(form.is_valid())
        
        defered = form.save()
        self.assertEquals(len(defered), LONG[1])
        # refetch user-object from db before checking the email,
        # because django objects don't reflect db changes done
        # elsewhere
        user_obj = User.objects.get(username=self.user.username)
        self.assertEquals(user_obj.email, 'user1@example.com')
        
        # ========================
        # in practice this is the boundary, where code excution will be defered.
        # ========================

        obj = DeferredAction.objects.confirm(token=defered)    
        #x = obj.resume_form_save()
        
        # refetch user-object from db before checking the email,
        # because django objects don't reflect db changes done
        # elsewhere
        user_obj = User.objects.get(username=self.user.username)
        self.assertEquals(user_obj.email, 'xxx@example.com')
        
        
    def testUserCreation(self):
        form = UserCreateForm({'username': 'user2', 'email': 'user2@example.com', 'password': '123456'})    
        self.assertTrue(form.is_valid())
        defered = form.save()
        self.assertEquals(len(defered), SHORT_UPPER[1])
        # at this point the object must not exist.
        self.assertRaises(User.DoesNotExist, User.objects.get, username='user2')
        
        # ========================
        # in practice this is the boundary, where code excution will be defered.
        # ========================

        obj = DeferredAction.objects.confirm(token=defered)    
        #x = obj.resume_form_save()
        
        # refetch user-object from db before checking the email,
        # because django objects don't reflect db changes done
        # elsewhere
        user_obj = User.objects.get(username='user2')
        self.assertEquals(user_obj.email, 'user2@example.com')
        
        
    def testConfirmViaForm(self):
        form = EmailChangeForm({'email': 'xxx@example.com'}, instance=self.user)
        self.assertTrue(form.is_valid())
        
        defered = form.save()
        self.assertEquals(len(defered), LONG[1])

        # refetch user-object from db before checking the email,
        # because django objects don't reflect db changes done
        # elsewhere
        user_obj = User.objects.get(username=self.user.username)
        self.assertEquals(user_obj.email, 'user1@example.com')
        
        # ========================
        # in practice this is the boundary, where code excution will be defered.
        # ========================
        
        confirm_form = ConfirmationForm({'token': defered})
        self.assertTrue(confirm_form.is_valid())
        obj = confirm_form.save()        
        self.assertNotEqual(obj, False)
        
        # refetch user-object from db before checking the email,
        # because django objects don't reflect db changes done
        # elsewhere
        user_obj = User.objects.get(username=self.user.username)
        self.assertEquals(user_obj.email, 'xxx@example.com')        
        
        
class ManyToManyTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user3', 'user3@example.com', '123456')
        self.group1 = Group.objects.create(name='first_test_group')
        self.group2 = Group.objects.create(name='second_test_group')
        
    def testGroupChange(self):
        form = GroupChangeForm({'groups': [self.group1.pk, self.group2.pk]}, instance=self.user)
        self.assertTrue(form.is_valid())
        
        defered = form.save()
        self.assertEquals(len(defered), LONG[1])

        # refetch user-object from db before checking the email,
        # because django objects don't reflect db changes done
        # elsewhere
        user_obj = User.objects.get(username=self.user.username)
        self.assertEquals(list(user_obj.groups.all()), [])
        
        # ========================
        # in practice this is the boundary, where code excution will be defered.
        # ========================
        
        obj = DeferredAction.objects.confirm(token=defered)    
        #x = obj.resume_form_save()
        
        # refetch user-object from db before checking the email,
        # because django objects don't reflect db changes done
        # elsewhere
        user_obj = User.objects.get(username=self.user.username)
        self.assertEquals(list(user_obj.groups.all()), [self.group1, self.group2])
        

class SignalTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user4', 'user4@example.com', '123456')
        self.group = Group.objects.create(name='test_group_one')
        
    def testCatchAllListener(self):
        
        def dummy_listener(sender, instance, testcase=self, **kwargs):
            """ a signal receiver which does some tests """
            testcase.assertEquals(instance.__class__, DeferredAction)
            
        signals.confirmation_required.connect(dummy_listener)
        
        # just triggr a confirmation request by changing the email
        form = EmailChangeForm({'email': 'xxx@example.com'}, instance=self.user)
        self.assertTrue(form.is_valid())
        defered = form.save()
        self.assertEquals(len(defered), LONG[1])
        
        form = GroupNameChangeForm({'name': 'new_name'}, instance=self.group)
        self.assertTrue(form.is_valid())
        defered = form.save()
        self.assertEquals(len(defered), SHORT[1])

    def testClassOnlyListener(self):
        
        def dummy_listener(sender, instance, testcase=self, **kwargs):
            """ a signal receiver which does some tests """
            testcase.assertEquals(instance.__class__, DeferredAction)
            testcase.assertEquals(sender, User)
            
        signals.confirmation_required.connect(dummy_listener, sender=User)
        
        # just triggr a confirmation request by changing the email
        form = EmailChangeForm({'email': 'xxx@example.com'}, instance=self.user)
        self.assertTrue(form.is_valid())
        defered = form.save()
        self.assertEquals(len(defered), LONG[1])
        
        form = GroupNameChangeForm({'name': 'new_name'}, instance=self.group)
        self.assertTrue(form.is_valid())
        defered = form.save()
        self.assertEquals(len(defered), SHORT[1])


    def testUserPassing(self):
        def dummy_listener(sender, instance, user, testcase=self, **kwargs):
            """ a signal receiver which does some tests """
            testcase.assertEquals(instance.__class__, DeferredAction)
            testcase.assertEquals(user, self.user)
            
        signals.confirmation_required.connect(dummy_listener)
        
        # just triggr a confirmation request by changing the email
        form = EmailChangeForm({'email': 'xxx@example.com'}, instance=self.user)
        self.assertTrue(form.is_valid())
        defered = form.save(self.user)
        self.assertEquals(len(defered), LONG[1])
    
    def testNoUser(self):
        def dummy_listener(sender, instance, user, testcase=self, **kwargs):
            """ a signal receiver which does some tests """
            testcase.assertEquals(instance.__class__, DeferredAction)
            testcase.assertEquals(user, None)
            
        signals.confirmation_required.connect(dummy_listener)
            
        form = GroupNameChangeForm({'name': 'new_name'}, instance=self.group)
        self.assertTrue(form.is_valid())
        defered = form.save()
        self.assertEquals(len(defered), SHORT[1])    

class NotificationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user4', 'user4@example.com', '123456')
        
    def testMailNotification(self):
        form = EmailChangeWithMailForm({'email': 'new@example.com'}, instance=self.user)
        self.assertTrue(form.is_valid())
        self.assertEquals(len(mail.outbox), 0)
        token = form.save(self.user)
        self.assertEquals(len(mail.outbox), 1)
        # make sure the right token is in the body of the message
        self.assertTrue(token in mail.outbox[0].body) 
        
        
        
# taken from djangosnippets.org/snippets/513 by obeattie        
        
class TestingModel(models.Model):
	pickle_field = PickledObjectField()

class TestCustomDataType(str):
	pass

class PickledObjectFieldTests(TestCase):
	def setUp(self):
		self.testing_data = (
			{1:1, 2:4, 3:6, 4:8, 5:10},
			'Hello World',
			(1, 2, 3, 4, 5),
			[1, 2, 3, 4, 5],
			TestCustomDataType('Hello World'),
		)
		return super(PickledObjectFieldTests, self).setUp()
	
	def testDataIntegriry(self):
		"""Tests that data remains the same when saved to and fetched from the database."""
		for value in self.testing_data:
			model_test = TestingModel(pickle_field=value)
			model_test.save()
			model_test = TestingModel.objects.get(id__exact=model_test.id)
			self.assertEquals(value, model_test.pickle_field)
			model_test.delete()
	
	def testLookups(self):
		"""Tests that lookups can be performed on data once stored in the database."""
		for value in self.testing_data:
			model_test = TestingModel(pickle_field=value)
			model_test.save()
			self.assertEquals(value, TestingModel.objects.get(pickle_field__exact=value).pickle_field)
			model_test.delete()
