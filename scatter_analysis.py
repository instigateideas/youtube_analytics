import plotly.graph_objs as go
from dash import html, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc

def get_btns_layout_scatter_plots():
    btns = html.Div(children=[html.Div(children=[
        html.Button("Views Chart", id="btn-scatter-usa-chart", className="scatter-metric-btn-name", disabled=False),
            ],className="scatter-metric1-trend"),
        html.Div(children=[
            html.Button("Likes Chart", id="btn-scatter-ind-chart", className="scatter-metric-btn-name", disabled=False),
        ],className="scatter-metric2-trend")
    ], className="scatter-btns")

    return btns


def get_scatter_analysis_layout():
    rwt = html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                    html.Div(children=[
                        html.Div("Scatter Plot Analysis", className="scatter-title"),
                        html.Button("Collapse", id="scatter-collapse-btn", className="scatter-expand-btn"),
                    ], className="scatter-title-box"),
                    dbc.Collapse([
                        get_btns_layout_scatter_plots(),
                        html.Div(children=[
                            html.Div(children=[
                                    dcc.Graph(id='scatter-heatmap', className="scatter-graph"),
                                ], className='scatter-graph-content')
                            ], className="scatter-analysis-container", \
                                id="scatter-analysis-container-id", style={'display': 'block'})
                    ], id="scatter-text-id", className="scatter-text-container", is_open=False)
            ], id='scatter-box-id', className="scatter-box"),
        ], className="scatter-content")
    ], className="scatter-container")  

    return rwt