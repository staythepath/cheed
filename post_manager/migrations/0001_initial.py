# Generated by Django 5.1.2 on 2024-11-01 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(db_index=True, max_length=255, unique=True)),
                ('community_id', models.IntegerField(blank=True, null=True)),
                ('creator_id', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(default='No title available', max_length=255)),
                ('content', models.TextField(default='No content available')),
                ('score', models.IntegerField(default=0)),
                ('community', models.CharField(default='Unknown', max_length=255)),
                ('creator_name', models.CharField(default='Unknown', max_length=255)),
                ('creator_avatar', models.URLField(blank=True, default='No avatar available', null=True)),
                ('community_description', models.TextField(blank=True, default='No description available', null=True)),
                ('embed_title', models.CharField(blank=True, default='No embed title available', max_length=255, null=True)),
                ('embed_description', models.TextField(blank=True, default='No embed description available', null=True)),
                ('counts_comments', models.IntegerField(default=0)),
                ('counts_score', models.IntegerField(default=0)),
                ('url', models.URLField(blank=True, default='', max_length=2048, null=True)),
            ],
        ),
    ]