from newspaper import Article
from content_scraper.models import ScrapedData

class ArticleScraper:
    def __init__(self, post):
        self.post = post
        self.url = post.url
        self.article = None

    def scrape(self):
        # Create an Article object from the given URL
        self.article = Article(self.url)
        
        # Download, parse, and apply NLP to the article
        self.article.download()
        self.article.parse()
        self.article.nlp()

    def save_scraped_data(self):
        # Save the scraped data to the `ScrapedData` model linked to the `Post`
        scraped_data = ScrapedData.objects.create(
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

# Usage Example:
# Assuming `post` is an instance of the Post model with a valid URL
# scraper = ArticleScraper(post)
# scraper.scrape()
# scraper.save_scraped_data()
