import dash
from dash import html, dcc


layout = html.Div(children=[
    html.H1(children='This is our About page'),

    html.Div(children='''
        This is our About page content.
    '''),

])