from ArticleFinders.AbstractArticleFinder import AbstractArticleFinder, ArticleFinderError
import pandas as pd
from datetime import datetime
import os

class DemoNewsFinder:
    """NewsFinder for demo purposes, it loads a predefined dataset"""
    def find(self, from_date: datetime, to_date:datetime, data_path='\dataset\Google_compiled_01012023_23032023.csv'):
        """
        Finds and returns news articles within a specified date range.

        Parameters
        ----------
        from_date : datetime
            The start date of the date range.
        to_date : datetime
            The end date of the date range.

        Returns
        -------
        list
            A list containing the links of the news articles.
        """
        dir = os.getcwd()
        df = pd.read_csv(dir + data_path)
        return df['link'].tolist()


