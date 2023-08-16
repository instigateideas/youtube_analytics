from dash import html, dcc

def get_trendgraph_of_country(chart_fig, metric_data, country_name="USA"):
    trend_layout = html.Div([
        html.Div([
            html.Div([
                html.Div([
                html.Div([
                    html.Div(children=[
                        html.Div(children=[
                                html.Div(html.Img(src=datum["img"], className="icon-style"), className="metric-image"),
                                html.Div(datum["title"], className="metric-title")
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
                            html.H6(f"{country_name} Trend Analysis - Top 5", className="trend-head"),
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
