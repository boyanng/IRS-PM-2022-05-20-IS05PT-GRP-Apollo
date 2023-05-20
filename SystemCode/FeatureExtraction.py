from FeatureExtractors.DiseaseExtractor import DiseaseExtractor
from FeatureExtractors.LocationExtractor import LocationExtractor
from FeatureExtractors.NumbersExtractor import NumberExtractor
from FeatureExtractors.KeywordExtractor import KeywordExtractor
from FeatureExtractors.OrganisationExtractor import OrganisationExtractor
import pickle
import pandas as pd
import spacy

disease_ner_model = pickle.load(open(r'PrebuildModel\ner_model_multi_train.pkl', 'rb'))

keyword_list = ['case','health','report','covid19','alzheimers','marburg','symptom','infection','toll','outbreak','treatment','death','virus','disease','patient','pandemic','spread','fever','flu']

feature_handler = {
    "location": {
        'method': LocationExtractor(),
        'on': 'title'
    },
    "disease": {
        'method': DiseaseExtractor(disease_ner_model),
        'on': 'title'
    },
    "keywords": {
        'method': KeywordExtractor(keywords=keyword_list),
        'on': ['title','summary']
    },
    "organisation":{
        'method': OrganisationExtractor(),
        'on': 'title'
    },
    "n_fatality": {
        'method': NumberExtractor(keywords=['die','death','kill']),
        'on': 'title'
    },
    "n_case": {
        'method': NumberExtractor(keywords=['case','patient','sick']),
        'on': 'title'
    },
}

class FeatureExtraction:
    """
    Manage Feature Extractor and manage extraction required.
    """
    def __init__(self, handler=feature_handler):
        self.feature_handler = handler

    def extract(self, series: dict):
        self.check_fields(series)
        self.features = {}
        for f, extractor in self.feature_handler.items():
            # print(extractor)
            text = self.identify_fields(series, extractor['on'])
            self.features[f] = extractor['method'].extract(text)

        return self.features
    
    def identify_fields(self, series, key):
        if type(key) == str:
            return series[key]
        if type(key) == list:
            return ' '.join([value for i,value in series[key].items()])

    def check_fields(self, series):
        required_field = []
        for i,d in self.feature_handler.items():
            if type(d['on']) == list:
                required_field = required_field + d['on']
            else:
                required_field = required_field +[d['on']]

        missing_field = list(set(required_field) - set(series.keys()))
        # print(missing_field)
        if len(missing_field)>0 :
            raise KeyError(f'Missing column in dataframe : {missing_field}')
    
        

    

if __name__=='__main__':
    # print(FeatureExtraction.extract('B.C. woman sues after husband dies of undiagnosed flesh-eating disease'))
    # print(FeatureExtraction.extract('500 in B.C. die of undiagnosed flesh-eating disease'))
    df = pd.DataFrame({'title' : 'Disease outbreak news: Wild poliovirus type 1 (WPV1) - Malawi (3 March 2022) - Malawi', 'summary': 'Disease outbreak news: Wild poliovirus type 1 (WPV1) - Malawi (3 March 2022) - Malawi'},index=[0])
    print(FeatureExtraction.extract(df.iloc[0,:]))
    