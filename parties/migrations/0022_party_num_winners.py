# Generated by Django 2.0.1 on 2018-05-08 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0021_auto_20180419_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='num_winners',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]