# Generated by Django 3.1.7 on 2021-04-02 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20210402_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit_withdrawal',
            name='trading_time',
            field=models.DateTimeField(default=''),
        ),
    ]
