# Generated by Django 5.1.2 on 2024-11-02 02:12

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor_id', models.URLField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('inbox', models.URLField()),
                ('public_key', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_type', models.CharField(max_length=100)),
                ('published', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('content', models.TextField()),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activitypub_server.actor')),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower_id', models.URLField()),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activitypub_server.actor')),
            ],
        ),
    ]
