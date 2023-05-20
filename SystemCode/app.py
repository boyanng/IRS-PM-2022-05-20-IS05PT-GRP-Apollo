import os
# set working directory
# Get the absolute path of the current script
script_path = os.path.abspath(__file__)
# Get the directory name of the script
script_dir = os.path.dirname(script_path)
# print(f'Working Directory =  {script_dir}')

from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc

import sqlite3
import pandas as pd
import datetime

### Get list of countries user interested in (config)
country_list = pd.read_excel(script_dir+"\dataset\country_interest.xlsx")

conn = sqlite3.connect(script_dir+'\KnowledgeBase\ApolloDB.db')
query= """SELECT * from article"""

def data_preprocessing(conn, query):
    df_final= pd.read_sql_query(query, conn)
    df_final = df_final.sort_values(by=['score'], ascending=False)
    df_final['date'] = pd.to_datetime(df_final['date'], format = '%Y-%m-%d')
    return df_final


df_final= data_preprocessing(conn, query)


# Set default country as Singapore
country_value="SG"

# Create options for Country Drop-down from config file
country_options = [{'label': row['country'], 'value': row['country_code']} for n,row in country_list.iterrows()]


# Get articles based on country of choice
def get_country_articles(df,country_code):
    country_articles = df[df["country_code"].str.contains(country_code)]
    country_articles=country_articles[["id","title","summary", "link", "date"]]
    return country_articles

# Get top news articles for home page
def get_top_n_articles(df_final,n):
    top_n = df_final.head(n)
    top_n=top_n[["id","title","summary", "link", "date"]]
    return top_n


# Create cards for each article
def create_cards(row):
    title=row["title"]
    summary=row["summary"]
    link=str(row["link"])
    date=str(row["date"])[0:10]
    article_id=str(row["id"])

    return dbc.Card(
        [
            dbc.CardHeader(html.H3(title)),
            dbc.CardBody([
            html.P(summary),
            dbc.CardLink("Original Article", href=link)
            ]),
            dbc.CardFooter(date, className="card-text text-muted")
        ]
    )
        
# Arrange the news articles by looping through entire list of data of interest
def update_layout(testdata, drop_down):

    cards_list=[]
    for i, row in testdata.iterrows():
        cards_list.append(create_cards(row))

    # make the card layout
    card_layout = [
            dbc.Row([dbc.Col(card, md=4, style={'margin-top':'7px','margin-bottom':'7px'}) for card in cards_list], style={'margin-top':'7px','margin-bottom':'7px'}),
    ]

    return card_layout


# Create Home tab content page
home_tab_content = html.Div(
     [
        dcc.DatePickerRange(
            start_date_placeholder_text="Start Period",
            end_date_placeholder_text="End Period",
            calendar_orientation='vertical',
            id='date-range-picker'
        ),
        html.Div(
            update_layout(get_top_n_articles(df_final,15), drop_down=False)
            , id= 'topn-output-container'
            , style = {'width': '100%'}
        )
     ]
)





# Create Country tab content page
country_tab_content= html.Div(
    [
        dcc.Dropdown(options=country_options, value="SG", id='country-dropdown-selection', style={'margin-top':'7px','margin-bottom':'7px'}),
        html.Div(
            update_layout(get_country_articles(df_final, country_value), drop_down=True)
            , id='country-output-container'
            , style = {'width': '100%'}
        )
    ]
)


# Create the app
app = Dash(external_stylesheets=[dbc.themes.SANDSTONE])

app.layout = html.Div(
    [
        html.H1(children='Apollo News', style={'textAlign':'center','margin-top':'7px','margin-bottom':'7px'}),
        dbc.Tabs(
            [
            dbc.Tab(home_tab_content, label="Home"),
            dbc.Tab(
                country_tab_content, label="Country"
                )
            ]
        )
    ]
)

### Country drop-down value change
@app.callback(
    Output('country-output-container', 'children'),
    Input('country-dropdown-selection', 'value')
)
def update_output(value):
    country_value=value
    country=update_layout(get_country_articles(df_final, country_value), drop_down=True)
    return country



### Date range value change
@app.callback(
    Output('topn-output-container', 'children'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date'))
def update_output(start_date, end_date):
    # print("Start Date: " + start_date + "End Date: " + end_date)
    if start_date is None:
        start_date = df_final['date'].min()
    if end_date is None:
        end_date = df_final['date'].max()
    
    
    filtered_data = df_final[(df_final["date"]>= start_date) & (df_final["date"]<= end_date)]
    topn_articles = update_layout(get_top_n_articles(filtered_data,15), drop_down=False)
    return topn_articles
    


if __name__ == '__main__':
    app.run_server(debug=True)
