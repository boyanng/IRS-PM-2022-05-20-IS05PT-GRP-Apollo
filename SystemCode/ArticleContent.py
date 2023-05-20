from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class ArticleContent:
    """A class that represents the content of an article."""
    
    link: str
    """The link of the article."""

    title: str
    """The title of the article."""
    
    body: str
    """The body text of the article."""
    
    summary: str
    """A summary of the article."""
    
    publish_date: datetime
    """The date and time when the article was published."""
    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}