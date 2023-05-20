from PostProcessors.AbstractPostProcessor import AbstractPostProcessor, PostProcessorError
import pandas as pd
from typing import Union
import sqlite3
import numpy as np

# get disease kb 
disease_obj = sqlite3.connect('KnowledgeBase\ApolloDB.db')
cursor_obj = disease_obj.cursor()
cursor_obj.execute("""SELECT * FROM disease""")
disease_kb = pd.DataFrame(cursor_obj.fetchall())
disease_kb.columns = list(map(lambda x: x[0], cursor_obj.description))
disease_obj.close()


class InfectiousLabeler(AbstractPostProcessor):
    def __init__(self, disease_kb: pd.DataFrame = disease_kb ):
        self.disease_kb = disease_kb
    
    def process(self, input: Union[list,str]):
        result = []
        for disease in input:
            d = disease_kb[(disease_kb['name'].str.contains(disease))| (disease_kb['alias'].str.contains(disease))]
            if d.shape[0]>0:
                result.append(d['infectious'].max())
            else:
                result.append(0.5)
        return np.mean(result)
        