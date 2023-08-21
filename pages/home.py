import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
from .trend_chart import get_trendgraph_of_country, channels_trending_video, depth_analysis_layout
from .agg_metrics import get_aggregated_metrics
from kpi_analysis import get_kpi_analysis
from load_data import clean_and_load_data
from promotional_analysis import get_promotional_analysis
from distribution_analysis import get_distribution_analysis
from top5_analysis import get_top5_analysis

# Sample data for the bar chart
data = {
    'Category': ['A', 'B', 'C', 'D'],
    'Values': [10, 15, 7, 12]
}

cleaned_usa_df, cleaned_ind_df = clean_and_load_data()

# KPI & Metrics Analysis
kpi_data, usa_metric_data, ind_metric_data = get_kpi_analysis(cleaned_usa_df, cleaned_ind_df)

# Top 5 Analysis
top5_analysis = get_top5_analysis(cleaned_usa_df, cleaned_ind_df)

# Distribution Analysis
distributional_analysis = get_distribution_analysis(usa_df=cleaned_usa_df, ind_df=cleaned_ind_df)

# Promotional Analysis
promotional_analysis_data = get_promotional_analysis(usa_df=cleaned_usa_df, ind_df=cleaned_ind_df)

usa_trend_analysis_data = [
    {"img": "/assets/img/trend-publish.png", "title": "Most Popular Publish"},
    {"img": "/assets/img/trend-day.png", "title": "Most Popular Trending"},
    {"img": "/assets/img/wordcloud.png", "title": "Word Cloud Analysis"},
    {"img": "/assets/img/hashtag.png", "title": "Hashtag Analysis"}
]


ind_trend_analysis_data = [
    {"img": "/assets/img/trend-publish.png", "title": "Most Popular Publish"},
    {"img": "/assets/img/trend-day.png", "title": "Most Popular Trending"},
    {"img": "/assets/img/wordcloud.png", "title": "Word Cloud Analysis"},
    {"img": "/assets/img/hashtag.png", "title": "Hashtag Analysis"}
]

# Depth Analysis
depth_analysis_data = [
    top5_analysis,
    distributional_analysis,
    promotional_analysis_data,
    {"img": "/assets/img/object-detection.png", "title": "Object Detection",
        "analysis": [
            {"title": "Top 5 Objects Detected from Thumbnails", "data_usa": "tie, person", "data_ind": "tie, person"},
    ]}
]


graph_layout = go.Layout(
        # title='Dark Theme Bar Chart',
        paper_bgcolor='#262b49',  # Set background color to transparent
        plot_bgcolor='#262b49',   # Set plot area background color to transparent
        font=dict(color='white'),       # Set font color to white
        xaxis=dict(showgrid=False),     # Turn off x-axis grid lines
        yaxis=dict(showgrid=False),     # Turn off y-axis grid lines
        #margin=dict(t=60, b=30, l=10, r=10)  # Adjust margins for title and labels
    )

# Create a bar chart with a dark theme
fig = go.Figure(
    data=[
        go.Bar(x=data['Category'], y=data['Values'])
    ],
    layout= graph_layout
)

ytb_kpi = get_aggregated_metrics(kpi_data=kpi_data)
usa_metrics = get_trendgraph_of_country(chart_fig=fig, metric_data=usa_metric_data, country_name="USA")
ind_metrics = get_trendgraph_of_country(chart_fig=fig, metric_data=ind_metric_data, country_name="IND")
usa_trending_channel = channels_trending_video(chart_fig=fig, metric_data=usa_trend_analysis_data, country_name="USA")
ind_trending_channel = channels_trending_video(chart_fig=fig, metric_data=ind_trend_analysis_data, country_name="IND")
depth_metrics = depth_analysis_layout(data=depth_analysis_data)

layout = dbc.Container([
    dbc.Row([
        html.Div(children=[
                html.Div(className="home-partion"),
                html.Br(),
                ytb_kpi,         
                usa_metrics,
                ind_metrics,
                usa_trending_channel,
                ind_trending_channel,
                depth_metrics
            ], className="graph-container-block"),
            html.Div(children=[
                html.Div(children=[html.Div("Made with"),
                                    html.A("Dash", href="https://dash.plotly.com/", className="link-style"), 
                                    html.Div("- ploty")
                                ], className="footer-msg")]
        )])
    ])
