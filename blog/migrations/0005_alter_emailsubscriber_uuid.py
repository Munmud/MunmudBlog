# Generated by Django 3.2.13 on 2022-04-22 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailsubscriber',
            name='uuid',
            field=models.CharField(max_length=250),
        ),
    ]
