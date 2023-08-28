import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import html, dcc, Input, Output
from app import app

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
def get_category_graph_image(df, x, y):
    fig = go.Figure(
        data=[
            go.Bar(x=df[x], y=df[y])
        ],
        layout= graph_layout
    )

    return fig

# Create a bar chart with a dark theme
def get_channel_graph_image(df, x, y):
    fig = go.Figure(
        data=[
            go.Bar(x=y, y=x, orientation='h')
        ],
        layout= graph_layout
    )

    return fig

def get_categorory_trending_graph(df, top=None):
    if top == None:
        category_data = pd.DataFrame(df.groupby(["snippet/title"])["video_id"].count().sort_values(ascending=False).reset_index())
    else:
        category_data = pd.DataFrame(df.groupby(["snippet/title"])["video_id"].count().sort_values(ascending=False).reset_index())[0:top]

    # graph
    graph_fig = get_category_graph_image(category_data, 'snippet/title', 'video_id')
    
    return graph_fig

def get_trending_channels_graph(df, top=None, length_cut=20):
    if top == None:
        channel_data = pd.DataFrame(df.groupby(["channel_title"])["video_id"].count().reset_index().sort_values(by="video_id",ascending=False))
    else:
        channel_data = pd.DataFrame(df.groupby(["channel_title"])["video_id"].count().reset_index().sort_values(by="video_id",ascending=False))[0:top]

    # Sort the data in descending order
    sorted_indices = sorted(list(channel_data.index), key=lambda k: channel_data['video_id'][k], reverse=False)
    sorted_categories = [channel_data['channel_title'][i][0:length_cut] for i in sorted_indices]
    sorted_values = [channel_data['video_id'][i] for i in sorted_indices]

    # graph
    graph_fig = get_channel_graph_image(channel_data, sorted_categories, sorted_values)
    
    return graph_fig

def get_vertical_graph(x, y):
    fig = go.Figure(
        data=[
            go.Bar(x=x, y=y)
        ],
        layout= graph_layout
    )

    return fig
