COLORS_SET = {
    'sp_red': '#d6002a',
    'sp_grey': '#e8eae8',
    'sp_black': '#333333',
    'sp_orange': '#f36c35',
    'tab_bgcolor': '#808285',
}


# GRAPH
GRAPH_LAYOUT = {
    'plot_bgcolor': COLORS_SET['sp_black'],
    'paper_bgcolor': COLORS_SET['sp_black'],
    # 'height': 150,
    # 'margin': {
    #     'l': 50,
    #     'b': 50,
    #     'r': 0,
    #     't': 50
    # },
    'xaxis': {
        'tickcolor': COLORS_SET['sp_grey'],
        # 'tickangle': 45,
        'tickfont': {
            'color': COLORS_SET['sp_grey'],
            # 'rotation': 45,
            # 'size': 10
        },
        'linecolor': COLORS_SET['sp_grey'],
        'titlefont': {
            'color': COLORS_SET['sp_grey']
        }
    },
    'yaxis': {
        'tickcolor': COLORS_SET['sp_grey'],
        'tickfont': {
            'color': COLORS_SET['sp_grey'],
            # 'size': 10
        },
        'showticklabels': True,
        'linecolor': COLORS_SET['sp_grey'],
        'titlefont': {
            'color': COLORS_SET['sp_grey']
        }
    },
    'titlefont': {
        'color': COLORS_SET['sp_grey']
    },
    'legend': {
        'font': {
            'color': COLORS_SET['sp_grey']
        }
    },
    'hovermode': "closest",
}


# Table styles
TABLE_STYLE = dict()
TABLE_STYLE['style_table'] = {\
    'overflowY': 'scroll',
    'overflowX': 'scroll',
    # 'width': '100%',
    # 'maxHeight': '500',
    # 'margin-top': 10,
}
TABLE_STYLE['style_data'] = {'whiteSpace': 'normal'}
TABLE_STYLE['content_style'] = 'grow'
TABLE_STYLE['style_header'] = {
    'backgroundColor': COLORS_SET['sp_black'],
    'color': COLORS_SET['sp_grey'],
    'fontWeight': 'bold',
    'textAlign': 'center'
}
TABLE_STYLE['style_cell'] = {
    'backgroundColor': COLORS_SET['sp_black'],
    'color': COLORS_SET['sp_grey'],
    'textAlign': 'center',
    # 'minWidth': '5px',
    # 'maxWidth': '300px',
    # 'maxHeight': '30',
    # 'overflowY': 'scroll',
    # 'borderColor': COLORS_SET['sp_grey'],
    # 'borderWidth': '0.5px',
}


# Tab styles
TAB_SELECTED_STYLE = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': COLORS_SET["tab_bgcolor"],
    'color': COLORS_SET["sp_grey"],
    'padding': '6px'
}

TAB_NORMAL_STYLE = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': COLORS_SET["sp_black"],
    'color': COLORS_SET["sp_grey"],
    'padding': '6px'
}
