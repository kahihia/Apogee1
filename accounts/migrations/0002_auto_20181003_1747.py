# Generated by Django 2.0.1 on 2018-10-03 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email_auth_token',
            field=models.CharField(default='keyaut', max_length=6),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_authenticated',
            field=models.BooleanField(default=True),
        ),
    ]
