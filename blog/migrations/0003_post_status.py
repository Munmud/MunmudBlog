# Generated by Django 3.2.13 on 2022-04-17 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_emailsubscriber'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approaved', 'Approaved')], default='pending', max_length=250),
        ),
    ]
