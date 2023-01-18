from dash import Dash, html, dash_table, dcc
from dash_table import FormatTemplate
from dash_table.Format import Format
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.express as px
import xgboost as xgb
import pickle
import pandas as pd


df = pd.read_csv('data/df_after_eda.csv')

# features we are using on our predictor
features_to_model = ['price','number_of_reviews', 'number_of_answered_questions',
                    'average_review_rating', 'number_in_stock', '#_items_bought', 'desc_len','desc_#_numb',
                    '#_tech_details','#_items_bought_view','desc_ques','competitors_count',
                    'competitors_avg_price','coded_0', 'coded_1', 'coded_2',
                    'coded_3', 'coded_4', 'coded_5', 'coded_6', 'coded_7', 'coded_8',
                    'coded_9', 'coded_10', 'coded_11', 'coded_12', 'coded_13', 'coded_14',
                    'coded_15', 'coded_16', 'coded_17', 'coded_18', 'coded_19',
                    'Advent Calendars', 'Arts & Crafts', 'Baby & Toddler Toys',
                    'Building & Construction Toys', 'Characters & Brands',
                    'Die-Cast & Toy Vehicles', 'Dolls & Accessories', 'Fancy Dress',
                    'Figures & Playsets', 'Games', 'Hobbies', 'Jigsaws & Puzzles',
                    'Musical Toy Instruments', 'Novelty & Special Use', 'Other',
                    'Party Supplies', 'Pretend Play', 'Puppets & Puppet Theatres',
                    'Soft Toys', 'Sports Toys & Outdoor']

# pull the first product of our opportunity DF
example_prediction = pd.read_csv('data/df_for_dash.csv', usecols = features_to_model, nrows=1)

sales_curve_df = sales_est = pd.DataFrame({'bsr': [1,5,10,17,20,38,49,50,55,67,72,88,93,100,250,
                                  500,1000,2000,3000,4000,6000,8000,10000,15000,
                                  20000,25000,30000,35000,40000],
                          'monthly_sales':[13367,10011,8573,8020,7783,6362,5493,5414,
                                           5296,5011,4893,4514,4396,4230,2968,
                                           2129,1445,937,673,557,399,388,324,220,
                                           151,85,18,3,1]})


def sales_pred(x_data, y_data, x):
  try:
    for i in range(len(x_data)):
      x1 = x_data[i]
      x2 = x_data[i+1]
      y1 = y_data[i]
      y2 = y_data[i+1]
      if x1 <= x <= x2:
        slope = (y2 - y1)/(x2 - x1)
        y_intercept = y1 - slope * x1
        y = slope * x + y_intercept
        return round(y)
  except: # when more than our last point, return the last point
    return 1

def cat_plot(df):
    # Create the dataframe for this plot
    df_fig1 = df.groupby(by=['category_eda']).size().sort_values(ascending=True).reset_index()
    # Add new percentage column
    df_fig1['perc'] = round(df_fig1[0]/(df_fig1[0].sum())*100,2)
    # Plot this barh
    fig = px.bar(df_fig1, x=0, y="category_eda", orientation='h', labels = {"category_eda": "Categories",
                        "0": "Number of Products"}, color_discrete_sequence = px.colors.qualitative.G10, custom_data=['perc'])
    # Customize the plot
    fig.update_layout(title_text='Number of Products by Category', title_x=0.5, 
                    title_font_color="royalblue", plot_bgcolor="white")
    # Customize hove
    fig.update_traces(
        hovertemplate="<br>".join([
            "Number of Products: %{x}",
            "Category: %{y}",
            "Percentage: %{customdata[0]}" ]))
    # Customize axes
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')

    return fig

def avg_bsr_cat(df):
    df_fig2 = df.groupby(by=['category_eda'])['best_seller_rank'].agg(['mean', 'count','min', 'max']).sort_values(by='mean', ascending=True).reset_index()

    # Plot this barh
    fig = px.bar(df_fig2, x='mean', y="category_eda", orientation='h', labels = {"category_eda": "Categories",
                        "mean": "Average Best Sellers Rank"}, color_discrete_sequence = px.colors.qualitative.G10, custom_data=['count',	'min', 'max'])
    # Customize the plot
    fig.update_layout(title_text='Average Best Sellers Rank by Category', title_x=0.5, 
                    title_font_color="royalblue", plot_bgcolor="white")
    # Customize hove
    fig.update_traces(
        hovertemplate="<br>".join([
            "Average: %{x}",
            "Category: %{y}",
            "Number of Products: %{customdata[0]}",
            "Minimum Rank: %{customdata[1]}",
            "Maximum Rank: %{customdata[2]}"]))
    # Customize axes
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')

    return fig

