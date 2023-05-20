# Main script to find article and post process
import os
# set working directory
# Get the absolute path of the current script
script_path = os.path.abspath(__file__)
# Get the directory name of the script
script_dir = os.path.dirname(script_path)
# Set the current working directory to the script directory
os.chdir(script_dir)

from NewsFinder import NewsFinder
from NewsHandlers.ArticleHandler import ArticleHandler
from FeatureExtraction import FeatureExtraction
from FeatureExtractors.DiseaseExtractor import DiseaseExtractor
from FeatureExtractors.LocationExtractor import LocationExtractor
from FeatureExtractors.NumbersExtractor import NumberExtractor
from FeatureExtractors.KeywordExtractor import KeywordExtractor
from FeatureExtractors.OrganisationExtractor import OrganisationExtractor
from PostProcessors.LocationFinder import LocationFinder
from PostProcessors.FakeLocationFinder import FakeLocationFinder
from PostProcessors.InfectiousLabeler import InfectiousLabeler  
from PostProcessors.DistanceCalculator import DistanceCalculator  
from PostProcessors.TravellerCalculator import TravellerCalculator  
from PostProcessor import PostProcessor
from Scorer import score

from PrintHandler import PrintHandler

from datetime import datetime, timedelta
import click
import sys
import pandas as pd
import pickle
from tqdm import tqdm
import warnings
import time
import sqlite3
warnings.filterwarnings('ignore')
tqdm.pandas()

# Load configuration 

# Config file Argument 
# # TODO move it to a config file
production_article_search = '| site:channelnewsasia.com | site:www.straitstimes.com | site:www.malaymail.com'
keyword_list = ['case','health','report','covid19','alzheimers','marburg','symptom','infection','toll','outbreak','treatment','death','virus','disease','patient','pandemic','spread','fever','flu']
disease_ner_model_path = r'PrebuildModel\ner_model_multi_train.pkl'
neo4j_connection_uri="neo4j+s://85b099f8.databases.neo4j.io:7687"
neo4j_username="neo4j"
neo4j_password ="password"
max_production_link_count = 200
google_map_api_key = 'AIzaSyAxAQEpYlOt8BFXe9q2JBXne-yhokmFevs'

# CMD Argument
@click.option('--mode','-M', type=click.Choice(['prod', 'test','demo'], case_sensitive=False), required=True, help='prod: run today-1, demo: run 11-April-203, test:  use test data')  
@click.option('--offline','-O', help='offline more, only available in demo mode', is_flag=True)
@click.option('--date','-D', help='optional: the date to run on (YYYY-MM-DD format)) - production mode only',default=(datetime.today()-timedelta(days=1)).strftime('%Y-%m-%d'))

@click.command()
def main(mode,offline, date=datetime.today().strftime('%Y-%m-%d')):
    if mode == 'prod':
        print(date)
        prod_run(date=date)

    elif mode == 'test':
        test_run()

    elif mode == 'demo' and offline == False:
        demo_internet_run()

    elif mode == 'demo' and offline:
        demo_no_internet_run()

