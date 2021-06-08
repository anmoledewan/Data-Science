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
# !pip install sqldf
#!pip install dash_bootstrap_components
#!pip install dpd-static-support
#!pip install django-plotly-dash


import base64
from copy import deepcopy
import sqldf
# import dash package, please make sure installing the same version in the requirements.txt
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
import plotly.graph_objs as go
#import statsmodels.formula.api as smf
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_extensions import Lottie       # pip install dash-extensions
# import the different styles from styles.py
from styles import GRAPH_LAYOUT, TABLE_STYLE, TAB_NORMAL_STYLE, TAB_SELECTED_STYLE, white_button_style, red_button_style
from datetime import date
import calendar
import plotly.express as px

mapbox_access_token='pk.eyJ1IjoiYW5tb2xlZGV3YW4iLCJhIjoiY2twb20yaGFoNGN2dTJvbGF5cGFreDUyeiJ9.FcWX-9ylEYKyMjkGutqSHw'
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
               values=value_list,hole=.3
               )
data2 = [trace3]
layout2 = deepcopy(GRAPH_LAYOUT)
layout2['title'] = 'Pathfinder Overall Jobs Status for Russell 3K'
pie_fig = go.Figure(data=data2, layout=layout2)

dropdownval2=pfdata['KeyProcessStream'].astype(str).unique()

pfdata['KeyProcessStream']=pfdata['KeyProcessStream'].astype(str)



x=pfdata.groupby(['KeyProcessStream','Job Status'])

sqldf.run('select CASE WHEN KeyProcessStream = 51024 THEN \'Manual Structure Extraction Jobs\' WHEN KeyProcessStream = 51029 THEN \'Manual Company Linking Jobs\' WHEN KeyProcessStream = 51032 THEN \'Manual Rel Tagging Jobs\' END AS KeyProcessStream , count(`Job Status`) as `Job Completed` from pfdata where `Job Status` = \'Job Completed\' group by KeyProcessStream order by KeyProcessStream')
sqldf.run('select CASE WHEN KeyProcessStream = 51024 THEN \'Manual Structure Extraction Jobs\' WHEN KeyProcessStream = 51029 THEN \'Manual Company Linking Jobs\' WHEN KeyProcessStream = 51032 THEN \'Manual Rel Tagging Jobs\' END AS KeyProcessStream, count(`Job Status`) as `Job Pending` from pfdata where `Job Status` = \'Job Pending\' group by KeyProcessStream order by KeyProcessStream')

KPSdf=sqldf.run('select CASE WHEN KeyProcessStream = 51024 THEN \'Manual Structure Extraction Jobs\' WHEN KeyProcessStream = 51029 THEN \'Manual Company Linking Jobs\' WHEN KeyProcessStream = 51032 THEN \'Manual Rel Tagging Jobs\' END AS KeyProcessStream, count(`Job Status`) as `Job_Completed` from pfdata where `Job Status` = \'Job Completed\' group by KeyProcessStream order by KeyProcessStream')
KPSdf2=sqldf.run('select CASE WHEN KeyProcessStream = 51024 THEN \'Manual Structure Extraction Jobs\' WHEN KeyProcessStream = 51029 THEN \'Manual Company Linking Jobs\' WHEN KeyProcessStream = 51032 THEN \'Manual Rel Tagging Jobs\' END AS KeyProcessStream, count(`Job Status`) as `Job_Pending` from pfdata where `Job Status` = \'Job Pending\' group by KeyProcessStream order by KeyProcessStream')

KPSdf['Job_Pending']=KPSdf2['Job_Pending']


trace11 = go.Bar(x=KPSdf['KeyProcessStream'], y=KPSdf['Job_Completed'], name='Completed Job')
trace22 = go.Bar(x=KPSdf['KeyProcessStream'], y=KPSdf['Job_Pending'], name='Pending Job')
layout22 = deepcopy(GRAPH_LAYOUT)
layout22['title'] = 'KPS wise Job Status' 
layout22['barmode']='stack'


