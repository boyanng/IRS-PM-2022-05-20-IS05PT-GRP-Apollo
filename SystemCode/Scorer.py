import pandas as pd
import pickle
import torch
from scipy.spatial.distance import cosine
import numpy as np
from transformers import AutoTokenizer, TFAutoModel, pipeline
from transformers import logging as hf_logging
hf_logging.set_verbosity_error()

def disease_article_score(series, model = 'PrebuildModel\ContextualisedEmbeding-SVM-Model.pkl'):
    topic_clf = pickle.load(open(model,'rb'))
    #using bert model and bert tokeniser for the embeddings
    model = TFAutoModel.from_pretrained('bert-base-uncased')
    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
    fe = pipeline('feature-extraction', model=model, tokenizer=tokenizer)
    title_embed = series.apply(lambda x: torch.mean(torch.tensor(np.squeeze(fe(x))), dim=0).numpy())
    return(topic_clf.predict_proba(title_embed.tolist())[:,1])
    
def relevant_score(X, model = r'PrebuildModel\relevance-rf-model.pkl'):
    relevance_clf = pickle.load(open(model,'rb'))
    return relevance_clf.predict_proba(X)[:,1]  

def score(df, disease_article_weight = 1000,relevance_weight = 500):
    df['link'] = df['link']
    df['has_disease'] = df['disease'].apply(lambda x: int(len(x)>0))
    df['has_organisation'] = df['organisation'].apply(lambda x: len(x)>0)
    df['fatality_count'] = df['n_fatality'].fillna(0)
    df['case_count'] = df['n_fatality'].fillna(0)
    df['infectious_score'] = df['infectious_score'].fillna(0)
    df['traveller_score'] = df['traveller_score'].fillna(0)
    df['distance_score'] = df['distance_score'].fillna(0)
    relevance_keyword_col = ['has_disease', 'has_organisation', 'fatality_count',
    'case_count', 'infectious_score', 'traveller_score', 'distance_score']
    df['score'] = disease_article_weight*disease_article_score(df['title']) +relevance_weight*relevant_score(df[relevance_keyword_col])
    return df

if __name__=='__main__':
    df = pd.read_csv(r'dataset\test_post_processed_result.csv')
    score(df)