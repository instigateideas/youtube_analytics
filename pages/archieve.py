import dash
from dash import html, dcc

dash.register_page(__name__,
                   path='/archieve',
                   title='Archieve',
                   name='Our Archieve Page'
                   )

layout = html.Div(children=[
    html.H1(children='This is our Archive page'),

    html.Div(children='''
        This is our Archive page content.
    '''),

])