#######################################################################################
#########################
#                       #
#  Master Stats variables #
#                       #
#########################

#df=pd.read_excel (r'\\II02FIL001.mhf.mhc\FT\2. Operations\MDCA - Hierarchy Management\Russell 3000\Stats\Master File - Presentation.xlsx')
df=pd.read_excel (r'Master File - Presentation.xlsx')

labels4 = ['Add-New','Manual Review','Add-Exist']
value_list4=[df['Add New Count'].sum(),df['Manual Review Count'].sum(),df['Add Exist Count'].sum()]

kenshoquantdf = pd.DataFrame(
    dict(category=labels4, action=["Automated", "Manual", "Automated" ],total=["Total Companies Linked","Total Companies Linked","Total Companies Linked"] ,number=value_list4)
)

trace4 = go.Pie(labels=labels4,
               values=value_list4, hole=.3
               )
data4 = [trace4]
layout4 = deepcopy(GRAPH_LAYOUT)
layout4['title'] = 'Company Linking Distribution'
#pie_fig2 = go.Figure(data=data4, layout=layout4)

pie_fig2 = px.sunburst(kenshoquantdf, path=['total','action', 'category'], values='number', #color='time',
                       color_discrete_map={'(?)':'black', 'Lunch':'gold', 'Dinner':'darkblue'},labels={"category": "Linking Category"})
pie_fig2["layout"] =  deepcopy(GRAPH_LAYOUT)

pie_fig2.update_layout(title="Company Linking Distribution", font_color="white",)
pie_fig2.update_traces(hoverinfo='label',textinfo='label+value+percent entry', marker=dict(line=dict(color='#000000', width=2))) #['label', 'text', 'value', 'current path', 'percent root', 'percent entry', 'percent parent']







trace6 = go.Bar(x=np.sort(df['Industry Level 1'].unique()), y=df['Industry Level 1'].value_counts().sort_index(), name='Industry')

layout6 = deepcopy(GRAPH_LAYOUT)
layout6['title'] = 'Filers distributed by Industry Level 1'
#layout['barmode']='stack'
        



dfg=pd.DataFrame({'Industry': np.sort(df['Industry Level 1'].unique()), 'No of Filers': df['Industry Level 1'].value_counts().sort_index()})


#########################
#                       #
#  Doc vs DB  variables #
#                       #
#########################

docvsdb=pd.read_excel (r'Doc vs DB combined.xlsx')

labels5 = ['Automated','Manual Review','No Action Performed']
value_list5=[docvsdb['Action'][docvsdb['Action']=='Automated'].count(),
             docvsdb['Action'][docvsdb['Action']=='Manual Review'].count(),
             docvsdb['Action'][docvsdb['Action']=='No Action'].count()]
trace5 = go.Pie(labels=labels5,
               values=value_list5, hole=.3)
data5 = [trace5]
layout5 = deepcopy(GRAPH_LAYOUT)
layout5['title'] = 'Relationship Ingestion Distribution'
pie_fig5 = go.Figure(data=data5, layout=layout5)
pie_fig5.update_traces(textinfo='value+percent', marker=dict(line=dict(color='#000000', width=2))) #['label', 'text', 'value', 'percent']

#########################
#                       #
#  Symbol variables     #
#                       #
#########################
symboldf=pd.read_excel (r'Consolidated Symbol file.xlsx')

##########################
#                        #
#  Extraction variables  #
#                        #
##########################
extractiondf=pd.read_excel (r'Extraction.xlsx')


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






# load image
image_filename = 'data/spg_logo.png'
encoded_image = load_encoded_image(image_filename)

#########################
#                       #
# Create the cards      #
#                       #
#########################
#fig24=go.Figure(go.Scattergeo())
#fig24.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0}),