def prod_run(date):
    print("============================================================")
    print('Production Mode')
    print("============================================================")
    print('Note: Production mode requires internet connection, some internet query will be blocked if there is too many queries a day')
    print(f'Extracting Article Links...\n\tsearch query={production_article_search} \n\tdate={date}')
    article_links = NewsFinder(demo=False).find(query=production_article_search,from_date=datetime.strptime(date, '%Y-%m-%d'), to_date = datetime.strptime(date, '%Y-%m-%d'), max_link_result= max_production_link_count)
    article_links = list(set(article_links))
    print(f'Found {len(article_links)} Article links')
    print("------------------------------------------------------------")
    print('Extracting Article Content...')
    article_contents = []
    for link in tqdm(article_links):
        try:
            content = ArticleHandler().handle(link)
            article_contents.append(content.dict())
        except Exception as error:
            print(error)
    article_contents = pd.DataFrame(article_contents)
    print("------------------------------------------------------------")
    print('Extracting Features...')
    disease_ner_model = pickle.load(open(disease_ner_model_path,'rb'))
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
    FeatureExtractors= FeatureExtraction(handler=feature_handler)
    df = article_contents.join(pd.DataFrame.from_records(article_contents.progress_apply(lambda x: FeatureExtractors.extract(x),
                                                    axis=1).values, 
                                        index=article_contents.index))
    print("------------------------------------------------------------")
    print('Post Processing Features...')
    PostProcessors = PostProcessor(processors=[
        {
            'field' : ['country', 'country_code','lat,lng'],
            'method': LocationFinder(api_key=google_map_api_key),
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
            'method': TravellerCalculator(neo4j_connection_uri, neo4j_username, neo4j_password),
            'on': 'country_code',
            'aggregate':True
        },

    ])
    post_processed_result = df.progress_apply(lambda x: PostProcessors.process(x),axis=1)
    del PostProcessors
    now = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    print('Scoring...')
    scored_result = score(post_processed_result)
    scored_result.to_csv(f'output\{now}_prod_result.csv',index=False)
    print(f"Done. Output: output\{now}_prod_result.csv")
    # To db
    conn = sqlite3.connect('KnowledgeBase\ApolloDB.db')
    c = conn.cursor()
    for c in ['publish_date','location','disease','keywords','organisation','country','country_code','lat,lng']:
        scored_result[c] = scored_result[c].astype(str)
    scored_result['date'] = date
    scored_result.to_sql('article', conn, if_exists='append', index=False)
    print(f"Successfully append to DB")
    

def test_run():
    print("============================================================")
    print('Test mode (Predefined Dataset, No Internet)')
    print("============================================================")
    print('*Skipped finding article from online site, loading predefine dataset...')
    article_contents = pd.read_csv(r'dataset\test_article_dataset.csv')
    print("------------------------------------------------------------")
    print('Extracting Features...')
    disease_ner_model = pickle.load(open(disease_ner_model_path,'rb'))
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
    FeatureExtractors= FeatureExtraction(handler=feature_handler)
    df = article_contents.join(pd.DataFrame.from_records(article_contents.progress_apply(lambda x: FeatureExtractors.extract(x),
                                                    axis=1).values, 
                                        index=article_contents.index))
    print("------------------------------------------------------------")
    print('Post Processing Features...')
    PostProcessors = PostProcessor(processors=[
        {
            'field' : ['country', 'country_code','lat,lng'],
            'method': FakeLocationFinder(),
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
        { # TODO: change to offline mode
            'field' : ['traveller_score'],
            'method': TravellerCalculator(neo4j_connection_uri, neo4j_username, neo4j_password),
            'on': 'country_code',
            'aggregate':True
        },

    ])
    post_processed_result = df.progress_apply(lambda x: PostProcessors.process(x),axis=1)
    del PostProcessors
    now = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    print('Scoring...')
    scored_result = score(post_processed_result)
    scored_result.to_csv(f'output\{now}_test_result.csv',index=False)
    print(f"Done. Output: output\{now}_test_result.csv")
    

def demo_internet_run():
    print("============================================================")
    print('Demo mode with internet connection')
    print("============================================================")
    print('note: Online demo mode requires internet connection, some internet query will be blocked if there is too many queries a day')
    print(f'Finding articles... \n\tsearch query: {production_article_search}')
    # article_links = NewsFinder(demo=False).find(query=production_article_search, from_date=datetime(2023,4,11), to_date = datetime(2023,4,11), max_link_result= max_production_link_count)
    article_links = NewsFinder(demo=True).find(data_path='\dataset\demo_11_04_2023.csv',from_date=(datetime.today()- timedelta(days = 1)), to_date = datetime.today())
    article_links = list(set(article_links))
    print(f'Number of links found: {len(article_links)}')
    print("------------------------------------------------------------")
    print('Read Article Content...')
    article_contents = []
    for link in tqdm(article_links):
        try:
            content = ArticleHandler().handle(link)
            article_contents.append(content.dict())
        except Exception as error:
            print('Error', error)
    article_contents = pd.DataFrame(article_contents)
    print("------------------------------------------------------------")
    print('Extracting Features...')
    disease_ner_model = pickle.load(open(disease_ner_model_path,'rb'))
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
    FeatureExtractors= FeatureExtraction(handler=feature_handler)
    df = article_contents.join(pd.DataFrame.from_records(article_contents.progress_apply(lambda x: FeatureExtractors.extract(x),
                                                    axis=1).values, 
                                        index=article_contents.index))
    print("------------------------------------------------------------")
    print('Post Processing Features...')
    PostProcessors = PostProcessor(processors=[
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
            'method': TravellerCalculator(neo4j_connection_uri, neo4j_username, neo4j_password),
            'on': 'country_code',
            'aggregate':True
        },

    ])
    post_processed_result = df.progress_apply(lambda x: PostProcessors.process(x),axis=1)
    del PostProcessors
    print('Scoring...')
    scored_result = score(post_processed_result)
    now = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    scored_result.to_csv(f'output\{now}_online_demo_result.csv',index=False)
    print(f"Done. Output: output\{now}_online_demo_result.csv")
    # To db
    conn = sqlite3.connect('KnowledgeBase\ApolloDB.db')
    c = conn.cursor()
    for c in ['publish_date','location','disease','keywords','organisation','country','country_code','lat,lng']:
        scored_result[c] = scored_result[c].astype(str)
    scored_result['date'] = datetime.now().strftime('%Y-%m-%d')
    scored_result.to_sql('article', conn, if_exists='append', index=False)
    print(f"Successfully append to DB")


