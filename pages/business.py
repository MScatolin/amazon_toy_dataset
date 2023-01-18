from dash import Dash, html, dash_table, dcc
from dash_table import FormatTemplate
from dash_table.Format import Format
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


df = pd.read_csv('data/df_after_eda.csv')

business_case = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            id='context_card',
                            children = [
                                dbc.CardHeader('Business Context'),
                                dbc.CardBody(
                                    [
                                        html.P('''In online shopping, customers may seek information before deciding the 
                                                purchase from different sources, such as product descriptions, reviews, 
                                                and questions. Therefore, it is important to provide essential yet helpful 
                                                information about the product. Providing the information the customer is 
                                                looking for can reduce customer barriers to shopping with OnlineRetail,
                                                increase sales and set us apart from our competitors.'''),
                                        html.P('Our main object wiht project Pythia is:'),
                                        html.Ul(
                                            [
                                                html.Li('Gain insight about which questions customer ask about our products;'),
                                                html.Li('Determine how the Q&A feature affects our sales. ')
                                            ],
                                        ),
                                        html.H6(' Business Impact'),
                                        html.P('''The output of this project is this interactive app that shows the estimated revenue improvement
                                                of products questions asked by the customer are aligned with the information on our prodcut page
                                                We expect this app can help our marketers and marketplace sellers to  better inform our customer 
                                                decisions and increase their sales.'''),
                                        
                                        html.H6('Data'),
                                        html.P('''As this is small-scaled Proof of Concept (POC), we  collected data from 10,000 products on sale at 
                                                OnlineRetail.co.uk. There are 10K products, offered by 2651 manufacturers, containing numerical (e.g.
                                                price), categorical (e.g.  peo)
                                                fields, but mostly textual data. There are also information about the pricing of 4136 competitors.
                                                Below there is a glimpse of how the raw data looks like''')
                                        # dbc.Col(
                                        #     [
                                        #         categories_graph
                                        #     ],
                                        #     md=3
                                        
                                    ]
                                ),
                            ],    
                        ), 
                    ],
                    md=6
                ),
                dbc.Col(
                    [
                        html.H6(
                            children=['What is Best Seller Rank?']
                        ),
                        html.H6(' The opportunity in diferent products')
                    ],
                    md=6,
                ),
            ]
        )
    ]
)