# Generated by Django 3.2.13 on 2022-04-23 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeforces', '0006_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='handle',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]
