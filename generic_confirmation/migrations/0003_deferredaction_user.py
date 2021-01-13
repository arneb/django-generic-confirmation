# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.admin.models
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('generic_confirmation', '0002_deferredaction_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='deferredaction',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
    ]
