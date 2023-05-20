from PostProcessors.AbstractPostProcessor import AbstractPostProcessor, PostProcessorError
from PostProcessors.LocationFinder.GoogleMapGeocodingAPIRequestor import GMGeocodingAPI
# from GoogleNews import GoogleNews
import pandas as pd
from typing import Union


class LocationFinder(AbstractPostProcessor):
    def __init__(self, api_key: str ='AIzaSyAxAQEpYlOt8BFXe9q2JBXne-yhokmFevs') -> None:
        self.api_key = api_key

    def process(self, input: Union[list,str]):
        geoCodingApi = GMGeocodingAPI(self.api_key)
        result = geoCodingApi.queryCountry(input)
        return result['country'], result['country_code'], (result['lat'], result['lng'])
