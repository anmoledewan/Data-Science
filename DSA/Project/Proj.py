# -*- coding: utf-8 -*-
"""
Created on Thu May 13 01:13:01 2021

@author: Anmole_Dewan
"""

# !pip install pandas
# !pip install statsmodels
# !pip install numpy
# !pip install seaborn
# !pip install scipy
# !pip install matplotlib
# !pip install dash

# !pip install copy




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

#import pyodbc

#########################
#                       #
#  Pathfinder variables #
#                       #
#########################

#conn = pyodbc.connect('Driver={SQL Server};''Server=chodb05;''Database=Pathfinder;''Trusted_Connection=yes;')
#
#pfQuery="""select distinct i.ProcessInstanceAppianID as 'PathFinder JOB ID', f.ProcessFieldValue as 'Filer Name', g.ProcessFieldValue as 'Filer CIQID',j.ProcessFieldValue as 'File Saved',i.KeyProcessStream,
#case when i.ProcessInstanceCompleted is NULL then 'Job Pending' 
#when i.ProcessInstanceCompleted is NOT NULL then 'Job Completed'
#else 'NULL' end as 'Job Status',h.ProcessFieldValue as 'Structure Type'
#from PathFinder..ProcessInstance i
#left join PathFinder..ProcessDataValue f on i.KeyProcessInstance = f.KeyProcessInstance and f.FieldIdentifier = 'FilerName'
#left join PathFinder..ProcessDataValue g on i.KeyProcessInstance = g.KeyProcessInstance and g.FieldIdentifier = 'FilerID'
#left join PathFinder..ProcessDataValue j on i.KeyProcessInstance = j.KeyProcessInstance and j.FieldIdentifier = 'FileSaved'
#left join PathFinder..ProcessDataValue h on i.KeyProcessInstance = h.KeyProcessInstance and h.FieldIdentifier = 'StructureType'
#where i.KeyProcessStream in ( 51029,51032,51024)
#and i.UpdOperation < 2
#order by i.KeyProcessStream"""
#
#pfdata=pd.read_sql(pfQuery, conn)
#pfdata.to_excel(r"C:\Users\anmole_dewan\OneDrive - S&P Global\Documents\GitHub\Data-Science\DSA\Project\pfoutput.xlsx", engine='xlsxwriter')


pfdata=pd.read_excel (r'pfoutput.xlsx')
df_cl_label = pfdata['Job Status'].value_counts().to_frame().sort_index()


labels = np.sort(pfdata['Job Status'].unique())
df_cl_label = pfdata['Job Status'].value_counts().to_frame().sort_index()
value_list = df_cl_label['Job Status'].tolist()

trace3 = go.Pie(labels=labels,
               values=value_list,
               )
data2 = [trace3]
layout2 = deepcopy(GRAPH_LAYOUT)
layout2['title'] = 'Pathfinder Overall Jobs Status for Russell 3K'
pie_fig = go.Figure(data=data2, layout=layout2)

dropdownval2=pfdata['KeyProcessStream'].astype(str).unique()

pfdata['KeyProcessStream']=pfdata['KeyProcessStream'].astype(str)

#######################################################################################


#df=pd.read_excel (r'\\II02FIL001.mhf.mhc\FT\2. Operations\MDCA - Hierarchy Management\Russell 3000\Stats\Master File - Presentation.xlsx')
df=pd.read_excel (r'Master File - Presentation.xlsx')

labels4 = ['Add-New','Manual Review','Add-Exist']
value_list4=[df['Add New Count'].sum(),df['Manual Review Count'].sum(),df['Add Exist Count'].sum()]
trace4 = go.Pie(labels=labels4,
               values=value_list4, hole=.3
               )
data4 = [trace4]
layout4 = deepcopy(GRAPH_LAYOUT)
layout4['title'] = 'Company Linking Tag via KENSHO'
pie_fig2 = go.Figure(data=data4, layout=layout4)




#########################
#                       #
#    Utils functions    #
#                       #
#########################
dropdownval1=df['Model run Date'].astype(str).unique()
df['Model run Date']=df['Model run Date'].astype(str)

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




