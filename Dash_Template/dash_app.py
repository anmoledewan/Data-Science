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
                html.H3('Data Science Academy'),
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
                    label='Data Exploratory Analysis',
                    # the original style of the tab
                    style=TAB_NORMAL_STYLE,
                    # the style of the tab when being selected, for instance, colors change
                    selected_style=TAB_SELECTED_STYLE,
                    children=[
                        dcc.Tabs(
                            [
                                dcc.Tab(
                                    label='Variable Descriptive Statistics',
                                    style=TAB_NORMAL_STYLE,
                                    selected_style=TAB_SELECTED_STYLE,
                                    children=[
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        # Dropdown for selecting the descriptive values
                                                        html.P(
                                                            'Select Variable',
                                                            className='sp_subheader'
                                                        ),
                                                        dcc.Dropdown(
                                                            id='descriptive-dropdown',
                                                            options=format_options(descriptive_vars),
                                                            # set all possible options
                                                            value=descriptive_vars[0],  # set default option
                                                            className='sp_dropdown'
                                                        )
                                                    ],
                                                    className='two columns' # indicate the location
                                                ),
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
                                                            id='descriptive-graph',
                                                            className='six columns'
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
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.P(
                                                            'Numeric Variable',
                                                            className='sp_subheader'
                                                        ),
                                                        dcc.Dropdown(
                                                            id='dropdown-numeric',
                                                            options=format_options(numerical_vars),
                                                            value=numerical_vars[0],
                                                            className='sp_dropdown'
                                                        ),
                                                        html.P(
                                                            'Categorical Variable',
                                                            className='sp_subheader'
                                                        ),
                                                        dcc.Dropdown(
                                                            id='dropdown-categorical',
                                                            options=format_options(categorical_vars),
                                                            value=categorical_vars[0],
                                                            className='sp_dropdown'
                                                        ),
                                                        html.P(
                                                            'Category Values',
                                                            className='sp_subheader'
                                                        ),
                                                        dcc.Dropdown(
                                                            id='dropdown-category-values',
                                                            multi=True, # allow multi selections
                                                            value=[],  # select all
                                                            className='sp_dropdown'
                                                        ),
                                                    ],
                                                    className='two columns'
                                                ),

                                                # Create the graph and table visualizations based on the selection
                                                html.Div(
                                                    children=[
                                                        # graph and table are created by the callback functions
                                                        html.Div(
                                                            id='distribution-graph',
                                                            className='seven columns',
                                                        ),
                                                        html.Div(
                                                            [
                                                                html.P(
                                                                    'Summary',
                                                                    className='sp_subheader'
                                                                ),
                                                                html.Div(
                                                                    id='distribution-table',
                                                                )
                                                            ],
                                                            className='five columns',
                                                        )

                                                    ],
                                                    className='ten columns',
                                                )
                                            ],
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
                    label='Modeling',
                    style=TAB_NORMAL_STYLE,
                    selected_style=TAB_SELECTED_STYLE,
                    children=[
                        html.Div(
                            [
                                html.H6('Linear Regression Model with log_Value of Players as Response Variable'),

                                html.Div(
                                    [
                                        # select the response and predictor variables
                                        html.Div(
                                            [
                                                html.P(
                                                    'Response Variable',
                                                    className='sp_subheader'
                                                ),
                                                dcc.RadioItems(
                                                    id='response-selection',
                                                    options=format_options(response_vars),
                                                    value=response_vars[0],  # default response variable
                                                    className='sp_radioitem',
                                                ),
                                                html.P(
                                                    'Model Predictors',
                                                    className='sp_subheader'
                                                ),
                                                dcc.Dropdown(
                                                    id='dropdown-predictors',
                                                    options=format_options(predictor_vars),
                                                    multi=True,
                                                    value=[],
                                                    className='sp_dropdown'
                                                )
                                            ],
                                            className='two columns'
                                        ),
                                        # display fitted results
                                        html.Div(
                                            [
                                                html.P(
                                                    'OLS Regression Results',
                                                    className='sp_subheader'
                                                ),
                                                html.Div(
                                                    id='coefficient-table',
                                                    style={'margin-top': 20}
                                                ),
                                                html.Div(
                                                    id='residual-graph',
                                                    style={'margin-top': 20}
                                                )
                                            ],
                                            className='ten columns'
                                        )
                                    ]
                                )
                            ],
                        )
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


#########################
#                       #
#  Callback functions   #
#                       #
#########################
# generate the graph with the dropdown selection
# component_id: clarify the component,which given the input value
# component_property: the property of the value.

# e.x. 'descriptive-graph' is given by html content division, and the output graph will be
# the children of this division, hence, the component_property = 'children'.
# if in the above layout, 'descriptive-graph' refers to a dcc.Graph component, then the
# component_property may different, like 'figure'.
@app.callback(Output(component_id='descriptive-graph', component_property='children'),
              [Input(component_id='descriptive-dropdown', component_property='value')])
def create_descriptive_graph(selection):
    if selection in numerical_vars:
        layout = deepcopy(GRAPH_LAYOUT)
        layout['title'] = 'Histogram for ' + selection
        # generating graph for dash, should use dcc.Graph, rather than matplotlib or seaborn.
        # please refer to https://plot.ly/ for more information.
        return dcc.Graph(
            figure={
                'data': [{'x': df[selection], 'type': 'histogram'}],
                'layout': layout
            }
        )
    else:
        freq = df[selection].value_counts()
        layout = deepcopy(GRAPH_LAYOUT)
        layout['title'] = 'Frequency Table for ' + selection
        return dcc.Graph(
            figure={
                'data': [{'x': freq.index, 'y': freq.values, 'type': 'bar'}],
                'layout': layout
            }
        )


# the component_property for descriptive-table is 'children'.
@app.callback(Output(component_id='descriptive-table', component_property='children'),
              [Input(component_id='descriptive-dropdown', component_property='value')])
def create_descriptive_table(selection):
    if selection in numerical_vars:
        summary = df[selection].describe().round(2)
        # generate table with dash_table
        # the columns name should be given as a dictionary
        # the data should be given as a dictionary as well.
        return dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in summary.index],
            data=[dict(summary)],
            # could give the style of table and cells separately.
            style_table=TABLE_STYLE['style_table'],
            style_cell=TABLE_STYLE['style_cell']
        )
    else:
        top_n = 6  # show only top_n keys with largest counts
        data_count = df.groupby(
            selection).size().sort_values(ascending=False).reset_index()[:top_n]
        data_count = data_count.rename({0: 'count'}, axis=1)
        return dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in data_count.columns],
            data=data_count.to_dict('rows'),
            style_table=TABLE_STYLE['style_table'],
            style_as_list_view=True,
            style_header=TABLE_STYLE['style_header'],
            style_cell=TABLE_STYLE['style_cell']
        )


