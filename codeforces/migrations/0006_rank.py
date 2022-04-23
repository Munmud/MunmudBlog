# Generated by Django 3.2.13 on 2022-04-22 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codeforces', '0005_auto_20220423_0500'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(max_length=250)),
                ('globalRank', models.IntegerField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('countryRank', models.IntegerField(blank=True, null=True)),
                ('organization', models.CharField(blank=True, max_length=250, null=True)),
                ('organizationRank', models.IntegerField(blank=True, null=True)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codeforces.contest')),
            ],
            options={
                'ordering': ['-contest', 'globalRank'],
            },
        ),
    ]