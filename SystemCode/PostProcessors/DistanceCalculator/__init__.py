from PostProcessors.AbstractPostProcessor import AbstractPostProcessor, PostProcessorError
import pandas as pd
from typing import Union
import sqlite3
import math
import numpy as np

class DistanceCalculator(AbstractPostProcessor):
    
    def process(self, input: Union[list,str], destination=(1.352083, 103.819836)):
        distances = []
        for origin in input:
            # print(origin, type(origin))
            lat1, lon1 = origin
            lat2, lon2 = destination
            radius = 6371  # km
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
                math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
                math.sin(dlon / 2) * math.sin(dlon / 2))
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            if lat1 == 0 and lon1 == 0: # zero if location is unknown
                distances.append(10000) # return median if unknown 
            else:
                distances.append(radius * c)
        if distances == []: # no location -> return nan
            return np.nan
        else:
            return (20000-np.mean(distances)) / 20000 # max distance on earth
        