# generate the options for the 'dropdown-category-values' depending on the selected values of 'dropdown-categorical'
# because the output is the options for a dropdown, the component_property is options.
@app.callback(Output(component_id='dropdown-category-values', component_property='options'),
              [Input(component_id='dropdown-categorical', component_property='value')])
def set_options_for_category_values(selection):
    return format_options(column_to_categorical_values[selection])


# could give more than one input/output to the function as a list.
@app.callback(Output(component_id='distribution-graph', component_property='children'),
              [Input(component_id='dropdown-categorical', component_property='value'),
               Input(component_id='dropdown-numeric', component_property='value'),
               Input(component_id='dropdown-category-values', component_property='value')])
def create_distribution_graph(categorical_col, numeric_col, categories):
    traces = []

    if not len(categories):
        category_selections = df[categorical_col].unique()
    else:
        category_selections = categories

    for selection in category_selections:
        # append boxes, when selecting more than one things within the category.
        traces.append(
            go.Box(y=df.loc[df[categorical_col] == selection, numeric_col], name=selection)
        )

    layout = deepcopy(GRAPH_LAYOUT)
    layout['title'] = 'Boxplot for ' + numeric_col
    graph = dcc.Graph(
        figure={
            'data': traces,
            'layout': layout
        },
    )
    return graph


@app.callback(Output(component_id='distribution-table', component_property='children'),
              [Input(component_id='dropdown-categorical', component_property='value'),
               Input(component_id='dropdown-numeric', component_property='value'),
               Input(component_id='dropdown-category-values', component_property='value')])
def create_distribution_table(categorical_col, numeric_col, categories):
    top_n = 10  # show top_n entries when all selected

    agg_types = ['count', 'mean', 'median']
    summary = df.groupby(categorical_col)[numeric_col].agg(agg_types).round(2)
    summary = summary.reset_index().sort_values('count', ascending=False)

    if not len(categories):
        summary = summary.iloc[:top_n]
    else:
        summary = summary[summary[categorical_col].isin(categories)]

    column_rename_mapping = {agg_type: "{}_{}".format(numeric_col, agg_type) for agg_type in agg_types}
    summary = summary.rename(columns=column_rename_mapping)

    return dash_table.DataTable(
        columns=[
            {"name": i, "id": i} for i in summary.columns
        ],
        data=summary.to_dict('rows'),
        style_table=TABLE_STYLE['style_table'],
        style_header=TABLE_STYLE['style_header'],
        style_cell=TABLE_STYLE['style_cell']
    )


@app.callback([Output(component_id='coefficient-table', component_property='children'),
               Output(component_id='residual-graph', component_property='children')],
              [Input(component_id='response-selection', component_property='value'),
               Input(component_id='dropdown-predictors', component_property='value')])
def create_ols_output(response_var, predictors):
    """Create the ols output based on the selections"""
#    print('\nCreating ols output...')
#    print('response : {}'.format(response_var))
#    print('predictors: {}'.format(predictors))

    df['log_value'] = np.log1p(df[response_var])

    if not len(predictors):
        return None, None

    formatted_predictors = []
    for p in predictors:
        # Among possible predictor choices, 'potential' is a numeric predictor
        # others are categorical predictors
        if p == 'potential':
            formatted_predictors.append(p)
        else:
            formatted_predictors.append('C({})'.format(p))

    formula = 'log_value ~ ' + '+'.join(formatted_predictors)

    lm = smf.ols(formula, data=df).fit()

    coef_df = lm.params.round(3).to_frame().reset_index()
    coef_df.columns = ['features', 'coefficients']

    output_table = dash_table.DataTable(
        columns=[
            {"name": i, "id": i} for i in coef_df.columns
        ],
        data=coef_df.to_dict('rows'),
        style_table=TABLE_STYLE['style_table'],
        style_cell=TABLE_STYLE['style_cell']
    )

    residual_plot_data = [
        go.Scatter(
            x=lm.fittedvalues,
            y=lm.resid,
            mode='markers',
        )
    ]

    layout = deepcopy(GRAPH_LAYOUT)
    layout['title'] = 'Residual Plot'
    layout['xaxis'].update({'title': 'Fitted Values'})
    layout['yaxis'].update({'title': 'Residuals'})

    output_graph = dcc.Graph(
        figure={
            'data': residual_plot_data,
            'layout': layout
        }
    )
    return output_table, output_graph


# if run this code on jupyter notebook, please change 'debug=False'.
if __name__ == '__main__':
    app.run_server(debug=True)
