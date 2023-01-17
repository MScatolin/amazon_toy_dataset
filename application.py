from dash import Dash, html, dash_table, dcc
from dash_table import FormatTemplate
from dash_table.Format import Format
from dash.dependencies import Input, Output, State
from flask_caching import Cache
import plotly.graph_objects as go
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import math

external_stylesheets = [dbc.themes.BOOTSTRAP, 
                        dbc.icons.BOOTSTRAP,
                        "assets/custom.css"]
app = Dash(__name__, external_stylesheets=external_stylesheets)


money = FormatTemplate.money(0)

# filter features that are relevant for our dash
features_to_import =['product_name', 'price', 'number_of_reviews',
       'number_of_answered_questions', 'average_review_rating',
       'product_description','number_in_stock', '#_items_bought',
       'desc_len', 'desc_#_numb', 'weight', 'dimension', 'recom_age',
       'info_len', 'info_#_numb', 'info_clean', 'model_no', 'assembly',
       'educational_obj', 'material_type', 'batt_requi', 'color',
       'best_seller_rank', 'deli_dest', 'first_del_date', '#_tech_details',
       '#_items_bought_view', 'question_list', 'desc_ques', 'category_eda',
       'competitors_count', 'competitors_avg_price', 'OnlineRetail.co.uk',
       'inferred-price', 'predicted_sales', 'predicted_revenue', 'coded_0',
       'coded_1', 'coded_2', 'coded_3', 'coded_4', 'coded_5', 'coded_6',
       'coded_7', 'coded_8', 'coded_9', 'coded_10', 'coded_11', 'coded_12',
       'coded_13', 'coded_14', 'coded_15', 'coded_16', 'coded_17', 'coded_18',
       'coded_19', 'predictions', 'bsr_improvement','sales_improvement']

# actions to help guide the user about possible improvements
dict_actions = {'desc_ques': 'Elaborate on your description',
                'coded_0': 'Insert dimension info',
                'coded_1': 'Pools and accessories',
                'coded_2': 'Model Trains',
                'coded_3': 'Insert materials info',
                'coded_4': 'Cards',
                'coded_5': 'Insert recommended age',
                'coded_6': 'Arts and Coloring',
                'coded_7': 'Insert color info',
                'coded_8': 'Sounds and voices',
                'coded_9': 'Insert delivery time',
                'coded_10':'Kinect Sand',
                'coded_11': 'Baloons',
                'coded_12': 'Tattoos and makeup',
                'coded_13': 'Insert batteries info',
                'coded_14': 'Insert country shipping info',
                'coded_15': 'Price',
                'coded_16': 'Kite',
                'coded_17': 'Model actions',
                'coded_18': 'Painting',
                'coded_19': 'Role play'}

tech_topics = ['coded_0','coded_3','coded_5', 'coded_7','coded_9','coded_13','coded_14']

desc_topics = ['coded_1', 'coded_2',  'coded_4', 'coded_6', 'coded_8', 'coded_10', 'coded_11', 'coded_12',
               'coded_15', 'coded_16', 'coded_17', 'coded_18','coded_19']


# read data and do some trasnformation to simplify and improve performance
df = pd.read_csv('data/df_for_dash.csv', 
                usecols=features_to_import).sort_values(by='sales_improvement', ascending=False)
df['Category'] = 'Toys & Games'
df.rename(columns={'product_name':'Product', 
                   'category_eda':'Sub Category',
                   'sales_improvement':'Opportunity'}, inplace=True)

sub_categories = [i for i in df['Sub Category'].unique()]
tech_info_cols = ['model_no', 'weight', 'dimension', 'recom_age', 'assembly', 'educational_obj', 'batt_requi', 'material_type', 'color',
                  'first_del_date']

bsr_max = df['best_seller_rank'].max()
bsr_min = 0                  

# header buttons
button_hande = dbc.Button(
    [
        html.I(className="bi bi-linkedin me-2"),
        "Hande Gulbagci Dede",
    ],
    outline=True,
    color="light",
    href="https://www.linkedin.com/in/hgdede/",
    id="hande_in",
    style={"textTransform": "none"},
)

