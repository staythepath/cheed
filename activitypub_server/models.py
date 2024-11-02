# activitypub_server/models.py

from django.db import models
from datetime import datetime

class Actor(models.Model):
    actor_id = models.URLField(unique=True)
    name = models.CharField(max_length=255)
    inbox = models.URLField()
    public_key = models.TextField()

class Follower(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    follower_id = models.URLField()

class Activity(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    published = models.DateTimeField(default=datetime.utcnow)
    content = models.TextField()
