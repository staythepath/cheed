from post_manager.models import Post
from django.core.exceptions import ObjectDoesNotExist

def get_all_posts():
    """
    Fetches all posts from the database.

    Returns:
        QuerySet: A queryset of all post objects.
    """
    return Post.objects.all()

def get_post_by_id(post_id):
    """
    Fetch a specific post by post_id.

    Args:
        post_id (str): The ID of the post to fetch.

    Returns:
        Post: The post object, or None if not found.
    """
    try:
        return Post.objects.get(post_id=post_id)
    except ObjectDoesNotExist:
        return None

def get_posts_by_community(community_name):
    """
    Fetches all posts belonging to a given community.

    Args:
        community_name (str): The name of the community.

    Returns:
        QuerySet: A queryset of post objects filtered by community.
    """
    return Post.objects.filter(community=community_name)

def get_posts_above_score(min_score):
    """
    Fetches all posts that have a score greater than or equal to min_score.

    Args:
        min_score (int): Minimum score to filter posts.

    Returns:
        QuerySet: A queryset of post objects filtered by score.
    """
    return Post.objects.filter(score__gte=min_score)
