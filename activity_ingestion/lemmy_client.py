import requests
import logging
from post_manager.ingestor import PostIngestor  # Importing the PostIngestor

logger = logging.getLogger(__name__)  # Configure logging for this module

class LemmyApiClient:
    def __init__(self, base_url, access_token=None):
        self.base_url = base_url
        self.access_token = access_token

    def fetch_posts(self, community_name=None):
        """
        Fetches posts from the Lemmy instance.

        Args:
            community_name (str): The community name to filter posts.

        Returns:
            list: List of posts fetched from the Lemmy API.
        """
        # Construct the API URL
        url = f"{self.base_url}/api/v3/post/list"

        # Optionally include a community name if provided
        params = {}
        if community_name:
            params['community_name'] = community_name

        # Make the request
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            posts = response.json().get("posts", [])
            
            # Log the number of posts fetched
            logger.info(f"Fetched {len(posts)} posts from {community_name or 'all communities'}")

            # Process posts by sending them to the post manager
            post_ingestor = PostIngestor()  # Instantiate the PostIngestor
            for post_data in posts:
                logger.info(f"Ingesting post with ID: {post_data['post']['id']}")
                post_ingestor.ingest_post(post_data)  # Send each post to be ingested

            return posts
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching posts: {e}")
            return []
