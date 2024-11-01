from django.test import TestCase
from post_manager.ingestor import PostIngestor
from post_manager.models import Post

class PostIngestorTest(TestCase):

    def test_ingest_post(self):
        post_data = {
            'post': {'id': '456', 'name': 'Test Post', 'body': 'Test content'},
            'community': {'id': 1, 'name': 'Community Name'},
            'creator': {'id': 2, 'name': 'Creator Name'},
            'counts': {'comments': 5, 'score': 10}
        }

        ingestor = PostIngestor()
        ingestor.ingest_post(post_data)

        # Verify that the post has been saved correctly
        post = Post.objects.get(post_id='456')
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.community, 'Community Name')
        self.assertEqual(post.counts_comments, 5)
