# Generated by Django 2.0.1 on 2018-10-17 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0004_remove_party_twitch_exclusive'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='is_twitch_event',
            field=models.BooleanField(default=False),
        ),
    ]