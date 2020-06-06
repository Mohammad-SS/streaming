# Generated by Django 2.2.12 on 2020-06-01 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0013_auto_20200601_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conductoritem',
            name='endTime',
        ),
        migrations.AddField(
            model_name='conductoritem',
            name='time',
            field=models.IntegerField(default=2, verbose_name='Program Duration'),
            preserve_default=False,
        ),
    ]