fig24 = go.Figure(
    go.Scattermapbox(
        lat=[40.6943],	

        lon=[-73.9249],
        mode='markers',
        #hovertemplate= "<extra></extra><em>%{customdata[3]}  </em><br>🚨  %{customdata[0]}<br>🏡  %{customdata[1]}<br>⚰️  %{customdata[2]}",
        hovertemplate = 'Filers: 19<extra></extra>',
        marker=go.scattermapbox.Marker(
            size=[19],
           # color=tmp['color']
        )
    )
)

# Specify layout information
fig24.update_layout(
    mapbox=dict(
        accesstoken=mapbox_access_token, #
        center=go.layout.mapbox.Center(lat=45, lon=-73),
        zoom=1.7
    )
)

#########################
#                       #
# Create the dash app   #
#                       #
#########################

url_filers_in = "https://assets4.lottiefiles.com/packages/lf20_i4bqu8fz.json"
url_companies = "https://assets9.lottiefiles.com/packages/lf20_EzPrWM.json"
url_calstart = "https://assets8.lottiefiles.com/private_files/lf30_qkroghd7.json"
url_calend= "https://assets8.lottiefiles.com/private_files/lf30_yzu4wlv9.json"

options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

app = dash.Dash(__name__)
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])



app.title = 'HM Coverage Expansion'


app.scripts.config.serve_locally = True

