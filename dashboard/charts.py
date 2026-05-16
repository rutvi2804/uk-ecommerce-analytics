
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

#COLOUR PALETTE 
PRIMARY   = '#4C9BE8'
SECONDARY = '#F4845F'
SUCCESS   = '#2ECC71'
WARNING   = '#F39C12'
BG_COLOR  = '#0F1117'
CARD_COLOR = '#1A1D27'
TEXT_COLOR = '#FFFFFF'

CHART_LAYOUT = dict(
    paper_bgcolor=BG_COLOR,
    plot_bgcolor=BG_COLOR,
    font=dict(color=TEXT_COLOR, family='Inter, sans-serif'),
    margin=dict(l=40, r=40, t=60, b=40),
    showlegend=True
)

#CHART 1 — MONTHLY REVENUE TREND
def monthly_trend_chart(df_sales):

    monthly = df_sales.groupby(['sales_year','sales_month']).agg(
        total_revenue=('total_revenue','sum'),
        total_orders=('total_orders','sum')
    ).reset_index()

    monthly['period'] = pd.to_datetime(
        monthly['sales_year'].astype(str) + '-' +
        monthly['sales_month'].astype(str).str.zfill(2) + '-01'
    )
    monthly = monthly.sort_values('period')

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=monthly['period'],
            y=monthly['total_revenue'],
            name='Revenue',
            fill='tozeroy',
            line=dict(color=PRIMARY, width=2.5),
            fillcolor='rgba(76,155,232,0.15)',
            hovertemplate='%{x|%b %Y}<br>Revenue: £%{y:,.0f}<extra></extra>'
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=monthly['period'],
            y=monthly['total_orders'],
            name='Orders',
            line=dict(color=SECONDARY, width=2, dash='dot'),
            hovertemplate='%{x|%b %Y}<br>Orders: %{y:,}<extra></extra>'
        ),
        secondary_y=True
    )

    fig.update_layout(
        title='Monthly Revenue & Orders Trend',
        yaxis=dict(title='Revenue (£)', tickprefix='£', tickformat=',.0f'),
        yaxis2=dict(title='Total Orders'),
        **CHART_LAYOUT
    )

    return fig


#CHART 2 — KPI CARDS
def kpi_figures(df_sales, df_rfm, df_country):

    total_revenue = df_sales['total_revenue'].sum()
    total_orders = df_sales['total_orders'].sum()
    total_customers = len(df_rfm)
    avg_order_value = df_sales['avg_order_value'].mean()

    kpis = [
        ('Total Revenue',    f'£{total_revenue:,.0f}',  PRIMARY),
        ('Total Orders',     f'{total_orders:,}',        SECONDARY),
        ('Total Customers',  f'{total_customers:,}',     SUCCESS),
        ('Avg Order Value',  f'£{avg_order_value:,.2f}', WARNING),
    ]
    return kpis


