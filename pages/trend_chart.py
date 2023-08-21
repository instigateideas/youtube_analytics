from dash import html, dcc
import dash_bootstrap_components as dbc

def get_trendgraph_of_country(chart_fig, metric_data, country_name="USA"):
    trend_layout = html.Div([
        html.Div([
            html.Div([
                html.Div([
                html.Div([
                    html.Div(children=[
                        html.Div(children=[
                                html.Div(html.Img(src=datum["img"], className="icon-style"), className="metric-image"),
                                html.Div(children=[
                                    html.Div(datum["title"], className="metric-title"),
                                    html.Div(datum["value"], className="metric-val")
                                ], className="metric-sub-title")
                            ], className='pane-head'),
                        html.Div(children=[
                            html.Div(children=[
                                html.P("Avg:", className="metric-name"),
                                html.P("", className="metric-space"),
                                html.P(datum["avg"], className="metric-value")
                            ],className="metric-1"),
                            html.Div(children=[
                                html.P("Temp:", className="metric-name"),
                                html.P(datum["temp"], className="metric-value")
                            ],className="metric-2")
                        ], className='pane-metrics-splitted')
                    ], className="rectangle-with-border")
                        for datum in metric_data]),
                ], className="graph-left-pane"),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H6(f"{country_name} Top 5 Trending Categories", className="trend-head"),
                            html.Div(children=[
                                dcc.Graph(figure=chart_fig)
                            ], className="graph-data")
                        ], className='rectangle-graph')
                    ], className="graph-pane")
                ], className='graph-right-pane')
            ], className="graph-card"),
        ], className="graph-area")
    ], className="country-graph")  # First column with 1/6 width

    return trend_layout

def button_selection(datum):
    title = datum["title"]

    if title in ["Word Cloud Analysis", "Hashtag Analysis"]:
        btns = [html.Div(children=[
            html.Button("Title", className="metric-btn-name"),
                ],className="metric1-trend"),
            html.Div(children=[
                html.Button("Desc", className="metric-btn-name"),
            ],className="metric2-trend"),
            html.Div(children=[
                html.Button("Tag", className="metric-btn-name"),
            ],className="metric3-trend")
        ]
    else:
        btns = [html.Div(children=[
            html.Button("Day", className="metric-btn-name"),
                ],className="metric1-trend"),
            html.Div(children=[
                html.Button("Hour", className="metric-btn-name"),
            ],className="metric2-trend")
        ]

    btn_selected = html.Div(children=btns, className='pane-metrics-trend')

    return btn_selected

def prepare_title(datum):
    title_block = html.Div(children=[
        html.Div(html.Img(src=datum["img"], className="icon-trend-style"), className="metric-trend-image"),
        html.Div(children=[
            html.Div(datum["title"], className="metric-trend-title"),
            ], className="metric-sub-title")
        ], className='pane-head-trend')

    return title_block

def channels_trending_video(chart_fig, metric_data, country_name="USA"):
    # No. of Video's Trending Vs Channels
    chnl_trend_video = html.Div([
        html.Div([
            html.Div([
                html.Div([
                # looper
                html.Div([
                    html.Div(children=[
                    prepare_title(datum),
                    button_selection(datum)], className="rectangle-with-border")
                    for datum in metric_data]),
                ], className="graph-left-pane"),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H6(f"{country_name} Trending Channels", className="trend-head"),
                            html.Div(children=[
                                dcc.Graph(figure=chart_fig)
                            ], className="graph-data")
                        ], className='rectangle-graph')
                    ], className="graph-pane")
                ], className='graph-right-pane')
            ], className="graph-card"),
        ], className="graph-area")
    ], className="country-graph")  # First column with 1/6 width

    return chnl_trend_video

def correlation_matrix(country):
    pass

def analysis_header_block(datum):
    header_block = html.Div(children=[
        html.Div(html.Img(src=datum["img"], className="analysis-image"), className="analysis-img-pane"),
        html.Div(datum["title"], className="analysis-head")
    ], className="analysis-title-pane")

    return header_block

def depth_analysis_head_block():
    head_block = html.Div(dbc.Row(
        [
            dbc.Col(html.Div("", className="analysis-name")),
            dbc.Col(html.Div(children=[
                html.Img(src="/assets/img/usa-flag.png", className="flag-img-analysis"),
                html.Div("USA - Depth Analysis", className="analysis-market-name")
            ], className="analysis-market-head")),  
            dbc.Col(html.Div(children=[
                html.Img(src="/assets/img/india-flag.png", className="flag-img-analysis"),
                html.Div("IND - Depth Analysis", className="analysis-market-name")
            ], className="analysis-market-head")),
        ],
        align="center",
    ))

    return head_block


def various_analysis_block(datum):
    analysis_block = []

    for dat in datum["analysis"]:
        new_data = dbc.Row([
            dbc.Col(html.Div(dat["title"], className="analysis-name-value")),
            dbc.Col(html.Div(children=[
                html.Div(dat["data_usa"], className="analysis-market-name")
            ], className="analysis-market-value-head")),  
            dbc.Col(html.Div(children=[
                html.Div(dat["data_ind"], className="analysis-market-name")
            ], className="analysis-market-value-head")),
        ], align="center")
        analysis_block.append(new_data)
    
    print(analysis_block)

    return analysis_block
    

def depth_analysis_layout(data):
    rwt = html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div("Depth Analysis", className="depth-title"),
                html.Div(children=[
                    html.Div(children=[
                        html.Div(children=[
                            analysis_header_block(datum),
                            # Head Analysis Block
                            depth_analysis_head_block(),
                            html.Div([
                                dbc.Row([
                                    dbc.Col(html.Div(children=[
                                                    dat["title"]], className="analysis-name-value")),
                                    dbc.Col(html.Div(children=[
                                        html.Div(children=[dat["data_usa"]], className="analysis-market-name")
                                    ], className="analysis-market-value-head")),  
                                    dbc.Col(html.Div(children=[
                                        html.Div(children=[dat["data_ind"]], className="analysis-market-name")
                                    ], className="analysis-market-value-head"))
                                ]
                            , align="center")
                            for dat in datum["analysis"]])
                        ])
                        # various_analysis_block()
                    ], className="depth-analysis-pane")
                for datum in data], className="depth-analysis-container")
            ], className="depth-box")
        ], className="depth-content")
    ], className="depth-container")  

    return rwt