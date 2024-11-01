from django.db import models

# This model represents the primary post information fetched from ActivityPub.
class Post(models.Model):
    post_id = models.CharField(max_length=255, unique=True, db_index=True)  # Unique identifier for the post, indexed for performance
    community_id = models.IntegerField(null=True, blank=True)  # ID of the community where the post was made
    creator_id = models.IntegerField(null=True, blank=True)  # ID of the post creator
    title = models.CharField(max_length=255, default="No title available")  # Title of the post
    content = models.TextField(default="No content available")  # Content or body of the post
    score = models.IntegerField(default=0)  # Score or votes on the post
    community = models.CharField(max_length=255, default="Unknown")  # Community name where the post was made
    creator_name = models.CharField(max_length=255, default="Unknown")  # Name of the creator of the post
    creator_avatar = models.URLField(default="No avatar available", null=True, blank=True)  # URL to the creator's avatar
    community_description = models.TextField(default="No description available", null=True, blank=True)  # Description of the community
    embed_title = models.CharField(max_length=255, default="No embed title available", null=True, blank=True)  # Title of any embedded content
    embed_description = models.TextField(default="No embed description available", null=True, blank=True)  # Description of embedded content
    counts_comments = models.IntegerField(default=0)  # Number of comments on the post
    counts_score = models.IntegerField(default=0)  # Score or ranking of the post
    url = models.URLField(max_length=2048, default="", null=True, blank=True)  # URL of the post

    def __str__(self):
        return self.title