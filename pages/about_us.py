import dash
from dash import html, dcc

dash.register_page(__name__,
                   path='/about',
                   title='About',
                   name='Our About Page'
                   )

layout = html.Div(children=[
    html.H1(children='This is our About page'),

    html.Div(children='''
        This is our About page content.
    '''),

])