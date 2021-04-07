# Generated by Django 3.1.7 on 2021-04-06 02:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0003_auto_20210402_1326'),
        ('account', '0005_auto_20210406_1111'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='account',
            unique_together={('company_id', 'uid')},
        ),
    ]
