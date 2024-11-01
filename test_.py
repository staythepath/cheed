import os
import django
from post_manager.models import Post
from pprint import pprint

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_main.settings')  # Adjust the settings path accordingly
django.setup()

# Fetch all posts from the Post model
posts = Post.objects.all()
for post in posts:
    # Create a dictionary of the post's main attributes
    post_dict = {
        'Post ID': post.post_id,
        'Title': post.title,
        'Content': post.content,
        'Community': post.community,
        'Creator Name': post.creator_name,
        'URL': post.url,
        'Score': post.score,
        'Comments Count': post.counts_comments,
        'Community Description': post.community_description,
        'Embed Title': post.embed_title,
        'Embed Description': post.embed_description,
    }

    # Pretty print the dictionary for easier viewing
    pprint(post_dict)
    print("\n" + "="*50 + "\n")