button_marcelo = dbc.Button(
    [
        html.I(className="bi bi-linkedin me-2"),
        "Marcelo Scatolin Queiroz",
    ],
    outline=True,
    color="light",
    href="https://www.linkedin.com/in/mscatolinqueiroz/",
    id="marcelo_in",
    style={"textTransform": "none", "marginLeft":"4px", "marginRight":"4px"},
)

button_github = dbc.Button(
    [
        html.I(className="bi bi-github me-2"),
        "View Code on GitHub",
    ],
    outline=True,
    color="light",
    href="https://github.com/MScatolin/amazon_toy_dataset",
    id="gh-link",
    style={"textTransform": "none"},
)

# main tree map graph
def opportunity_treemap():
    fig = px.treemap(
            df, 
            path=['Category','Sub Category', 'Product'],
            maxdepth=2, 
            values='Opportunity'
    )
    fig.update_traces(root_color="lightgrey")

    return fig

#header:
header = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            id='logo',
                            src=app.get_asset_url('logo.png'),
                            height="80px"
                        ),
                        md='auto',
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H3('Project Pythia'),
                                html.P('Investigating Q&A business impact on online retails')
                            ],
                            id='app-title',
                        )
                    ],
                    md=True,
                    align='center',
                ),
                ],
                align='center',
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.NavbarToggler(id='Navbar-toggler'),
                            dbc.Collapse(
                                dbc.Nav(
                                    [
                                        dbc.NavItem(button_hande),
                                        dbc.NavItem(button_marcelo),
                                        dbc.NavItem(button_github),
                                    ],
                                    navbar=True,
                                ),
                                id="Navbar-collapse",
                                navbar=True,
                            ),
                            #model_overlay,
                        ],
                        md=4,
                    ),
                ],
                align='center'
            ),
        ],
        fluid=True,
    ),
    dark=True,
    color='#0071ce',
    sticky='top',
)

# main tree map for layout
opp_treemap = dbc.Card(
                    id='treemap_card',
                    children=[
                        dbc.CardHeader('Opportunity Tree Map'),
                        dbc.CardBody(
                            [
                                dcc.Graph(
                                    id='treemap_graph',
                                    figure = opportunity_treemap(),
                                ),                
                            ],
                        ),
                    ],
               ),

# card on the right
sidebar = dbc.Card(
    id='side_bar',
    children=[
        dbc.CardHeader('Summary'),
        dbc.CardBody(
            [
                html.P(
                    id = 'label_cat',
                    children = [],
                ),
                html.H2(
                    id='bounty',
                    children= [''],
                    style={'textAlign':'center'}
                ),
                html.P(
                    children=['in montlhy revenue'],
                    style={'textAlign':'right'}
                ),    
                dash_table.DataTable(data = [],
                                    id='opp_table', 
                                    columns = [
                                        dict(id='Product', name='Product'),
                                        dict(id='Opportunity', name='Opport.', type='numeric', format=money)
                                    ],   
                                    style_cell = {
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis',
                                        'maxWidth':0
                                    },
                                    style_cell_conditional=[
                                        {'if': {'column_id': 'Product'}},
                                    ],
                                    fixed_rows={'headers': True},
                                    style_table = {'height': '325px','overflowY': 'auto'},
                                    page_size=10000,
                                    css=[{"selector": ".show-hide", "rule": "display: none"}],
                                    filter_action="native",
                                    filter_options={"placeholder_text": "Search Product"},
                )
            ],
        ),
    ],
)