app.layout = dbc.Container([
    html.Div(
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
                
                html.H3(['Corporate Structure Coverage Expansion to Russell 3K'],style={'color': '#ffffff'}),
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
                                        html.Div(  # Row 1
                                            [     
                                                
                                                    dbc.Row(
                                                        [
                                                            dbc.Col([
                                                                dbc.Card([
                                                                    dbc.CardHeader(Lottie(options=options, width="18%", height="18%", url=url_calstart)),
                                                                    dbc.CardBody([
                                                                        html.P('Select Date Range'),
                                                                        dcc.DatePickerSingle(
                                                                                id='my-date-picker-start',
                                                                                date=date(2018, 1, 1),
                                                                               
                                                                                ),
                                                                        dcc.DatePickerSingle(
                                                                        id='my-date-picker-end',
                                                                        date=date(2021, 4, 4),
                                                                        
                                                                        ),
                                                                        ], style={'textAlign':'center'})
                                                                    ], color="dark", inverse=True),
                                                                ], width=4),
                                                            
                                                            
                                                            
                                                            dbc.Col([
                                                                dbc.Card([
                                                                    dbc.CardHeader(Lottie(options=options, width="25%", height="25%", url=url_filers_in)),
                                                                    dbc.CardBody([
                                                                        html.P('Filers Automated'),
                                                                        html.H6(str(df.shape[0]))
                                                                        ], style={'textAlign':'center'})
                                                                    ],color="dark", inverse=True ),
                                                                ], width=4),
                                                            dbc.Col([
                                                                dbc.Card([
                                                                    dbc.CardHeader(Lottie(options=options, width="25%", height="25%", url=url_companies)),
                                                                    dbc.CardBody([
                                                                        html.P('Total Subsidiaries Extracted'),
                                                                        html.H6(str(df['count previous year'].sum()+df['count current year'].sum()))
                                                                        ], style={'textAlign':'center'})
                                                                    ],color="dark", inverse=True),
                                                                ], width=4),
                                                            
                                                          
                                                            
                                                            
                                                             ],justify="center",
                                                        ),
                                                           
                                                
                                             
                                               
                                                html.H5('Automation vs Manual Quantum Distribution'),
                                               
                                                dbc.Row(
                                                        [
                                                              
                                                            dbc.Col([
                                                                dbc.Card([
                                                                    #dbc.CardHeader(html.P("Company Linking Distribution"), style={'textAlign':'center'}),
                                                                    dbc.CardBody([
                                                                        
                                                                         dcc.Graph(
                                                
                                                                id='pie-graph4',
                                                                figure=pie_fig2 
                                                                
                                                                ),
                                                                       
                                                                        ], style={'textAlign':'center'})
                                                                    ],color="info", inverse=False ),
                                                                ], width=6),
                                                            dbc.Col([
                                                                dbc.Card([
                                                                    #dbc.CardHeader(Lottie(options=options, width="25%", height="25%", url=url_companies)),
                                                                    dbc.CardBody([
                                                                        
                                                                        dcc.Graph(
                                                
                                                                id='pie-graph5',
                                                                figure=pie_fig5
                                                                ),
                                                                        
                                                                        ], style={'textAlign':'center'})
                                                                    ],color="info", inverse=False),
                                                                ], width=6),
                                                            
                                                          
                                                            
                                                            
                                                             ],justify="center",
                                                        ),
                                                
                                               
                                                
                                                
                                                                                               
                                                html.Br(),
                                                 ],className='twelve columns'
                                            ),
                                               # html.Hr(),
                                                html.Div(
                                                    [
                                                        #html.Hr(),
                                                        html.H5('Overall Extraction Statistics'),
                                                        
                                                        
                                                        dbc.Row(
                                                        [
                                                              
                                                            dbc.Col([
                                                                dbc.Card([
                                                                    dbc.CardHeader(
                                                                        dbc.Tabs(
                                                                        [
                                                                            dbc.Tab(label="Industry Level Table view", tab_id="tab-1",label_style={"color": "#222222"}),
                                                                            dbc.Tab(label="Industry Level Chart-view", tab_id="tab-2",label_style={"color": "#222222"}),
                                                                            ],
                                                                        id="card-tabs",
                                                                        card=True,
                                                                        active_tab="tab-1",
                                                                        )),
                                                                    dbc.CardBody( id="card-content")
                                                                    ],color="info", inverse=False ),
                                                                ], width=6),
                                                            dbc.Col([
                                                                dbc.Card([
                                                                    dbc.CardHeader(html.H6("Country-wise Map View", style={'textAlign':'center',"color": "#222222"})),
                                                                    dbc.CardBody([
                                                                        dcc.Graph(
                                                                        figure = fig24
                                                                        ),
                                                                    
                                                                        
                                                                        ], style={'textAlign':'center'})
                                                                    ],color="info", inverse=False),
                                                                ], width=6),
                                                            
                                                          
                                                            
                                                            
                                                             ],justify="center",
                                                        ),
                                                        
                                                        
                                                        
                                                        
                                                        ],
                                                    className='twelve columns',
                                                    
                                                    ),
                                                
                                                html.Div(
                                                    [
                                                        #html.Hr(),
                                                        html.H5('Daily Extraction Statistics'),
                                                        
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
                                                        
                                                            id='descriptive-graph1',
                                                            className='five columns',

                                                        ),
                                                 
                                                          html.Div(
                                                              id='descriptive-table1',
                                                              className='four columns',
                                                              style={'margin-top': 100},
                                                            
                                                           ),
                                                    ],
                                                    className='twelve columns',
                                                    style={'margin-top': 40},
                                                ),
                                           
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
                                                            
                                                            [
                                                            dcc.Graph(
                                                                className='seven columns',
                                                                id='pie-graph1',
                                                                figure=pie_fig
                                                                ),
                                                            ]

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
                                                            className='five columns',

                                                        ),
                                                       
                                                    ],
                                                    className='twelve columns',
                                                    style={'margin-top': 40},
                                                ),
                                                
                                                html.Div(
                                                    
                                                    [
                                                       html.Div( 
                                                           [
                                                        dcc.Graph(
                                                        figure={
                                                            'data': [trace11,trace22],
                                                            'layout':layout22
                                                                })
                                                        ],className='four columns',
                                                        )
                                                        ],className='ten columns',
                                                    
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
                        html.H5(['Company Linking Data'],style={'margin-top': 50},),
                        html.Div(
                            [
                                dash_table.DataTable(
                                    id='datatable-interactivity',
                                    columns=[
                                        {'name': i, 'id': i, 'deletable': False} for i in symboldf.columns
                                        # omit the id column
                                        if i != 'id'
                                        ],
                                    data=symboldf.to_dict('records'),
                                    editable=True,
                                    filter_action="native",
                                    sort_action="native",
                                    sort_mode='multi',
                                    #row_selectable='multi',
                                    row_deletable=False,
                                    selected_rows=[],
                                    page_action='native',
                                    page_current= 0,
                                    page_size= 20,
                                    #style_table=TABLE_STYLE['style_table'],
                                    style_header=TABLE_STYLE['style_header'],
                                    style_cell=TABLE_STYLE['style_cell']
                                    ),
                                ],
                            ),
                        html.Button('Update in Database', id='submit-val', n_clicks=0),
                        html.Div(id='datatable-interactivity-container')
                                    

                    ]
                ),

                dcc.Tab(
                    label='About',
                    style=TAB_NORMAL_STYLE,
                    selected_style=TAB_SELECTED_STYLE,
                    children=[
                        html.Div(
                            [
                        
                        
                        html.Div(
                            [
                                # 'Dash is a productive Python framework for building '
                                # 'web applications. For detailed information, the "User Guide"'
                                # 'is available at ',
                                # # add the external webpages
                                # html.A('Dash User Guide', href='https://dash.plot.ly/'),
                                # ' and ',
                                # html.A('Dash Gallery', href='https://dash.plot.ly/gallery')
                            ],
                            style={'margin-left': 30, 'margin-top': 20, 'color': 'white'},
                            className='ten columns',
                        ),
                        
                        html.Div(
                            [
                            html.H4('Project Details'),
                             html.Iframe(id="embedded-pdf", src="assets/Auto Extraction  PIT - Going Forward Approach.pdf",width='80vh',height='100vh'),
                             ],className='ten columns',
                            ),
                    ],className='ten columns',
                    ),
                    ],
                ),
            ],
            vertical=False
        )
    ]
)
    ], fluid=True)


