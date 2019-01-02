# Generated by Django 2.0.1 on 2018-09-14 21:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import parties.models
import parties.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140, validators=[parties.validators.validate_title, parties.validators.validate_profanity])),
                ('description', models.CharField(max_length=280, validators=[parties.validators.validate_profanity])),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('party_time', models.DateTimeField()),
                ('minimum_bid', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('interaction_pts', models.IntegerField(default=0)),
                ('time_pts', models.DecimalField(decimal_places=4, default=0, max_digits=10)),
                ('popularity', models.DecimalField(db_index=True, decimal_places=4, default=0, max_digits=10)),
                ('is_flagged', models.BooleanField(default=False)),
                ('num_possible_winners', models.PositiveSmallIntegerField(default=1)),
                ('max_entrants', models.PositiveSmallIntegerField(blank=True, choices=[(None, 'Unlimited'), (3, 3), (10, 10), (25, 25), (50, 50), (100, 100), (500, 500), (1000, 1000)], null=True)),
                ('is_open', models.BooleanField(default=True)),
                ('thumbnail', models.ImageField(blank=True, max_length=255, null=True, upload_to=parties.models.path_and_rename)),
                ('task_id', models.CharField(blank=True, editable=False, max_length=50)),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('event_type', models.IntegerField(choices=[(1, 'Lottery'), (2, 'Bid'), (3, 'Buy')], default=1)),
                ('joined', models.ManyToManyField(blank=True, related_name='joined_by', to=settings.AUTH_USER_MODEL)),
                ('report_list', models.ManyToManyField(blank=True, related_name='reported_by', to=settings.AUTH_USER_MODEL)),
                ('starred', models.ManyToManyField(blank=True, related_name='starred_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('winners', models.ManyToManyField(blank=True, related_name='won_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-time_created'],
            },
        ),
    ]
