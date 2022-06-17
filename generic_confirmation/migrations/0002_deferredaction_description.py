from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generic_confirmation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deferredaction',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
    ]