# bottom element to show products
product_detail = dbc.Col(
    [    
        dbc.Card(
            id='detail_card',
            children=[
                dbc.CardHeader('Product Details'),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H2(
                                            id='product_name',
                                            children=['Select a Product to begin'],
                                            style={'textAlign':'left'}
                                        ),
                                    ],
                                    md=10,
                                ),
                                dbc.Col(
                                    [
                                        html.H3(
                                            id='product_bounty',
                                            children=[''],
                                            style={'textAlign':'right'}
                                        ),
                                    ],
                                    md=2,
                                ),
                            ],
                            
                        ),
                        dbc.Row(
                            [     
                                dbc.Col(
                                    id='stars',
                                    children=[''],
                                    md=1
                                ),
                                dbc.Col(
                                    id='avg_review',
                                    children=[''],
                                    style = {'textAlign':'center'},
                                    md=1
                                ),
                                dbc.Col(
                                    id='review_count',
                                    children=[''],
                                    style = {'textAlign':'left'},
                                    md=2
                                ),
                                dbc.Col(
                                    id='space',
                                    children=[''],
                                    md=1
                                ),
                                dbc.Col(
                                    id='ans_count',
                                    children=[''],
                                    md=2
                                ),
                                dbc.Col(
                                    id='tru_ans_count',
                                    children=[''],
                                    md=2
                                ),
                                dbc.Col(
                                    id='price',
                                    children=[''],
                                    style = {'textAlign':'right'},
                                    md=2
                                ),
                            ],
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H4('Description'),
                                        dcc.Textarea(
                                            id='description',
                                            value='',
                                            style={'width': '100%', 'height': 300, 'display': 'inline-block'},
                                        ),
                                    ],
                                    md=4,
                                    align='start'
                                ),
                                dbc.Col(
                                    [
                                        html.H4('Technical Information'),
                                        dash_table.DataTable(
                                            data = [],
                                            id='tech_info_table', 
                                            columns = [
                                                dict(id='Information', name='Information'),
                                                dict(id='Value', name='Value', type='numeric', format=Format(precision=3))
                                            ],   
                                            style_cell = {
                                                'overflow': 'hidden',
                                                'textOverflow': 'ellipsis',
                                                'maxWidth':0
                                            },
                                            style_cell_conditional=[
                                                {'if': {'column_id': 'Product'}},
                                            ],
                                            fixed_rows={'headers': True},
                                            style_table = {'height': '300px','overflowY': 'auto'},
                                            page_size=10,
                                            css=[{"selector": ".show-hide", "rule": "display: none"}],
                                            filter_action="native",
                                            filter_options={"placeholder_text": "Search Field"}
                                        )
                                    ],
                                    md=4,
                                    align = 'center'
                                ),
                                dbc.Col(
                                    [
                                        html.H4('Questions'),
                                        dcc.Textarea(
                                            id='questions',
                                            contentEditable=False,
                                            value='',
                                            style={'width': '100%', 'height': 300, 'display': 'inline-block'},
                                        ),
                                    ],
                                    md=4,
                                    align = 'end'
                                ),

                            ],
                            style={'marginTop':'20px', 'display':'none'},
                            id='product_details_row',
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.P('Consider the improvements:'),
                                        html.Ul(
                                            id = 'rec_desc',
                                            children=['test', 'test2'],
                                        )
                                    ],
                                    md=4,
                                ),
                                dbc.Col(
                                    [
                                        html.P('Recommendations:'),
                                        html.P(
                                            id = 'rec_info',
                                            children=[],
                                        )
                                    ],
                                    md=4,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Button("Predict (Soon)", disabled=True),
                                    ],
                                    md=2,
                                ),
                                dbc.Col(
                                    [
                                    html.P('Estimated improvement:'),
                                    html.H5(
                                        id='cur_improve',
                                        children=[],
                                    ),
                                    html.P(
                                        id='cur_bsr',
                                        children=[],
                                    ),
                                    html.P(
                                        id='new_bsr',
                                        children=[],
                                    )
                                 ],
                                 md=2,
                                )
                            ],
                            style={'marginTop':'20px', 'display':'none'},
                            id='suggestions_row',
                        ),
                        dbc.Row(
                            daq.GraduatedBar(
                                size=1200,
                                min=1,
                                step=1000,
                                id='bsr_bar',
                            ),
                            style={'marginTop':'20px', 'display':'none'},
                            id='slider_row',
                        ),
                        dbc.Row(
                            html.P(id='results', 
                                children=[
                                    html.I(className="bi bi-square-fill me-2",  style={'color': '#0071ce', 'paddingLeft':'10px'}),
                                    'Current Position     ', 
                                    html.I(className="bi bi-square-fill me-2",  style={'color': '#ffc220', 'paddingLeft':'10px'}),
                                    'Estimated Potential      ',
                                    html.I(className="bi bi-square-fill me-2",  style={'color': '#fa8282', 'paddingLeft':'10px'}),
                                    'Estimated Changes'
                                ],                              
                            ),
                            style={'display':'none'},
                            id='legend_row',                          
                        ),
                    ],
                ),
            ],
        ),
    ],
    md=12,
)

