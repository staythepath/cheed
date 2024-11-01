from django.test import TestCase
from unittest.mock import patch
from activity_ingestion.lemmy_client import LemmyApiClient

class LemmyApiClientTest(TestCase):

    @patch('activity_ingestion.lemmy_client.requests.get')
    def test_fetch_posts(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"posts": [{"post": {"id": "123"}}]}

        client = LemmyApiClient(base_url="https://dummy.instance")
        posts = client.fetch_posts(community_name="opensource")

        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]['post']['id'], "123")
