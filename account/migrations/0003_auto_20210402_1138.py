# Generated by Django 3.1.7 on 2021-04-02 02:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_deposit_withdrawal'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='account',
            table='account',
        ),
        migrations.AlterModelTable(
            name='deposit_withdrawal',
            table='deposit_withdrawal',
        ),
    ]
