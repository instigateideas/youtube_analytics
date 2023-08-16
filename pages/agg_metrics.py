from dash import html, dcc
import dash_bootstrap_components as dbc

no_of_kpi = 6

agg_data = [
    {"img": "/assets/img/channel-icon.png", "name": "No. of Youtube Channels", "value": "10223"},
    {"img": "/assets/img/trending-video.png", "name": "No. of Trending Videos", "value": "10223"},
    {"img": "/assets/img/social-engagement.png", "name": "No. of Total Engagements", "value": "2345"},
    {"img": "/assets/img/engagement-per-video.png", "name": "Avg. Engagement/ video", "value": "124"},
    {"img": "/assets/img/publish-rate.png", "name": "Avg. Content Publishing Rate/ Day", "value": "30%"},
    {"img": "/assets/img/avg-trending.png", "name": "Avg. Rate Video Trends", "value": "45%"}
]

def get_aggregated_metrics():
    agg_metrics = html.Div(children=[
        dbc.Row(
            [
            dbc.Col(html.Div(children=[
                html.Div(children=[
                    html.Div(html.Img(src=kpi_datum["img"], className="kpi-img"), className="kpi-logo"),
                    html.Div(children=[
                        html.Div(kpi_datum["name"], className="kpi-name"),
                        html.Div(children=[
                            html.Div(children=[
                                html.Div(html.Img(src='/assets/img/usa-flag.png'), className="country-flag"),
                                html.Div(kpi_datum["value"])
                            ], className="usa-flag-kpi-value"),
                            html.Div(children=[
                                # html.Div(html.Img()),
                                html.Div(kpi_datum["value"])
                            ], className="ind-flag-kpi-value"),
                        ], className="kpi-value")
                    ], className="kpi-metric"),
                ], className="kpi-card"),
                                       
            ]), width=4, lg=2)
            for kpi_datum in agg_data]
        ),

    ], className="agg-container")

    return agg_metrics
