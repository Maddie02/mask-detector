# Generated by Django 3.1.3 on 2021-02-04 18:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210204_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistic',
            name='last_seen_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 4, 18, 2, 32, 957098, tzinfo=utc), null=True),
        ),
    ]