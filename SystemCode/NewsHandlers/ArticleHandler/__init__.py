from newspaper import Article
from NewsHandlers.AbstractBaseHandler import AbstractBaseHandler, HandlerError
from ArticleContent import ArticleContent

class ArticleHandler(AbstractBaseHandler):
    """A class that handles articles."""
    
    @classmethod
    def handle(cls, url):
        """Downloads, parses, and processes an article from a given URL.
        
        Args:
            url (str): The URL of the article to handle.
            
        Returns:
            ArticleContent: An instance of the ArticleContent class containing the processed article data.
        """
        article = Article(url)
        try:
            article.download()
            article.parse()
            article.nlp()
            title = article.title
            body = article.text 
            summary = article.summary 
            publish_date = article.publish_date

            return ArticleContent(url, title, body, summary, publish_date)
        except Exception as e:
            print(f'Something wrong when processing: ({url})\n',e)
            return (ArticleContent(url, 'error', 'error', 'error', 'error'))
