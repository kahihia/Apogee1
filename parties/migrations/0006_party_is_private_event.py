# Generated by Django 2.0.1 on 2018-10-18 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0005_party_is_twitch_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='is_private_event',
            field=models.BooleanField(default=False),
        ),
    ]
