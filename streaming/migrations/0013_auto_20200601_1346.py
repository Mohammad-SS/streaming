# Generated by Django 2.2.12 on 2020-06-01 09:16

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0012_remove_conductoritem_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conductoritem',
            name='time',
        ),
        migrations.AddField(
            model_name='conductoritem',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 1, 9, 16, 41, 694965, tzinfo=utc), verbose_name='End Air Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conductoritem',
            name='startTime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Start Air Time'),
            preserve_default=False,
        ),
    ]