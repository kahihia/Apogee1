# Generated by Django 2.0.1 on 2018-05-22 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0026_merge_20180517_1653'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='party',
            name='num_curr_winners',
        ),
    ]