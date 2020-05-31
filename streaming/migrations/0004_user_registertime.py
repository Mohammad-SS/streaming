# Generated by Django 2.2.12 on 2020-05-31 03:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0003_auto_20200530_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='registerTime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Register Date and Time'),
            preserve_default=False,
        ),
    ]
