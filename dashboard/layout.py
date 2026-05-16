from dash import html, dcc
import dash_bootstrap_components as dbc

BG_COLOR   = '#0F1117'
CARD_COLOR = '#1A1D27'
TEXT_COLOR = '#FFFFFF'
PRIMARY    = '#4C9BE8'
SECONDARY  = '#F4845F'
SUCCESS    = '#2ECC71'
WARNING    = '#F39C12'

def make_kpi_card(title, value, color):
    return dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.P(
                    title,
                    style={
                        'color': '#AAAAAA',
                        'fontSize': '13px',
                        'marginBottom': '4px'
                    }
                ),
                html.H3(
                    value,
                    style={
                        'color': color,
                        'fontWeight': 'bold',
                        'marginBottom': '0'
                    }
                )
            ])
        ], style={
            'backgroundColor': CARD_COLOR,
            'border': f'1px solid {color}',
            'borderRadius': '8px'
        }),
        width=3
    )


def overview_layout(kpis, fig_trend, fig_dow):
    return html.Div([

        html.H2(
            'Overview',
            style={
                'color': TEXT_COLOR,
                'marginBottom': '20px',
                'fontWeight': 'bold'
            }
        ),

        dbc.Row([
            make_kpi_card(title, value, color)
            for title, value, color in kpis
        ], className='mb-4'),

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(figure=fig_trend)
                    ),
                    style={
                        'backgroundColor': CARD_COLOR,
                        'borderRadius': '8px',
                        'border': 'none'
                    }
                ),
                width=12
            )
        ], className='mb-4'),

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(figure=fig_dow)
                    ),
                    style={
                        'backgroundColor': CARD_COLOR,
                        'borderRadius': '8px',
                        'border': 'none'
                    }
                ),
                width=12
            )
        ])

    ], style={'padding': '20px'})


def segmentation_layout(fig_segment, fig_scatter, fig_cohort):
    return html.Div([

        html.H2(
            'Customer Segmentation',
            style={
                'color': TEXT_COLOR,
                'marginBottom': '20px',
                'fontWeight': 'bold'
            }
        ),

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(figure=fig_segment)
                    ),
                    style={
                        'backgroundColor': CARD_COLOR,
                        'borderRadius': '8px',
                        'border': 'none'
                    }
                ),
                width=6
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(figure=fig_scatter)
                    ),
                    style={
                        'backgroundColor': CARD_COLOR,
                        'borderRadius': '8px',
                        'border': 'none'
                    }
                ),
                width=6
            )
        ], className='mb-4'),

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(figure=fig_cohort)
                    ),
                    style={
                        'backgroundColor': CARD_COLOR,
                        'borderRadius': '8px',
                        'border': 'none'
                    }
                ),
                width=12
            )
        ])

    ], style={'padding': '20px'})


def products_layout(fig_products):
    return html.Div([

        html.H2(
            'Product Analysis',
            style={
                'color': TEXT_COLOR,
                'marginBottom': '20px',
                'fontWeight': 'bold'
            }
        ),

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(figure=fig_products)
                    ),
                    style={
                        'backgroundColor': CARD_COLOR,
                        'borderRadius': '8px',
                        'border': 'none'
                    }
                ),
                width=12
            )
        ])

    ], style={'padding': '20px'})


def regional_layout(fig_bar, fig_map):
    return html.Div([

        html.H2(
            'Regional Performance',
            style={
                'color': TEXT_COLOR,
                'marginBottom': '20px',
                'fontWeight': 'bold'
            }
        ),

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(figure=fig_bar)
                    ),
                    style={
                        'backgroundColor': CARD_COLOR,
                        'borderRadius': '8px',
                        'border': 'none'
                    }
                ),
                width=5
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(figure=fig_map)
                    ),
                    style={
                        'backgroundColor': CARD_COLOR,
                        'borderRadius': '8px',
                        'border': 'none'
                    }
                ),
                width=7
            )
        ])

    ], style={'padding': '20px'})