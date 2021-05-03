# Generated by Django 3.1.7 on 2021-04-29 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20210406_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('bank', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=6)),
            ],
            options={
                'db_table': 'bank',
            },
        ),
    ]