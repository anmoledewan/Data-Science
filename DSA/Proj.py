# -*- coding: utf-8 -*-
"""
Created on Thu May 13 01:13:01 2021

@author: Anmole_Dewan
"""


import base64
from copy import deepcopy

# import dash package, please make sure installing the same version in the requirements.txt
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import statsmodels.formula.api as smf
from dash.dependencies import Input, Output
# import the different styles from styles.py
from styles import GRAPH_LAYOUT, TABLE_STYLE, TAB_NORMAL_STYLE, TAB_SELECTED_STYLE


#########################
#                       #
#  constant variables   #
#                       #
#########################

# define variables for df column names
categorical_vars = ['nationality', 'club', 'preferred_foot', 'position_group', 'age_group']
numerical_vars = ['potential', 'overall', 'wage', 'value']
descriptive_vars = categorical_vars + numerical_vars
predictor_vars = ['preferred_foot', 'age_group', 'potential']  # Used as predictors for model
response_vars = ['overall', 'value']

df=pd.read_excel (r'\\II02FIL001.mhf.mhc\FT\2. Operations\MDCA - Hierarchy Management\Russell 3000\Stats\Master File.xlsx')

df=df.tail(20)

trace1 = go.Bar(x=df['Name'], y=df['count current year'], name='Current Year')
trace2 = go.Bar(x=df['Name'], y=df['count previous year'], name='Previous Year')

#trace = go.Pie(labels=labels,
#               values=value_list,
#               marker=dict(
 #                  colors=['rgb(42,60,142)', 'rgb(199,119,68)', 'rgb(91,138,104)', 'rgb(67,125,178)', 'rgb(225,184,10)',
 #                          'rgb(165,12,12)'])
  #             )
#data=[trace]
#########################
#                       #
#    Utils functions    #
#                       #
#########################

def preprocess_df(data):
    """preprocess the input data, rename the column and drop the na rows"""
    data = data.rename({'preferred.foot': 'preferred_foot'}, axis=1)
    data = data.dropna(subset=categorical_vars, how='any')
    return data


def load_encoded_image(filename):
    """Load and encode the input image"""
    encoded_image = base64.b64encode(open(filename, 'rb').read()).decode('ascii')
    return encoded_image


def format_options(option_list):
    """Format the input option list for dash app."""
    return [{'label': i, 'value': i} for i in option_list]


#########################
#                       #
# load and process data #
#                       #
#########################

# load fifa data
df = pd.read_csv('data/fifa.csv')
df = preprocess_df(df)

# get unique values for the categorical variables
column_to_categorical_values = dict()
for column in categorical_vars:
    column_to_categorical_values.update({column: df[column].unique()})

# load image
image_filename = 'data/spg_logo.png'
encoded_image = load_encoded_image(image_filename)


#########################
#                       #
# Create the dash app   #
#                       #
#########################

app = dash.Dash()

# You can load an external css file in the following way
app.css.append_css({"external_url": "https://altd-dev.s3.amazonaws.com/dash/style.css"})
# You can also provide local css files in the assets folder.
# In this case, the css files I put in the remote s3 storage and here in the assets folder are the same.
# You may use the external css in s3 as a baseline and override certain settings with local css files.

app.scripts.config.serve_locally = True

app.layout = html.Div(
    [
        # Header with S&P logo
        html.Div(
            [   # include the image and headlines
                html.Img(
                    src='data:image/png;base64,{}'.format(encoded_image),
                    style={'visibility': 'hidden'}
                ),  # Add an invisible image, just a hack to make the H3 title perfectly centered.
                    # Also, when setting 'visibility': 'hidden', the insert component will not
                    # show up, which is helpful for generating the intermediate data for the dash.
                html.H3('Corporate Structure Coverage Expansion to Russell 3K'),
                html.Img(
                    src='data:image/png;base64,{}'.format(encoded_image)
                )
            ],
            className='sp_header'  # using CSS flexbox
        ),

        # Tabs
        dcc.Tabs(
            [
                dcc.Tab(
                    label='Stats',
                    # the original style of the tab
                    style=TAB_NORMAL_STYLE,
                    # the style of the tab when being selected, for instance, colors change
                    selected_style=TAB_SELECTED_STYLE,
                    children=[
                        dcc.Tabs(
                            [
                                dcc.Tab(
                                    label='Performance',
                                    style=TAB_NORMAL_STYLE,
                                    selected_style=TAB_SELECTED_STYLE,
                                    children=[
                                        html.Div(
                                            [
                                                
                                                # Create the graph and table visualizations based on the selection
                                                html.Div(
                                                    [
                                                        # Note that the graph and table are created by the callback functions
                                                        html.Div(
                                                            # the 'id' for the component is important
                                                            # when using this component as input or
                                                            # generating this component as output in
                                                            # the following functions.
                                                            # this has to be identical.
                                                            
                                                            dcc.Graph(
                                                                className='six columns',
                                                                id='descriptive-graph',
                                                                figure={
                                                                    'data': [trace1,trace2],
                                                                    'layout':
                                                                        go.Layout(title='Subsidiaries extracted per filer', barmode='stack')
                                                                        }),

                                                        ),
                                                        html.Div(
                                                            id='descriptive-table',
                                                            className='six columns',
                                                            style={'margin-top': 50}
                                                        ),
                                                    ],
                                                    className='ten columns',
                                                    style={'margin-top': 20},
                                                ),
                                            ]
                                        )
                                    ],
            
                                ),

                                dcc.Tab(
                                    label='Variable Distribution',
                                    style=TAB_NORMAL_STYLE,
                                    selected_style=TAB_SELECTED_STYLE,
                                    children=[

                                    ]
                                ),
                            ],
                            vertical=False,
                            style={'margin-top': 50},
                        )
                    ]
                ),

                dcc.Tab(
                    label='Extracted Data',
                    style=TAB_NORMAL_STYLE,
                    selected_style=TAB_SELECTED_STYLE,
                    children=[

                    ]
                ),

                dcc.Tab(
                    label='About',
                    style=TAB_NORMAL_STYLE,
                    selected_style=TAB_SELECTED_STYLE,
                    children=[
                        html.Div(
                            [
                                'Dash is a productive Python framework for building '
                                'web applications. For detailed information, the "User Guide"'
                                'is available at ',
                                # add the external webpages
                                html.A('Dash User Guide', href='https://dash.plot.ly/'),
                                ' and ',
                                html.A('Dash Gallery', href='https://dash.plot.ly/gallery')
                            ],
                            style={'margin-left': 30, 'margin-top': 20, 'color': 'white'}
                        )
                    ]
                ),
            ],
            vertical=False
        )
    ]
)



# if run this code on jupyter notebook, please change 'debug=False'.
if __name__ == '__main__':
    app.run_server(debug=False,port=8090)
