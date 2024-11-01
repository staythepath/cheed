import logging
from post_manager.models import Post

logger = logging.getLogger(__name__)

class PostIngestor:
    def ingest_post(self, post_data):
        """
        Handles the ingestion of post data into the database.

        Args:
            post_data (dict): The post data fetched from Lemmy's API.
        """
        post_id = post_data['post']['id']

        # Using get_or_create to avoid redundant database hits
        try:
            new_post, created = Post.objects.get_or_create(
                post_id=post_id,
                defaults={
                    'community_id': post_data['community']['id'],
                    'creator_id': post_data['creator']['id'],
                    'title': post_data['post'].get('name', 'No title available'),
                    'content': post_data['post'].get('body', 'No content available'),
                    'score': post_data['counts'].get('score', 0),
                    'community': post_data['community'].get('name', 'Unknown'),
                    'creator_name': post_data['creator'].get('name', 'Unknown'),
                    'creator_avatar': post_data['creator'].get('avatar', 'None'),
                    'community_description': post_data['community'].get('description', 'No description available'),
                    'embed_title': post_data['post'].get('embed_title', 'No embed title available'),
                    'embed_description': post_data['post'].get('embed_description', 'No embed description available'),
                    'counts_comments': post_data['counts'].get('comments', 0),
                    'counts_score': post_data['counts'].get('score', 0),
                    'url': post_data['post'].get('url', "No URL"),
                }
            )

            if created:
                logger.info(f"Successfully saved post with ID: {post_id}")
            else:
                logger.debug(f"Post with ID: {post_id} already exists in the database.")

        except Exception as e:
            logger.error(f"Failed to save post with ID: {post_id}. Error: {e}")

