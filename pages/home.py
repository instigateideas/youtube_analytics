import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
from .trend_chart import get_trendgraph_of_country
from .agg_metrics import get_aggregated_metrics

# Sample data for the bar chart
data = {
    'Category': ['A', 'B', 'C', 'D'],
    'Values': [10, 15, 7, 12]
}

usa_metric_data = [
    {"img": "/assets/img/engagement.png", "title": "Audience Engagement Rate", "avg": "70%", "temp": "20%"},
    {"img": "/assets/img/likes.png", "title": "Likes", "avg": "50%", "temp": "70%"},
    {"img": "/assets/img/comment.png", "title": "Comments", "avg": "50%", "temp": "40%"},
    {"img": "/assets/img/dislike.png", "title": "Dislike", "avg": "10%", "temp": "20%"},
]


ind_metric_data = [
    {"img": "/assets/img/engagement.png", "title": "Audience Engagement Rate", "avg": "75%", "temp": "20%"},
    {"img": "/assets/img/likes.png", "title": "Likes", "avg": "60%", "temp": "20%"},
    {"img": "/assets/img/comment.png", "title": "Comments", "avg": "40%", "temp": "20%"},
    {"img": "/assets/img/dislike.png", "title": "Dislike", "avg": "30%", "temp": "20%"},
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

ytb_kpi = get_aggregated_metrics()
usa_metrics = get_trendgraph_of_country(chart_fig=fig, metric_data=usa_metric_data, country_name="USA")
ind_metrics = get_trendgraph_of_country(chart_fig=fig, metric_data=ind_metric_data, country_name="IND")


layout = dbc.Container([
    dbc.Row([
        html.Div(children=[
            html.Div(className="home-partion"),
            html.Br(),
            ytb_kpi,         
            usa_metrics,
            ind_metrics
            ], className="graph-container-block"),
            html.Div(children=[
                html.H4("Home Page")]
        )])
    ])
