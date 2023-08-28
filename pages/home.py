import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
from .trend_chart import get_trendgraph_of_country, channels_trending_video, depth_analysis_layout
from .agg_metrics import get_aggregated_metrics
from kpi_analysis import get_kpi_analysis
from load_data import clean_and_load_data
from promotional_analysis import get_promotional_analysis
from distribution_analysis import get_distribution_analysis
from correlation_analysis import get_correlation_analysis_layout, get_heatmap_figure
from top5_analysis import get_top5_analysis
from graphical_analysis import get_categorory_trending_graph, get_trending_channels_graph
from insights import insights_layout

# Load the USA and IND Data
cleaned_usa_df, cleaned_ind_df = clean_and_load_data()

# Graphical Analysis
usa_category_fig = get_categorory_trending_graph(df=cleaned_usa_df, top=10)
ind_category_fig = get_categorory_trending_graph(df=cleaned_ind_df, top=10)
usa_trend_channel = get_trending_channels_graph(df=cleaned_usa_df, top=10)
ind_trend_channel = get_trending_channels_graph(df=cleaned_ind_df, top=10)

# Sample data for the bar chart
data = {
    'Category': ['A', 'B', 'C', 'D'],
    'Values': [10, 15, 7, 12]
}


# KPI & Metrics Analysis
kpi_data, usa_metric_data, ind_metric_data = get_kpi_analysis(cleaned_usa_df, cleaned_ind_df)

# Correlation Analysis
usa_corr_fig = get_heatmap_figure(df=cleaned_usa_df)
correlation_layout = get_correlation_analysis_layout(default_fig=usa_corr_fig)

# Top 5 Analysis
top5_analysis = get_top5_analysis(cleaned_usa_df, cleaned_ind_df)

# Distribution Analysis
distributional_analysis = get_distribution_analysis(usa_df=cleaned_usa_df, ind_df=cleaned_ind_df)

# Promotional Analysis
promotional_analysis_data = get_promotional_analysis(usa_df=cleaned_usa_df, ind_df=cleaned_ind_df)

usa_trend_analysis_data = [
    {"img": "/assets/img/trend-publish.png", "title": "Most Popular Publish"},
    {"img": "/assets/img/trend-day.png", "title": "Most Popular Trending"},
    {"img": "/assets/img/wordcloud.png", "title": "Word Count Analysis"},
    {"img": "/assets/img/hashtag.png", "title": "Hashtag Analysis"}
]


ind_trend_analysis_data = [
    {"img": "/assets/img/trend-publish.png", "title": "Most Popular Publish"},
    {"img": "/assets/img/trend-day.png", "title": "Most Popular Trending"},
    {"img": "/assets/img/wordcloud.png", "title": "Word Count Analysis"},
    {"img": "/assets/img/hashtag.png", "title": "Hashtag Analysis"}
]

# Depth Analysis
depth_analysis_data = [
    top5_analysis,
    distributional_analysis,
    promotional_analysis_data,
    {"img": "/assets/img/object-detection.png", "title": "Object Detection",
        "analysis": [
            {"title": "Top 5 Objects Detected from Thumbnails", "data_usa": "person, tie, car, bowl, donut", "data_ind": "person, tv, tree, tie, vegetable"},
    ]}
]


ytb_kpi = get_aggregated_metrics(kpi_data=kpi_data)
usa_metrics = get_trendgraph_of_country(metric_data=usa_metric_data, data_input=usa_category_fig, country_name="USA")
ind_metrics = get_trendgraph_of_country(metric_data=ind_metric_data, data_input=ind_category_fig, country_name="IND")
usa_trending_channel = channels_trending_video(chart_fig=usa_trend_channel, metric_data=usa_trend_analysis_data, country_name="USA")
ind_trending_channel = channels_trending_video(chart_fig=ind_trend_channel, metric_data=ind_trend_analysis_data, country_name="IND")
depth_metrics = depth_analysis_layout(data=depth_analysis_data)

layout = dbc.Container([
    dbc.Row([
        html.Div(children=[
                html.Div(className="home-partion"),
                html.Br(),
                ytb_kpi,
                insights_layout,        
                usa_metrics,
                ind_metrics,
                usa_trending_channel,
                ind_trending_channel,
                correlation_layout,
                depth_metrics
            ], className="graph-container-block"),
            html.Div(children=[
                html.Div(children=[html.Div("Made with"),
                                    html.A("Dash", href="https://dash.plotly.com/", className="link-style"), 
                                    html.Div("- ploty")
                                ], className="footer-msg")]
        )])
    ])