def demo_no_internet_run():
    print("============================================================")
    print('Demo mode with no internet connection')
    print("============================================================")
    print('*Skipped finding article from online site, loading predefine dataset...')
    article_contents = pd.read_csv('dataset\demo_11_04_2023_article_content.csv')
    print("------------------------------------------------------------")
    print('Extracting Features...')
    disease_ner_model = pickle.load(open(disease_ner_model_path,'rb'))
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
    FeatureExtractors= FeatureExtraction(handler=feature_handler)
    df = article_contents.join(pd.DataFrame.from_records(article_contents.progress_apply(lambda x: FeatureExtractors.extract(x),
                                                    axis=1).values, 
                                        index=article_contents.index))
    print("------------------------------------------------------------")
    print('Post Processing Features...')
    PostProcessors = PostProcessor(processors=[
        {
            'field' : ['country', 'country_code','lat,lng'],
            'method': FakeLocationFinder(),
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
        { # TODO: change to offline mode
            'field' : ['traveller_score'],
            'method': TravellerCalculator(neo4j_connection_uri, neo4j_username, neo4j_password),
            'on': 'country_code',
            'aggregate':True
        },

    ])
    post_processed_result = df.progress_apply(lambda x: PostProcessors.process(x),axis=1)
    del PostProcessors
    print('Scoring...')
    scored_result = score(post_processed_result)
    now = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    scored_result.to_csv(f'output\{now}_offline_demo_result.csv',index=False)
    print(f"Done. Output: output\{now}_offline_demo_result.csv")
    # To db
    conn = sqlite3.connect('KnowledgeBase\ApolloDB.db')
    c = conn.cursor()
    for c in ['publish_date','location','disease','keywords','organisation','country','country_code','lat,lng']:
        scored_result[c] = scored_result[c].astype(str)
    scored_result['date'] = datetime.now().strftime('%Y-%m-%d')
    scored_result.to_sql('article', conn, if_exists='append', index=False)
    print(f"Successfully append to DB")


if __name__=='__main__':
    sys.stdout = PrintHandler()
    print(f'Working Directory =  {script_dir}')
    main()

