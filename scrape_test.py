import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_main.settings')  # Replace with your actual settings module
django.setup()

from post_manager.models import Post
from content_scraper.models import ScrapedData
from pprint import pprint

def test_combined_post_and_scraped_data(post_id):
    try:
        # Fetch the post from Post table by its post_id
        post = Post.objects.get(post_id=post_id)
        pprint({
            'Post ID': post.post_id,
            'Community ID': post.community_id,
            'Creator ID': post.creator_id,
            'Title': post.title,
            'Content': post.content,
            'Score': post.score,
            'Community': post.community,
            'Creator Name': post.creator_name,
            'Creator Avatar': post.creator_avatar,
            'Embed Title': post.embed_title,
            'Embed Description': post.embed_description,
            'Comments Count': post.counts_comments,
            'Score Count': post.counts_score,
            'URL': post.url,
        })

        # Fetch the scraped data linked to the post, if available
        try:
            scraped_data = ScrapedData.objects.get(post=post)
            pprint({
                'Article Title': scraped_data.article_title,
                'Authors': scraped_data.article_authors,
                'Publication Date': scraped_data.publication_date,
                'Content': scraped_data.article_content,
                'Top Image': scraped_data.top_image,
                'Keywords': scraped_data.article_keywords,
                'Summary': scraped_data.article_summary
            })
        except ScrapedData.DoesNotExist:
            print(f"No scraped data available for post ID: {post_id}")

    except Post.DoesNotExist:
        print(f"No post found with post ID: {post_id}")

if __name__ == "__main__":
    # Test with an example post ID
    test_combined_post_and_scraped_data('21992689')  # Replace with an actual post ID from your DB
