from ArticleFinders.DemoNewsFinder import DemoNewsFinder
from ArticleFinders.GoogleNewsFinder import GoogleNewsFinder

class NewsFinder:
    def __init__(self, demo=False, *args, **kwargs) -> None:
        if demo == True:
            self.finder = DemoNewsFinder(*args, **kwargs)
        else:
            self.finder = GoogleNewsFinder(*args, **kwargs)

    def find(self, *args, **kwargs):
        return self.finder.find(*args, **kwargs)