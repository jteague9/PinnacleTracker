# Generated by Django 3.1.1 on 2020-10-10 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20201010_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchup',
            name='winner',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
