# Generated by Django 3.1.4 on 2021-02-11 05:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20210211_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 11, 5, 27, 52, 203336, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 11, 5, 27, 52, 203336, tzinfo=utc)),
        ),
        migrations.DeleteModel(
            name='Register',
        ),
    ]