def sales_curve(df):
    fig = px.scatter(df, x="bsr", y="monthly_sales",
                    labels = {"bsr": "Best Sellers Rank",
                        "monthly_sales": "Predicted Monthly Sales"}, color_discrete_sequence = px.colors.qualitative.G10)
    # Customize the plot
    fig.update_layout(title_text='Predicted Monthly Sales by Best Sellers Rank', title_x=0.5, 
                    title_font_color="royalblue", plot_bgcolor="white")

    # Customize axes
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')

    return fig


# this is me being very creative and getting 3 random producs at our datasset :)
ex_1 = 7734
ex_2 = 236
ex_3 = 0

#top opportunity index for prediction
pred_example_index = 7734

business_case = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            id='context_card',
                            children = [
                                dbc.CardHeader(html.H5('Business Context')),
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
                                                Below there is a glimpse of how the raw data looks like'''),
                                        dbc.Col(
                                            [
                                                dcc.Graph(
                                                figure = cat_plot(df),
                                            ), 
                                            ],
                                            md=12,
                                        ),
                                        dbc.Col(
                                            [
                                                dcc.Tabs(
                                                    id="tabs-examoples",
                                                    children = [
                                                        dcc.Tab(
                                                            label='Example 1',
                                                            children=[
                                                               dbc.Col(
                                                                    [
                                                                        html.H5(df['product_name'][ex_1])
                                                                    ],
                                                                ),
                                                                html.P('Product Description', style={'textAlign': 'center'}),
                                                                dcc.Textarea(
                                                                    value=df['product_description'][ex_1],
                                                                    style={'width': '100%', 'height': 100, 'display': 'inline-block'},
                                                                ),
                                                                html.P('Product Information', style={'textAlign': 'center'}),
                                                                dcc.Textarea(
                                                                    value=df['product_information'][ex_1],
                                                                    style={'width': '100%', 'height': 150, 'display': 'inline-block'},
                                                                ),
                                                                html.P('Customers Questions and Answers', style={'textAlign': 'center'}),
                                                                dcc.Textarea(
                                                                    value=df['customer_questions_and_answers'][ex_1],
                                                                    style={'width': '100%', 'height': 100, 'display': 'inline-block'},                                                                
                                                                ),
                                                            ]
                                                        ),
                                                        dcc.Tab(
                                                            label='Example 2',
                                                            children=[
                                                                dbc.Col(
                                                                    [
                                                                        html.H5(df['product_name'][ex_2])
                                                                    ],
                                                                ),
                                                                html.H6('Product Description', style={'textAlign': 'center'}),
                                                                dcc.Textarea(
                                                                    value=df['product_description'][ex_2],
                                                                    style={'width': '100%', 'height': 100, 'display': 'inline-block'},
                                                                ),
                                                                html.H6('Product Information', style={'textAlign': 'center'}),
                                                                dcc.Textarea(
                                                                    value=df['product_information'][ex_2],
                                                                    style={'width': '100%', 'height': 150, 'display': 'inline-block'},
                                                                ),
                                                                html.H6('Customers Questions and Answers', style={'textAlign': 'center'}),
                                                                dcc.Textarea(
                                                                    value=df['customer_questions_and_answers'][ex_2],
                                                                    style={'width': '100%', 'height': 150, 'display': 'inline-block'},                                                                
                                                                ),
                                                            ],
                                                        ),
                                                        dcc.Tab(
                                                            label='Example 3',
                                                            children=[
                                                                dbc.Col(
                                                                    [
                                                                        html.H5(df['product_name'][ex_3])
                                                                    ],
                                                                ),
                                                                html.H6('Product Description', style={'textAlign': 'center'}),
                                                                dcc.Textarea(
                                                                    value=df['product_description'][ex_3],
                                                                    style={'width': '100%', 'height': 100, 'display': 'inline-block'},
                                                                ),
                                                                html.H6('Product Information', style={'textAlign': 'center'}),
                                                                dcc.Textarea(
                                                                    value=df['product_information'][ex_3],
                                                                    style={'width': '100%', 'height': 150, 'display': 'inline-block'},
                                                                ),
                                                                html.H6('Customers Questions and Answers', style={'textAlign': 'center'}),
                                                                dcc.Textarea(
                                                                    value=df['customer_questions_and_answers'][ex_3],
                                                                    style={'width': '100%', 'height': 150, 'display': 'inline-block'},                                                                
                                                                ),
                                                            ],
                                                        ),
                                                    ], 
                                                ),
                                            ],
                                            md=12,
                                        ),
                                    ]
                                ),
                            ],    
                        ), 
                    ],
                    md=6
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            id='bsr_card',
                            children = [
                                dbc.CardHeader(html.H5('What is the Best Seller Rank')),
                                dbc.CardBody(
                                    [
                                        html.P('''Best sellers rank is a number that shows a product’s rank relative 
                                                  to all other products within a particular category. As all products
                                                  on this dataset belongs to 'Toys & Games' category, the rank have them
                                                  all. There are also ranks within Sub Categories, but we chose not to 
                                                  use it.'''),
                                        dbc.Col(
                                            dcc.Graph(
                                                figure = avg_bsr_cat(df)
                                            ),
                                            md=12,
                                            style = {'display':'inline-block'},
                                        ),
                                        html.P('''If you hover over the bars above you will see how large are the numbers
                                                  in Best Seller Rank, but how do we turn them into action? '''),
                                    ],
                                ),
                            ],
                        ),    
                        dbc.Card(
                            id='pred_card',
                            children = [
                                dbc.CardHeader(html.H5("What's the opportunity in our products?")),
                                dbc.CardBody(
                                    [
                                        html.P('''Our model predicts the Best Seller Rank of a product given the 
                                                  inputs like description similarity with customer questions and
                                                  quantity of technical information available. To transform our
                                                  into an intuitive number, we estimate sales number before and
                                                  after adjusts, and calculate the difference, i.e. the improvement
                                                  OPPORTUNITY!'''),
                                        html.P('''Here's a simplified version of how it works:'''),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.P('Unanswered questions:'),
                                                        daq.BooleanSwitch(
                                                            on=False,
                                                            label="Dimension",
                                                            labelPosition="right",
                                                            id='dim_tog',
                                                        ),
                                                        daq.BooleanSwitch(
                                                            on=True,
                                                            label="Recomended Age",
                                                            labelPosition="right",
                                                            id='recag_tog',
                                                        ),
                                                        daq.BooleanSwitch(
                                                            on=True,
                                                            label="Batteries Required",
                                                            labelPosition="right",
                                                            id='batt_tog',
                                                        )
                                                    ],
                                                    md=6,
                                                    style = {'align':'left'},
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                html.P('Question/Description similarity:'),
                                                                dcc.Slider(0,1,
                                                                    value=0.2,
                                                                    id='slider_sim',
                                                                ),
                                                            ],
                                                        ),
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        html.P('Current rank:'),
                                                                        html.H4(int(df['best_seller_rank'][pred_example_index]))
                                                                    ],
                                                                    md=6,
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        html.P('Predicted rank:'),
                                                                        html.H4(
                                                                            id='result_model',
                                                                            children=[],
                                                                        )
                                                                    ],
                                                                    md=6,
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                    md=6,
                                                ),
                                                html.P('''With the new best seller rank we use this curve to
                                                          estimate monthly sales:'''),
                                                dcc.Graph(figure = sales_curve(sales_curve_df)),
                                                dbc.Col(
                                                    [
                                                        html.P('Predicted Sales:'),
                                                        html.H4(
                                                            id='result_model_money',
                                                            children=[],
                                                        )
                                                    ],
                                                    md=4,
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.P('Predicted Sales:'),
                                                        html.H4('£ {:,.2f}'.format(sales_pred(sales_curve_df['bsr'], sales_curve_df['monthly_sales'], df['best_seller_rank'][pred_example_index])*df['price'][pred_example_index]))
                                                    ],
                                                    md=4,
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.P('Opportunity:'),
                                                        html.H4(
                                                            id='result_model_opp',
                                                            children=[],
                                                        ),
                                                    ],
                                                    md=4,
                                                ),
                                            ],
                                        ),  
                                    ],
                                ),
                            ],
                        ),  
                    ],
                    md=6,
                ),
            ]
        )
    ]
)

