# activity_ingestion/management/commands/fetch_and_ingest.py

from django.core.management.base import BaseCommand
from activity_ingestion.lemmy_client import LemmyApiClient
from post_manager.ingestor import PostIngestor  # Importing the PostIngestor
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch posts from Lemmy and ingest them into the database'

    def handle(self, *args, **kwargs):
        # Set your Lemmy instance URL here
        lemmy_instance_url = "https://lemmy.ml"
        community_name = "opensource"  # Change as needed

        try:
            # Create a client instance
            client = LemmyApiClient(base_url=lemmy_instance_url)

            # Fetch posts from Lemmy
            posts = client.fetch_posts(community_name=community_name)

            if posts:
                logger.info(f"Successfully fetched {len(posts)} posts.")
                self.stdout.write(self.style.SUCCESS(f"Successfully fetched {len(posts)} posts."))

                # Instantiate PostIngestor
                post_ingestor = PostIngestor()

                # Iterate over posts and ingest them
                for post_data in posts:
                    post_ingestor.ingest_post(post_data)  # Send each post to be ingested
                    logger.info(f"Successfully ingested post with ID: {post_data['post']['id']}")
                    self.stdout.write(self.style.SUCCESS(f"Ingested post with ID: {post_data['post']['id']}"))

            else:
                logger.warning("No posts were fetched.")
                self.stdout.write(self.style.WARNING("No posts were fetched."))

        except Exception as e:
            logger.error(f"Error occurred during the ingestion: {e}")
            self.stdout.write(self.style.ERROR(f"Error occurred: {e}"))
