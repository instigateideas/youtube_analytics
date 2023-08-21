from dash import html, dcc
import dash_bootstrap_components as dbc

no_of_kpi = 6

def get_aggregated_metrics(kpi_data):
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
                                html.Div(html.Img(src='/assets/img/usa-flag.png', className="country-flag")),
                                html.Div(kpi_datum["usa_value"])
                            ], className="usa-flag-kpi-value"),
                            html.Div(children=[
                                html.Div(html.Img(src='/assets/img/india-flag.png', className="country-flag")),
                                html.Div(kpi_datum["ind_value"])
                            ], className="ind-flag-kpi-value"),
                        ], className="kpi-value")
                    ], className="kpi-metric"),
                ], className="kpi-card"),
                                       
            ]), width=4, lg=2)
            for kpi_datum in kpi_data]
        ),

    ], className="agg-container")

    return agg_metrics
