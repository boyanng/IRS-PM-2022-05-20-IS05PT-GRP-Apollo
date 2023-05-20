from PostProcessors.LocationFinder import LocationFinder
from PostProcessors.InfectiousLabeler import InfectiousLabeler  
from PostProcessors.DistanceCalculator import DistanceCalculator  
from PostProcessors.TravellerCalculator import TravellerCalculator  
import pandas as pd

class PostProcessor:
    """
    Manage PostProcessor and manage process required.
    """
    
    def __init__(self, processors=False) -> None:
        if processors:
            self.processors = processors
        else:
            self.processors = [
                {
                    'field' : ['country', 'country_code','lat,lng'],
                    'method': LocationFinder(),
                    'on': 'location',
                    'aggregate':False
                },
                {
                    'field' : ['infectious_score'],
                    'method': InfectiousLabeler(),
                    'on': 'disease',
                    'aggregate':True
                },
                {
                    'field' : ['distance_score'],
                    'method': DistanceCalculator(),
                    'on': 'lat,lng',
                    'aggregate':True
                },
                {
                    'field' : ['traveller_score'],
                    'method': TravellerCalculator(),
                    'on': 'country_code',
                    'aggregate':True
                },
            ]


    def process(self, series: pd.Series):
        series = series.copy()
        for processor in self.processors:
            # print(extractor)
            on = series[processor['on']]
            if type(on) == list:
                results = []
                for f in processor['field']:
                    series[f] = []
                if not processor['aggregate']:
                    for i in on:
                        result = processor['method'].process(i)
                        j = 0
                        if type(result) == tuple:
                            for f in processor['field']:
                                series[f].append(result[j])
                                j+=1
                        else:
                            series[f].append(result)
                else:
                    result = processor['method'].process(on)
                    series[f] = result

            else:
                result= processor['method'].process(on)
                if len(result) != len (processor['field']): raise ValueError('Number of result field and processor return unmatched')
                i = 0
                for f in processor['field']:
                    series[f] = result[i]
                    i+=1            

        return series
    
        
    def identify_fields(self, series, key):
        if type(key) == str:
            return series[key]
        if type(key) == list:
            return ' '.join([value for i,value in series[key].items()])


if __name__ == '__main__':
    import pandas as pd
    import ast
    result = pd.read_csv(r'dataset\test_feature_extraction_result.csv')
    result['location'] = result['location'].apply(lambda x:ast.literal_eval(x) )
    result['disease'] = result['disease'].apply(lambda x:ast.literal_eval(x) )
    PostProcessor().process(result.iloc[6,:])
    PostProcessor().process(result.iloc[745,:])
