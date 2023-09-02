from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

def get_metrics_pane(metric_data, country_name):
    metric_right_layout = html.Div([
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
                        html.P("Temp/hr:", className="metric-name"),
                        html.P(datum["temp"], className="metric-value")
                    ],className="metric-2")
                ], className='pane-metrics-splitted')
            ], disable_n_clicks=False, className="rectangle-with-border", id=f"{country_name.lower()}-{datum['title'].lower()}")
                for datum in metric_data]),
    ], className="graph-left-pane")

    return metric_right_layout

def render_graph_pane(data_input, country_name="USA"):
    graph_pane = html.Div([
        html.Div([
            html.Div([
                html.H6(f"{country_name} Top 10 Trending Categories", id="{}-trend-head".format(country_name.lower()), className="trend-head"),
                # TODO: make it interactive
                html.Div(children=[
                        dcc.Graph(figure=data_input, id=f"{country_name.lower()}-vertical-bar-chart")
                ], className="graph-data")
            ], className='rectangle-graph')
        ], className="graph-pane")
    ], className='graph-right-pane')

    return graph_pane

def generate_data_for_trendgraph(df, col_name):
    list_df = list(df[col_name])

    return list_df

def generate_data_for_most_popular(df, col_name):
    list_df = pd.DataFrame(df.groupby([col_name])["video_id"].count().sort_values(ascending=False).reset_index())

    return list_df

def get_trendgraph_of_country(metric_data, data_input, country_name="USA"):
    trend_layout = html.Div([
        html.Div([
            html.Div([
                get_metrics_pane(metric_data=metric_data, country_name=country_name),
                render_graph_pane(data_input=data_input, country_name=country_name)
            ], className="graph-card"),
        ], className="graph-area")
    ], className="country-graph")  # First column with 1/6 width

    return trend_layout

def button_selection(datum, country):
    title = datum["title"]
    id_title = title.replace(" ", "-").lower()
    country = country.lower()

    if title in ["Word Count Analysis", "Hashtag Analysis"]:
        btns = [html.Div(children=[
            html.Button("Title", id=f"{country}-title-{id_title}",className="metric-btn-name"),
                ],className="metric1-trend"),
            html.Div(children=[
                html.Button("Desc", id=f"{country}-desc-{id_title}", className="metric-btn-name"),
            ],className="metric2-trend"),
            html.Div(children=[
                html.Button("Tag", id=f"{country}-tag-{id_title}", className="metric-btn-name"),
            ],className="metric3-trend")
        ]
    else:
        btns = [html.Div(children=[
            html.Button("Day", id=f"{country}-day-{id_title}", className="metric-btn-name"),
                ],className="metric1-trend"),
            html.Div(children=[
                html.Button("Hour", id=f"{country}-hour-{id_title}", className="metric-btn-name"),
            ],className="metric2-trend"),
            html.Div(children=[
                html.Button("Month", id=f"{country}-month-{id_title}", className="metric-btn-name"),
            ],className="metric3-trend")
        ]

    btn_selected = html.Div(children=btns, className='pane-metrics-trend')

    return btn_selected

def prepare_title(datum, country):
    country = country.lower()
    title_block = html.Div(children=[
        html.Div(html.Img(src=datum["img"], className="icon-trend-style"), className="metric-trend-image"),
        html.Div(children=[
            html.Div(datum["title"], id=f"{country}-metric-trend-title", className="metric-trend-title"),
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
                    prepare_title(datum, country_name),
                    button_selection(datum, country_name)], className="rectangle-trend-with-border")
                    for datum in metric_data]),
                ], className="graph-left-pane"),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H6(f"{country_name} Trending Channels", id=f"{country_name.lower()}-channel-trend-head", className="trend-head"),
                            # TODO: make it interactive
                            html.Div(children=[
                                dcc.Graph(figure=chart_fig, id=f"{country_name.lower()}-horizontal-bar-chart")
                            ], className="graph-data")
                        ], className='rectangle-graph')
                    ], className="graph-pane")
                ], className='graph-right-pane')
            ], className="graph-card"),
        ], className="graph-area")
    ], className="country-graph")  # First column with 1/6 width

    return chnl_trend_video

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
                html.Div(children=[
                    html.Div("Depth Analysis", className="depth-title"),
                    html.Button("Collapse", id="depth-collapse-btn", className="depth-expand-btn"),
                ], className="depth-title-box"),
                dbc.Collapse(children=[
                    html.Div(children=[
                        html.Div(children=[
                            html.Div(children=[
                                analysis_header_block(datum),
                                # Head Analysis Block
                                depth_analysis_head_block(),
                                html.Div([
                                    dbc.Row([
                                        dbc.Col(html.Div(children=[dat["title"]], className="analysis-name-value")),
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
                ], id="depth-text-id", className="depth-text-container", is_open=False),
            ], id="depth-box-id", className="depth-box")
        ], className="depth-content")
    ], className="depth-container")  

    return rwt