#CHART 3 — REVENUE BY DAY OF WEEK 
def day_of_week_chart(df_sales):

    day_order = ['Monday','Tuesday','Wednesday',
                 'Thursday','Friday','Saturday','Sunday']

    dow = df_sales.groupby('sales_day_name').agg(
        total_revenue=('total_revenue','sum')
    ).reindex(day_order).reset_index()

    fig = go.Figure(go.Bar(
        x=dow['sales_day_name'],
        y=dow['total_revenue'],
        marker_color=PRIMARY,
        name='Revenue',          
        hovertemplate='%{x}<br>Revenue: £%{y:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title='Revenue by Day of Week',
        yaxis=dict(tickprefix='£', tickformat=',.0f'),
        **CHART_LAYOUT
    )

    return fig


#CHART 4 — RFM SEGMENTS 
def rfm_segment_chart(df_rfm):

    seg = df_rfm.groupby('segment').agg(
        count=('customer_id','count'),
        avg_revenue=('monetary','mean')
    ).reset_index().sort_values('count', ascending=True)

    fig = go.Figure(go.Bar(
        x=seg['count'],
        y=seg['segment'],
        orientation='h',
        marker_color=PRIMARY,
        hovertemplate='%{y}<br>Customers: %{x:,}<extra></extra>'
    ))

    fig.update_layout(
        title='Customer Count by RFM Segment',
        xaxis=dict(title='Number of Customers'),
        **CHART_LAYOUT
    )

    return fig


#CHART 5 — RFM SCATTER
def rfm_scatter_chart(df_rfm):

    fig = px.scatter(
        df_rfm,
        x='recency_days',
        y='monetary',
        color='segment',
        size='frequency',
        hover_data=['customer_id','segment','frequency'],
        title='RFM Customer Map — Recency vs Monetary Value',
        labels={
            'recency_days': 'Days Since Last Purchase (lower = better)',
            'monetary': 'Total Spend (£)',
            'segment': 'Segment'
        }
    )

    fig.update_layout(**CHART_LAYOUT)
    return fig


# CHART 6 — COHORT HEATMAP
def cohort_heatmap_chart(df_cohort):

    cohort_pivot = df_cohort.pivot_table(
        index='cohort_label',
        columns='month_number',
        values='retention_rate'
    )

    cohort_order = (
        df_cohort.sort_values('cohort_month')['cohort_label'].unique()
    )
    cohort_pivot = cohort_pivot.reindex(cohort_order)

    fig = go.Figure(go.Heatmap(
        z=cohort_pivot.values,
        x=[f'M{i}' for i in cohort_pivot.columns],
        y=cohort_pivot.index.tolist(),
        colorscale='YlOrRd',
        text=[[f'{v:.1f}%' if not pd.isna(v) else '' 
            for v in row] 
            for row in cohort_pivot.values],
        texttemplate='%{text}',
        hovertemplate='Cohort: %{y}<br>Month: %{x}<br>Retention: %{z:.1f}%<extra></extra>',
        showscale=True
    ))

    fig.update_layout(
        title='Monthly Cohort Retention Rate (%)',
        xaxis=dict(title='Months Since First Purchase'),
        yaxis=dict(title='Cohort Month'),
        **CHART_LAYOUT
    )

    return fig


#CHART 7 — TOP PRODUCTS 
def top_products_chart(df_raw):

    products = df_raw.groupby('description').agg(
        total_revenue=('total_price','sum'),
        total_quantity=('quantity','sum')
    ).reset_index().nlargest(15, 'total_revenue')

    fig = go.Figure(go.Bar(
        x=products['total_revenue'],
        y=products['description'],
        orientation='h',
        marker_color=PRIMARY,
        name='Revenue',
        hovertemplate='%{y}<br>Revenue: £%{x:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title='Top 15 Products by Revenue',
        xaxis=dict(tickprefix='£', tickformat=',.0f'),
        **CHART_LAYOUT
    )

    return fig


#CHART 8 — COUNTRY BAR CHART 
def country_bar_chart(df_country):

    top = df_country.nlargest(10, 'total_revenue')

    fig = go.Figure(go.Bar(
        x=top['total_revenue'],
        y=top['country'],
        orientation='h',
        marker_color=PRIMARY,
        name='Revenue',
        hovertemplate='%{y}<br>Revenue: £%{x:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title='Top 10 Countries by Revenue',
        xaxis=dict(tickprefix='£', tickformat=',.0f'),
        yaxis=dict(autorange='reversed'),
        **CHART_LAYOUT
    )

    return fig


#CHART 9 — COUNTRY MAP 
def country_map_chart(df_country):

    fig = px.choropleth(
        df_country,
        locations='country',
        locationmode='country names',
        color='total_revenue',
        hover_name='country',
        hover_data={
            'total_revenue': ':,.0f',
            'total_orders': ':,',
            'unique_customers': ':,'
        },
        color_continuous_scale='Teal',
        title='Revenue by Country'
    )

    fig.update_layout(
        **CHART_LAYOUT,
        geo=dict(
            scope='europe',
            projection_type='natural earth',
            showland=True,
            landcolor='#1A1D27',
            showocean=True,
            oceancolor='#0F1117',
            showframe=False,
            showcountries=True,
            countrycolor='#2A2D3A',
            bgcolor=BG_COLOR
        )
    )

    return fig