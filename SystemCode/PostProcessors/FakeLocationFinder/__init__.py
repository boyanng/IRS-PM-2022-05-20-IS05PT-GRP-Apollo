from PostProcessors.AbstractPostProcessor import AbstractPostProcessor, PostProcessorError
import pandas as pd
from typing import Union
import ast

class FakeLocationFinder(AbstractPostProcessor):
    def process(self, input: Union[list,str], lookup_table='KnowledgeBase\location_country_map.csv'):
        df = pd.read_csv(lookup_table)
        result = df[df['location']==input]
        # print(result.shape[0])
        if result.shape[0]>0:
            result = result.iloc[0,:]
            return result['country'], result['country_code'], ast.literal_eval(result['lat,lng'])
        else:
            return 'unknown','unknown',(0,0)