import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_main.settings')  # Replace with your actual settings module
django.setup()

from activity_ingestion.lemmy_client import LemmyApiClient
from content_scraper.scraper import ArticleScraper
from post_manager.models import Post
from content_scraper.models import ScrapedData
from pprint import pprint

def run_full_test():
    # Step 1: Fetch posts using Lemmy API client and ingest them
    lemmy_instance_url = "https://lemmy.ml"  # Set your Lemmy instance URL here
    community_name = "opensource"  # Change as needed

    client = LemmyApiClient(base_url=lemmy_instance_url)
    posts = client.fetch_posts(community_name=community_name)

    # Ensure we have posts fetched
    if not posts:
        print("No posts were fetched.")

    # Step 2: Scrape the data for each post URL and save it
    for post in Post.objects.all():
        if not post.url or post.url.lower() == "no url":
            print(f"Skipping post with ID: {post.post_id} due to missing or invalid URL.")
            continue
        
        print(f"Scraping post with ID: {post.post_id}")
        print("Calling ArticleScraper with the post instance")
        scraper = ArticleScraper(post=post)  # Pass the post object directly
        scraper.scrape()
        scraper.save_scraped_data()
        print(f"Successfully scraped and saved data for post with ID: {post.post_id}")

    # Step 3: Verify the combined Post and ScrapedData entries using index
    # Select a specific index to verify (or any index that exists)
    index = 2  # Example index to select the second post
    try:
        post = Post.objects.all()[index]  # Get the post at the specified index in the DB
        if post:
            # Print Post details
            print("\nPost Information:")
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

            # Print ScrapedData linked to the post, if available
            try:
                scraped_data = ScrapedData.objects.get(post=post)
                print("\nScraped Data Information:")
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
                print(f"No scraped data available for post ID: {post.post_id}")

    except IndexError:
        print("No post found at the specified index in the database.")

if __name__ == "__main__":
    run_full_test()
