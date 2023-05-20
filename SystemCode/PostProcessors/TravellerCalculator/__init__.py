from PostProcessors.AbstractPostProcessor import AbstractPostProcessor, PostProcessorError
import pandas as pd
from typing import Union
import numpy as np
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

class TravellerCalculator(AbstractPostProcessor):
    def __init__(self,connection_uri="neo4j+s://85b099f8.databases.neo4j.io:7687", username="neo4j", password ="password") -> None:
        # Driver instantiation
        self.driver = GraphDatabase.driver(
            connection_uri,
            auth=(username, password)
        )
        #calculate the total visitor volume of this dataset
        query = (
                "MATCH (c1)-[r:travel_to]->(c2 {code :'SG'})"
                "RETURN max(r.visitors), min(r.visitors), avg(r.visitors)"
                )
        with self.driver.session() as session:
            results = session.run(query)
            for result in results:
                        
                self.maxvisitors=result['max(r.visitors)']
                self.minvisitors=result['min(r.visitors)']
                self.meanvisitors=result['avg(r.visitors)']

    def onehop(self,country):
        try:
            query = (
                    "MATCH (c1 {code :'" 
                    f"{country}"
                    "'})-[r:travel_to]-> (c2 {code :'SG'})"
                    "RETURN c1, c2, r"
                    )
            with self.driver.session() as session:
                results = session.run(query)
                onehop_results = []
                for result in results:
                    # print(query)

                    onehop_results.append((result['r']['visitors']-self.minvisitors)/(self.maxvisitors-self.minvisitors))
                if len(onehop_results)>1: raise Warning(f'More than one hop one country visitors found from {country} to SG')
                if len(onehop_results)==0: 
                    # print(f'No one country visitors found from {country} to SG')
                    return self.meanvisitors/(self.maxvisitors-self.minvisitors)

                return np.mean(onehop_results)

        except Exception as e:
            print(e)
            return self.meanvisitors/(self.maxvisitors-self.minvisitors) # if not found, then return mean
    
    def twohop(self,country):
        try:

            query = (
                "MATCH (c1 {code :'" 
                f"{country}"
                "'})-[r1:travel_to]->(c2)-[r2:travel_to]-> (c3 {code :'SG'})"
                "RETURN c1, c2, r1, r2, c3"
                    )
            with self.driver.session() as session:
                twohop_results = []
                results = session.run(query)
                for result in results:
                    # print(result['c2']['code'])
                    first_hop=result['r1']['visitors']
                    second_hop=result['r2']['visitors']
                    twohop_results.append(((first_hop+second_hop)-(self.minvisitors*2))/((self.maxvisitors-self.minvisitors)*2))
                if len(twohop_results)==0: 
                    # print(f'No one country visitors found from {country} to SG')
                    return self.meanvisitors/(self.maxvisitors-self.minvisitors)
                return np.mean(twohop_results)
        
        except Exception as e:
            print(e)
            return self.meanvisitors/(self.maxvisitors-self.minvisitors) # if not found, then return mean
    
    def process(self, input: Union[list,str], alpha=0.3):
        if input == []: # no location, return nan
            return np.nan
        else:
            return np.mean([self.onehop(country)+alpha*self.twohop(country) if country != 'SG' else 1 for country in input]) # if it is SG return 1
    
    def __del__(self):
        self.driver.close()
        