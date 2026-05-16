import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

from dashboard.data import load_data
from dashboard.charts import (
    monthly_trend_chart,
    kpi_figures,
    day_of_week_chart,
    rfm_segment_chart,
    rfm_scatter_chart,
    cohort_heatmap_chart,
    top_products_chart,
    country_bar_chart,
    country_map_chart
)
from dashboard.layout import (
    overview_layout,
    segmentation_layout,
    products_layout,
    regional_layout
)

# ── LOAD DATA ────────────────────────────────────────────────
print("Loading data from SQL Server...")
df_sales, df_rfm, df_cohort, df_country, df_raw = load_data()
print("Data loaded successfully")

# ── BUILD CHARTS ─────────────────────────────────────────────
print("Building charts...")
kpis         = kpi_figures(df_sales, df_rfm, df_country)
fig_trend    = monthly_trend_chart(df_sales)
fig_dow      = day_of_week_chart(df_sales)
fig_segment  = rfm_segment_chart(df_rfm)
fig_scatter  = rfm_scatter_chart(df_rfm)
fig_cohort   = cohort_heatmap_chart(df_cohort)
fig_products = top_products_chart(df_raw)
fig_bar      = country_bar_chart(df_country)
fig_map      = country_map_chart(df_country)
print("All charts built")

# ── COLOURS ──────────────────────────────────────────────────
BG_COLOR   = '#0F1117'
CARD_COLOR = '#1A1D27'
TEXT_COLOR = '#FFFFFF'
PRIMARY    = '#4C9BE8'

# ── APP ──────────────────────────────────────────────────────
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True
)

# ── SIDEBAR ──────────────────────────────────────────────────
sidebar = html.Div([

    html.Div([
        html.H4(
            'UK E-Commerce',
            style={
                'color': PRIMARY,
                'fontWeight': 'bold',
                'marginBottom': '4px'
            }
        ),
        html.P(
            'Analytics Dashboard',
            style={
                'color': '#AAAAAA',
                'fontSize': '12px',
                'marginBottom': '0'
            }
        )
    ], style={
        'padding': '20px 20px 10px 20px',
        'borderBottom': '1px solid #2A2D3A'
    }),

    html.Div([
        dbc.Nav([
            dbc.NavLink(
                [html.Span('📊', style={'marginRight': '10px'}),
                 'Overview'],
                href='/',
                active='exact',
                style={
                    'color': TEXT_COLOR,
                    'borderRadius': '6px',
                    'marginBottom': '4px'
                }
            ),
            dbc.NavLink(
                [html.Span('👥', style={'marginRight': '10px'}),
                 'Customer Segmentation'],
                href='/segmentation',
                active='exact',
                style={
                    'color': TEXT_COLOR,
                    'borderRadius': '6px',
                    'marginBottom': '4px'
                }
            ),
            dbc.NavLink(
                [html.Span('📦', style={'marginRight': '10px'}),
                 'Product Analysis'],
                href='/products',
                active='exact',
                style={
                    'color': TEXT_COLOR,
                    'borderRadius': '6px',
                    'marginBottom': '4px'
                }
            ),
            dbc.NavLink(
                [html.Span('🌍', style={'marginRight': '10px'}),
                 'Regional Performance'],
                href='/regional',
                active='exact',
                style={
                    'color': TEXT_COLOR,
                    'borderRadius': '6px',
                    'marginBottom': '4px'
                }
            ),
        ], vertical=True, pills=True)
    ], style={'padding': '20px'})

], style={
    'width': '240px',
    'minHeight': '100vh',
    'backgroundColor': CARD_COLOR,
    'position': 'fixed',
    'left': 0,
    'top': 0,
    'borderRight': '1px solid #2A2D3A'
})

# ── MAIN LAYOUT ──────────────────────────────────────────────
app.layout = html.Div([

    dcc.Location(id='url', refresh=False),

    sidebar,

    html.Div(
        id='page-content',
        style={
            'marginLeft': '240px',
            'backgroundColor': BG_COLOR,
            'minHeight': '100vh'
        }
    )

], style={'backgroundColor': BG_COLOR})


# ── ROUTING CALLBACK ─────────────────────────────────────────
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/segmentation':
        return segmentation_layout(fig_segment, fig_scatter, fig_cohort)
    elif pathname == '/products':
        return products_layout(fig_products)
    elif pathname == '/regional':
        return regional_layout(fig_bar, fig_map)
    else:
        return overview_layout(kpis, fig_trend, fig_dow)


# ── RUN ──────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=8050)