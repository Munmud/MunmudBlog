# Generated by Django 3.2.13 on 2022-04-22 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeforces', '0003_contest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