# app layout itself
app.layout = html.Div(
    [
        header,
        dbc.Container(
            [
                dbc.Tabs(
                    [
                        dbc.Tab(
                            [
                                dbc.Container( 
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(opp_treemap,md=8),
                                                dbc.Col(sidebar,md=4),
                                            ],
                                            
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(product_detail, md=12),
                                            ]
                                        ),
                                    ],
                                    fluid=True,
                                    className='h-100',
                                ),
                            ],
                            label = 'Interactive Tool'),
                        dbc.Tab('tab2', label = 'Business'),
                        dbc.Tab('tab3',label = 'Data'),
                        dbc.Tab('tab4',label = 'Modeling')
                    ]
                )
            ]
        )
    ]
)

# Treemap update list 
@app.callback(
    Output('opp_table','data'),
    Output('label_cat', 'children'),
    Output('bounty', 'children'),
    Input('treemap_graph','clickData'))
def filter_by_treemap(clickData):
    cat = 'Toys & Games'
    if clickData:
 
        parent = clickData['points'][0]['parent']
        label = clickData['points'][0]['label']

        if label in sub_categories:
            filtered_df = df[df['Sub Category'] == label]
            cat=label
        elif parent in sub_categories:
            filtered_df = df[df['Sub Category'] == parent]
            cat=parent
        else:
            filtered_df = df

    else:
        filtered_df = df


    return filtered_df.to_dict('records'), 'For ' + cat + ', we can increase', '$ {:,.2f}'.format(filtered_df['Opportunity'].sum())

def draw_stars(rating):
    ''' Helper method that takes a float from 0 to 5 and return html elements to draw a 5 star rate using Bootstrap icons'''
    full_stars = math.floor(rating)
    half_star = rating - full_stars
    stars = []
    for i in range(5):
        if i < full_stars:
            stars.append(html.I(className="bi bi-star-fill", style={'color': '#f2b01e'}))
        elif i == full_stars and half_star >= 0.5:
            stars.append(html.I(className="bi bi-star-half", style={'color': '#f2b01e'}))
        else:
            stars.append(html.I(className="bi bi-star"))
    return stars

def info_str_to_dict(df, columns_list, index, list_of_ids):
    ''' Helper function the takes a DataFrame, a list of columns with technical details, a specific record on the DF,
        and a list of dash_table ids. It returns a dictionary with the column ids and the values from the product
        specified by index to be used on a dash_table.DataTable()'''
    info_dict = {}
    for i in list_of_ids:
        info_dict[i] = {}
    for j in range(len(columns_list)):
        info_dict[list_of_ids[0]][str(j)] = columns_list[j]
    for k in range(len(columns_list)):
        value = df[columns_list[k]][index]
        info_dict[list_of_ids[1]][str(k)] = value

    return pd.DataFrame(info_dict)

def question_str_to_dict(question_list):
    ''' Helper function the takes a list of questions and returns a dictionary with quesitons to be used on a dash_table.DataTable()'''
    output = ''
    for i in question_list:
        output = output + i + '\n\n'  
    return output

    
def slider_marks(min, max, now, realized, future):
    marks = {"default":'#ffffff',
             "ranges":{'#0071ce':[min, now], '#fa8282':[now, realized], '#ffc220':[realized,future], '#ffffff': [future, max]}}
    return marks

