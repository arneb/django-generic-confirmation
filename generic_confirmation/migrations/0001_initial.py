from django.db import models, migrations
import generic_confirmation.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeferredAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=40)),
                ('valid_until', models.DateTimeField(null=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('form_class', models.CharField(max_length=255)),
                ('form_input', generic_confirmation.fields.PickledObjectField(editable=False)),
                ('form_prefix', models.CharField(max_length=255, null=True, blank=True)),
                ('object_pk', models.TextField(null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
