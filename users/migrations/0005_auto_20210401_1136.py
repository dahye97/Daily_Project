# Generated by Django 3.1.7 on 2021-04-01 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210401_1122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={},
        ),
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_active',
        ),
    ]