# Generated by Django 2.0.1 on 2018-10-17 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20181003_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='twitch_OAuth_token',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='twitch_id',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='twitch_refresh_token',
            field=models.CharField(default='', max_length=100),
        ),
    ]
