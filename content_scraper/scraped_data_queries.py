from content_scraper.models import ScrapedData
from django.core.exceptions import ObjectDoesNotExist

def get_all_scraped_data():
    """
    Fetches all scraped data entries from the database.

    Returns:
        QuerySet: A queryset of all scraped data objects.
    """
    return ScrapedData.objects.all()

def get_scraped_data_by_post_id(post_id):
    """
    Fetch scraped data linked to a specific post by post_id.

    Args:
        post_id (str): The ID of the post to fetch the scraped data for.

    Returns:
        ScrapedData: The scraped data object, or None if not found.
    """
    try:
        return ScrapedData.objects.get(post__post_id=post_id)
    except ObjectDoesNotExist:
        return None

def get_scraped_data_by_index(index):
    """
    Fetch scraped data by its index in the queryset.

    Args:
        index (int): The index of the scraped data to fetch.

    Returns:
        ScrapedData: The scraped data object at the specified index, or None if index is out of range.
    """
    try:
        all_data = ScrapedData.objects.all()
        return all_data[index]
    except IndexError:
        return None

# Explanation:
# 1. `get_all_scraped_data()`: Fetches all scraped data entries from the `ScrapedData` model.
# 2. `get_scraped_data_by_post_id(post_id)`: Retrieves a specific scraped data entry linked to a post ID.
# 3. `get_scraped_data_by_index(index)`: Retrieves a scraped data entry by its index in the queryset.
