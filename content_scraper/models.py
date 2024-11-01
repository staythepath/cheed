from django.db import models
from post_manager.models import Post


# This model represents any scraped data related to the post (e.g., metadata from a linked article).
class ScrapedData(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)  # Link to the corresponding Post instance
    article_title = models.CharField(max_length=255, default="No title available")  # Title of the linked article
    article_authors = models.JSONField(default=list)  # List of authors of the article
    publication_date = models.CharField(max_length=255, default="No date available", null=True, blank=True)  # Date of publication, optional
    article_content = models.TextField(default="No content available")  # Full content of the scraped article
    top_image = models.URLField(max_length=2048, default="No image available", null=True, blank=True)  # URL of the top image in the article
    article_keywords = models.JSONField(default=list)  # Keywords associated with the article
    article_summary = models.TextField(default="No summary available", null=True, blank=True)  # Summary of the article

    def __str__(self):
        return f"ScrapedData for: {self.post.title}"

