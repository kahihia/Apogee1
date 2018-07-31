# Generated by Django 2.0.1 on 2018-07-31 20:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parties', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=30)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parties.Party')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifs_list', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