@app.callback(
    Output('product_name', 'children'),
    Output('product_bounty', 'children'),
    Output('product_details_row', 'style'),
    Output('stars', 'children'),
    Output('avg_review', 'children'),
    Output('review_count', 'children'),
    Output('ans_count', 'children'),
    Output('tru_ans_count', 'children'),
    Output('price', 'children'),
    Output('description', 'value'),
    Output('tech_info_table','data'),
    Output('questions', 'value'),
    Output('bsr_bar', 'color'),
    Output('bsr_bar', 'value'),
    Output('bsr_bar', 'max'),
    Output('bsr_bar', 'step'),
    Output('slider_row', 'style'),
    Output('legend_row', 'style'),
    Output('suggestions_row', 'style'),
    Output('rec_desc', 'children'),
    Output('rec_info', 'children'),
    Output('cur_bsr', 'children'),
    Output('new_bsr', 'children'),
    Input('opp_table', 'derived_viewport_indices'),
    Input('opp_table', 'active_cell'),
    Input('opp_table', 'data'))
def show_product_name(window, cel, data):
    df = pd.DataFrame(data)
    
    bounty='$ 0'
    question_list = []
    rec_info = []
    rec_desc = []

    if cel:
        #define row:
        index = window[cel['row']]

        # now each line is one feature: 
        prod = df['Product'][index] #product name
        bounty = df['Opportunity'][index] # opportunity
        show_product = {'padding':'20px', 'display':'flex'}
        avg_rate = df['average_review_rating'][index] * 5 # avg review, descaled
        avg_rate_stars = draw_stars(avg_rate) # avg review with stats html element
        rev_count = df['number_of_reviews'][index] # number of reviews
        ans_count = df['number_of_answered_questions'][index] #number of asnwered questions
        
        if type(df['question_list'][index]) == str: # missing values are floats. Need to verify the DF later.
            question_list = eval(str(df['question_list'][index])) # question list is a string, but has a list format.
            tru_ans_count = len(question_list)
            question_list_data = question_str_to_dict(question_list)

        else:
            tru_ans_count = 0
            question_list_data = 'No questions yet :('

        price = df['price'][index]
        desc = df['product_description'][index] # textual product description
        info_data = info_str_to_dict(df, tech_info_cols, index, ['Information', 'Value']).to_dict('records')
        future_bsr = df['best_seller_rank'][index] + df['bsr_improvement'][index]
        bsr_bar_range = 1.25 * df['best_seller_rank'][index]
        bsr_bar_now = bsr_bar_range -  df['best_seller_rank'][index]
        realized = bsr_bar_now
        bsr_bar_future = bsr_bar_range - df['bsr_improvement'][index]
        steps = bsr_bar_range/100
        bsr_marks = slider_marks(0, bsr_bar_range, bsr_bar_now, realized, bsr_bar_future)

        for i in desc_topics:
            if df[i][index] == 1:
                rec_desc = rec_desc + [html.Li('Mention ' + dict_actions[i])]
            if df['desc_ques'][index] < 0.4: # TODO: verify repeating values
                rec_desc = html.Li(dict_actions['desc_ques'])
        
        for j in tech_topics:
            if df[j][index] == 1:
                rec_info = rec_info + [html.Li(dict_actions[j])]
        
        cur_bsr = 'Current Rank : {:,.0f}'.format(df['best_seller_rank'][index])
        new_bsr = 'Possible Rank : {:,.0f}'.format(df['predictions'][index])
   
        
        return [prod,
               '$ {:,.2f}'.format(bounty),
               show_product, 
               avg_rate_stars,
               '({:,.2f})'.format(avg_rate),
                str(rev_count) + ' reviews', 
                str(ans_count) + ' answered question(s)', 
                str(tru_ans_count) + ' available question(s)',
                html.H5('Price: $ {:,.2f}'.format(price)),
                desc,
                info_data,
                question_list_data,
                bsr_marks,
                bsr_bar_range,
                bsr_bar_range,
                steps,
                show_product,
                show_product,
                show_product,
                rec_desc,
                rec_info,
                cur_bsr,
                new_bsr,
                ]


    else:
        prod = 'Select a product to begin'
        pass

@app.callback(
    Output("Navbar-collapse", "is_open"),
    [Input("Navbar-toggler", "n_clicks")],
    [State("Navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=False)