# Generated by Django 3.1.3 on 2021-02-04 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210204_1526'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statistic',
            old_name='employee_id',
            new_name='employee',
        ),
    ]