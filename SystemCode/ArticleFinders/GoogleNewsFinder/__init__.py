from ArticleFinders.AbstractArticleFinder import AbstractArticleFinder, ArticleFinderError
from ArticleFinders.GoogleNewsFinder.GoogleNews import GoogleNews
# from GoogleNews import GoogleNews
import pandas as pd
from datetime import datetime

class GoogleNewsFinder(AbstractArticleFinder):
    """
    A class to find news articles using Google News.

    Parameters
    ----------
    exclude_domains : list of str, optional
        A list of domains to exclude from the search results (default is ['news.google.com']).

    Attributes
    ----------
    exclude_domains : list of str
        A list of domains to exclude from the search results.

    Methods
    -------
    find(from_date: datetime, to_date:datetime)
        Find news articles between the given dates.
    post_process(df)
        Post-process the search results.
    """

    def __init__(self, exclude_domains=['news.google.com']):
        """
        Initializes a new instance of the GoogleNewsFinder class.

        Parameters
        ----------
        exclude_domains : list of str, optional
            A list of domains to exclude from the search results (default is ['news.google.com']).    
        """
        self.exclude_domains = exclude_domains


    def find(self, from_date: datetime, to_date:datetime,query='*', max_link_result= 100)->list:
        """
        Find news articles between the given dates.

        Parameters
        ----------
        from_date : datetime
            The start date for the search.
        to_date : datetime
            The end date for the search.

        Returns
        -------
        list
            A list containing the search results.

        Raises
        ------
        ArticleFinderError
            If no links are returned from Google News.
        """
        num_per_page = 100
        news = GoogleNews(start=from_date.strftime("%m/%d/%Y"),end=to_date.strftime("%m/%d/%Y"),encode='utf-8',lang='en', page_size=100)
        news.search(query)
        df = pd.DataFrame()
        max_link_result = max_link_result if news.total_count()>max_link_result else news.total_count()
        print(f'Google return {news.total_count()} result, getting max {max_link_result}')
        for i in list(range(1, int(max_link_result/num_per_page)+1)):
            temp_df = pd.DataFrame(news.page_at(i))
            df = pd.concat([df,temp_df])
        
        # print(df)
        if df.shape[0]>0:
            links = self.post_process(df)
        else:
            raise ArticleFinderError('No links return from GoogleNews')
        return list(set(links))
    
    def post_process(self,df):
        """
        Post-process the search results.

        Parameters
        ----------
        df : pd.DataFrame
            The DataFrame containing the search results.

        Returns
        -------
        pd.DataFrame
            The post-processed DataFrame.
        
         """
        # Filter host
        df = df[df['link'].astype(str) != 'nan']
        # for domain in self.exclude_domains:
        #     df = df[~df['link'].str.contains(domain)]
        return df['link'].tolist()
        