@app.callback(
    Output("card-content", "children"), [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    if str(active_tab)=='tab-1':
        return dash_table.DataTable(
            data=dfg.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in dfg.columns],
            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'font_size': '16px'},
            style_cell={'backgroundColor': 'rgb(50, 50, 50)',
                        'font_size': '14px',
                        'color': 'white'
                        },
            )
    else:
        return dcc.Graph(
            figure={
                'data': [trace6],
                'layout':layout6
                })
    
    

# @app.callback(Input('submit-val', 'n_clicks'))
# def update_output( value):
#     sdf_edited=pd.read_excel (r'Symbol-updated.xlsx')
#     sdf_edited['CIQID_old']=symboldf['Subsidiary CIQID']
#     sdf_edited['CIQID Match?'] = np.where(sdf_edited['Subsidiary CIQID'] == sdf_edited['CIQID_old'], 'True', 'False')  #create new column in df1 to check if prices match
#     sdf_edited.to_excel(r'./Symbol-updated-rows.xlsx', engine='xlsxwriter')




@app.callback(
    Output('datatable-interactivity-container', "children"),
    Input('datatable-interactivity', "derived_virtual_data"))
def update_graphs(rows):
    

    dff = symboldf if rows is None else pd.DataFrame(rows)

    if rows is None:
        return [
            html.P("")
        ]
    else:
        dff.to_excel(r'./Symbol-updated.xlsx', engine='xlsxwriter')
        return [
            html.P("")  # always runs and updates local symbol file
        ]
    


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
                hole=.3
            )
        data2 = [trace3]
        #layout2 = deepcopy(GRAPH_LAYOUT)
        layout2['title'] = 'Pathfinder Status for KPS:' + selection2
        pie_fig = go.Figure(data=data2, layout=layout2)
        return dcc.Graph(
            figure=pie_fig
            )


# if run this code on jupyter notebook, please change 'debug=False'.
if __name__ == '__main__':
    app.run_server(debug=True,port='8090',use_reloader=False)







