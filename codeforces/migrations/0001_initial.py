# Generated by Django 3.2.13 on 2022-04-22 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Handles',
            fields=[
                ('handle', models.CharField(max_length=250)),
                ('firstName', models.CharField(max_length=250)),
                ('lastName', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('isVerified', models.BooleanField(default=False)),
                ('uid', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
    ]