# get unique values for the categorical variables


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
#app.css.append_css({"external_url": "https://altd-dev.s3.amazonaws.com/dash/style.css"})
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
                                                html.H6('Total Filers Processed as part of automation:      ' + str(df.shape[0])),
                                                html.H6('Total Subsidiaries Extracted automatically:        ' + str(df['count previous year'].sum()+df['count current year'].sum())),
                                                html.Div(
                                                            
                                                    [
                                                            dcc.Graph(
                                                
                                                                id='pie-graph4',
                                                                figure=pie_fig2
                                                                ),
                                                            ],
                                                            className='five columns'
                                                        ),
                                                html.Hr(),
                                                html.Div(
                                                    [
                                                        
                                                        #html.H6('Average Subsidiaries per Filer: ' + str((df['count previous year'].sum()+df['count current year'].sum())/df.shape[0])),
                                                        
                                                        html.Div(
                                                            [
                                                                # Dropdown for selecting the descriptive values
                                                                html.P(
                                                                    'Select Model Run Date',
                                                                    className='sp_subheader'
                                                                    ),
                                                                dcc.Dropdown(
                                                                    id='descriptive-dropdown',
                                                                    options=format_options(dropdownval1),
                                                                    # set all possible options
                                                                    value=dropdownval1[0],  # set default option
                                                                    className='sp_dropdown'
                                                                    )
                                                                ],
                                                            className='two columns' # indicate the location
                                                            ),
                                                       # html.br(),
                                                        # Note that the graph and table are created by the callback functions
                                                        html.Div(
                                                            # the 'id' for the component is important
                                                            # when using this component as input or
                                                            # generating this component as output in
                                                            # the following functions.
                                                            # this has to be identical.
                                                            id='descriptive-graph1',
                                                            className='five columns',

                                                        ),
                                                        # html.Div(
                                                        #     [
                                                        #     html.Img(
                                                        #         src='data:image/png;base64,{}'.format(encoded_image),
                                                        #         style={'visibility': 'hidden'}
                                                        #         ), 
                                                        #     ],
                                                        #     className='one column',
                                                          
                                                        # ),
                                                          html.Div(
                                                              id='descriptive-table1',
                                                              className='four columns',
                                                            
                                                           ),
                                                    ],
                                                    className='twelve columns',
                                                    style={'margin-top': 40},
                                                ),
                                            ]
                                        )
                                    ],
            
                                ),

                                dcc.Tab(
                                    label='Pathfinder Job Status',
                                    style=TAB_NORMAL_STYLE,
                                    selected_style=TAB_SELECTED_STYLE,
                                    children=[html.Div(
                                            [
                                                
                                                # Create the graph and table visualizations based on the selection
                                                html.Div(
                                                    [
                                                        # Note that the graph and table are created by the callback functions
                                                        html.Div(
                                                            
                                                            
                                                            dcc.Graph(
                                                                className='seven columns',
                                                                id='pie-graph1',
                                                                figure=pie_fig
                                                                ),

                                                        ),
                                                        html.Div(
                                                            className='.offset-by-one.column',
                                                           
                                                            ),
                                                        html.Div(
                                                            [
                                                                # Dropdown for selecting the descriptive values
                                                                html.P(
                                                                    'Select KPS for Job Status',
                                                                    className='sp_subheader'
                                                                    ),
                                                                dcc.Dropdown(
                                                                    id='descriptive-dropdown2',
                                                                    options=format_options(dropdownval2),
                                                                    # set all possible options
                                                                    value=dropdownval2[0],  # set default option
                                                                    className='sp_dropdown'
                                                                    )
                                                                ],
                                                            className='two columns' # indicate the location
                                                            ),
                                                       # html.br(),
                                                        # Note that the graph and table are created by the callback functions
                                                        html.Div(
                                                           
                                                            id='pie-graph2',
                                                            className='four columns',

                                                        ),
                                                       
                                                    ],
                                                    className='ten columns',
                                                    style={'margin-top': 40},
                                                ),
                                            ]
                                        )

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

@app.callback(Output(component_id='descriptive-graph1', component_property='children'),
              Input(component_id='descriptive-dropdown', component_property='value'),
              )
def create_descriptive_graph1(selection):
        df2 = df[df['Model run Date']==selection]
        trace1 = go.Bar(x=df2['Name'], y=df2['count current year'], name='Current Year')
        trace2 = go.Bar(x=df2['Name'], y=df2['count previous year'], name='Previous Year')
        layout = deepcopy(GRAPH_LAYOUT)
        layout['title'] = 'Filers Extracted on ' + selection
        layout['barmode']='stack'
        return dcc.Graph(
            figure={
            'data': [trace1,trace2],
             'layout':layout
               })
    
@app.callback(Output(component_id='descriptive-table1', component_property='children'),
              Input(component_id='descriptive-dropdown', component_property='value'),
              )
def create_descriptive_table1(selection):
        df2 = df[df['Model run Date']==selection]
        df2=df2.iloc[:,[0,7]]
        
        return dash_table.DataTable(
            data=df2.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df2.columns],
            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'font_size': '16px'},
            style_cell={'backgroundColor': 'rgb(50, 50, 50)',
                        'font_size': '14px',
                        'color': 'white'
                        },
            )
@app.callback(Output(component_id='pie-graph2', component_property='children'),
              Input(component_id='descriptive-dropdown2', component_property='value'),
              )
def create_descriptive_graph2(selection2):
        df2 = pfdata[pfdata['KeyProcessStream']==selection2]
        df_cl_label = df2['Job Status'].value_counts().to_frame().sort_index()
        labels = np.sort(df2['Job Status'].unique())
        df_cl_label = df2['Job Status'].value_counts().to_frame().sort_index()
        value_list = df_cl_label['Job Status'].tolist()
        trace3 = go.Pie(labels=labels,
               values=value_list,
               )
        data2 = [trace3]
        layout2 = deepcopy(GRAPH_LAYOUT)
        layout2['title'] = 'Pathfinder Status for KPS:' + selection2
        pie_fig = go.Figure(data=data2, layout=layout2)
        return dcc.Graph(
            figure=pie_fig
            )


# if run this code on jupyter notebook, please change 'debug=False'.
if __name__ == '__main__':
    app.run_server(debug=True,port='8090')







