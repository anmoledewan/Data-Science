import base64

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objs as go


from styles import GRAPH_LAYOUT, TABLE_STYLE, TAB_NORMAL_STYLE, TAB_SELECTED_STYLE


#########################
#                       #
#    Utils functions    #
#                       #
#########################

def load_encoded_image(filename):
    """Load and encode the input image"""
    encoded_image = base64.b64encode(open(filename, 'rb').read()).decode('ascii')
    return encoded_image


# load data
df = pd.read_csv('data/fifa.csv')

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
            [
                html.Img(
                    src='data:image/png;base64,{}'.format(encoded_image),
                    style={'visibility': 'hidden'}
                ),  # Add an invisible image, just a hack to make the H3 title perfectly centered.
                html.H3('Data Science Academy'),
                html.Img(
                    src='data:image/png;base64,{}'.format(encoded_image)
                )
            ],
            className='sp_header'  # setting in style.css under .sp_header
        ),

        # Tabs for navigation
        dcc.Tabs(
            [
                dcc.Tab(
                    label='Tab 1',
                    style=TAB_NORMAL_STYLE,  # set tab style using settings in styles.py
                    selected_style=TAB_SELECTED_STYLE,  # set tab style using settings in styles.py
                    children=[
                        html.Div(
                            [
                                html.Div(
                                    [
                                        # Dropdown
                                        html.P(
                                            'Dropdown',
                                            className='sp_subheader'  # setting in style.css under .sp_subheader
                                        ),
                                        dcc.Dropdown(
                                            id='dropdown',
                                            options=[
                                                {'label': 'option 1', 'value': 'option_1'},
                                                {'label': 'option 2', 'value': 'option_2'}
                                            ],
                                            value='option_1',  # set default option
                                            className='sp_dropdown'  # setting in style.css under .sp_dropdown
                                        ),

                                        html.P(
                                            'Checklist',
                                            className='sp_subheader'
                                        ),
                                        dcc.Checklist(
                                            options=[
                                                {'label': 'option 1', 'value': 'option_1'},
                                                {'label': 'option 2', 'value': 'option_2'}
                                            ],
                                            values=['option_1'],
                                            className='sp_checklist'  # setting in style.css under .sp_checklist
                                        ),
                                        html.P(
                                            'Radioitems',
                                            className='sp_subheader'
                                        ),
                                        dcc.RadioItems(
                                            id='radioitems',
                                            options=[
                                                {'label': 'option 1', 'value': 'option_1'},
                                                {'label': 'option 2', 'value': 'option_2'}
                                            ],
                                            value='option_1',  # default response variable
                                            className='sp_radioitem',  # setting in style.css under .sp_radioitem
                                        ),
                                        html.P(
                                            'Button',
                                            className='sp_subheader'
                                        ),
                                        html.Button(
                                            'Dummy Button',
                                            className='sp_button',  # setting in style.css under .sp_button
                                        )
                                    ],
                                    className='two columns'
                                ),
                                html.Div(
                                    [
                                        # an example for graph
                                        dcc.Graph(
                                            figure=go.Figure(
                                                data=[
                                                    go.Bar(
                                                        x=[2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                                                        y=[350, 430, 474, 526, 488, 537, 500, 439],
                                                        name='Rest of world',
                                                    ),
                                                    go.Bar(
                                                        x=[2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                                                        y=[105, 156, 270, 299, 340, 403, 549, 499],
                                                        name='China',
                                                    )
                                                ],
                                                layout=go.Layout(
                                                    title='US Export of Plastic Scrap',
                                                    **GRAPH_LAYOUT
                                                )  # set graph style using settings in styles.py
                                            )
                                        ),

                                        # an example for table
                                        html.P(
                                            'Illustrative table',
                                            className='sp_subheader'
                                        ),
                                        dash_table.DataTable(
                                            id='table',
                                            columns=[{"name": i, "id": i} for i in df.columns[:4]],
                                            data=df.iloc[:5, :4].to_dict('records'),
                                            style_table=TABLE_STYLE['style_table'],
                                            style_cell=TABLE_STYLE['style_cell'],
                                            style_header=TABLE_STYLE['style_header']  # set table style using settings in styles.py
                                        )
                                    ],
                                    className='ten columns'
                                )
                            ]
                        )
                    ]
                ),

                dcc.Tab(
                    label='Tab 2',
                    style=TAB_NORMAL_STYLE,
                    selected_style=TAB_SELECTED_STYLE,
                    children=[
                        html.Div(
                            [
                                'Dash is a Python framework for building '
                                'web applications. For detailed information, the "User Guide"'
                                'is available at ',
                                html.A('Dash User Guide', href='https://dash.plot.ly/'),
                                ' and ',
                                html.A('Dash Gallery', href='https://dash.plot.ly/gallery')
                            ],
                            style={'margin-left': 30, 'margin-top': 20}
                        )
                    ]
                )
            ]
        )
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)
