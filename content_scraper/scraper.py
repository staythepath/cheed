from newspaper import Article
from content_scraper.models import ScrapedData

class ArticleScraper:
    def __init__(self, post):
        self.post = post
        self.url = post.url
        self.article = None

    def scrape(self):
        """
        Downloads and processes the article from the given URL if it has not been scraped already.
        """
        # Check if ScrapedData already exists for the given post
        if ScrapedData.objects.filter(post=self.post).exists():
            print(f"Data for post ID: {self.post.post_id} has already been scraped. Skipping.")
            return

        if not self.url or self.url == "No URL" or self.url == "":
            print("No valid URL available to scrape.")
            return

        # Create an Article object from the given URL
        self.article = Article(self.url.strip())

        # Download, parse, and apply NLP to the article
        try:
            self.article.download()
            self.article.parse()
            self.article.nlp()
        except Exception as e:
            print(f"Error downloading or processing article at {self.url}: {e}")
            return

    def save_scraped_data(self):
        """
        Saves the scraped data to the `ScrapedData` model.
        If a reference is provided, it links the scraped data accordingly.
        """
        # Check again to make sure we haven't saved this post's scraped data already
        if ScrapedData.objects.filter(post=self.post).exists():
            print(f"Data for post ID: {self.post.post_id} has already been saved. Skipping.")
            return

        # Save the scraped data to the `ScrapedData` model linked to a reference, if available
        scraped_data = ScrapedData(
            post=self.post,
            article_title=self.article.title,
            article_authors=self.article.authors,
            publication_date=self.article.publish_date if self.article.publish_date else "No date available",
            article_content=self.article.text,
            top_image=self.article.top_image,
            article_keywords=self.article.keywords,
            article_summary=self.article.summary
        )

        scraped_data.save()
        print(f"Successfully saved scraped data for post ID: {self.post.post_id}")

# Example usage:
# Assuming `post` is an instance of the Post model with a valid URL
# scraper = ArticleScraper(post=post)
# scraper.scrape()
# scraper.save_scraped_data()
