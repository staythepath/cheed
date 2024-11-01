import django
import os
from scraped_data_queries import get_all_scraped_data, get_scraped_data_by_post_id
from pprint import pprint

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_main.settings')
django.setup()

def query_and_print_all_scraped_data():
    # Query all scraped data entries
    all_scraped_data = get_all_scraped_data()

    for data in all_scraped_data:
        pprint({
            'Post ID': data.post.post_id,
            'Article Title': data.article_title,
            'Authors': data.article_authors,
            'Publication Date': data.publication_date,
            'Content': data.article_content,
            'Top Image': data.top_image,
            'Keywords': data.article_keywords,
            'Summary': data.article_summary,
        })
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    query_and_print_all_scraped_data()
