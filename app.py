from dash import Dash, html, dcc, Input, Output
from flask import Flask
import dash_bootstrap_components as dbc
import dash

# Pages
from pages import home
from pages import about_us
from pages import archieve

YOUTUBE_LOGO = '/assets/img/youtube-logo.png'
BASE_URL = 'youtube_analytics'


external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, 
	   #use_pages=True,
       server=Flask(__name__),
	   meta_tags=[{"name": "viewport", "content": "width=device-width"}],
	   suppress_callback_exceptions=True,
       external_stylesheets=external_stylesheets)
server = Flask = app.server

# Register Pages
# dash.register_page(__name__, path='/home', title='Home',name='Our Home Page')
# dash.register_page(__name__, path='/about', title='About', name='Our About Page')
# dash.register_page(__name__, path='/archieve', title='Archieve', name='Our Archieve Page')

navbar = dbc.Navbar(
    dbc.Container(
        [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=YOUTUBE_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("YouTube Analytics Dashoard", className="ms-2")),
                ],
                align="center",
                className="g-0",
            ),
            href="https://youtube.com",
            style={"textDecoration": "none"},
        ),
        html.Div([
            dbc.NavItem(dbc.NavLink('Home', href=f"/{BASE_URL}/home")),
            dbc.NavItem(dbc.NavLink('Abstract', href=f"/{BASE_URL}/archieve")),
            dbc.NavItem(dbc.NavLink('Contact', href=f"/{BASE_URL}/about")),
            dbc.DropdownMenu(children=[
                dbc.DropdownMenuItem("Last 30 days", href="#"),
                dbc.DropdownMenuItem("Last 15 days", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="Last 90 days",
        )], className='nav-items-container'),
		]
    ),
    color="#1c2039",
    dark=True,
    class_name="nav-container"
)

# App Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
	navbar,
	html.Div(id='page-content', children=[]), 
])


@app.callback(Output('page-content', 'children'),
        [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == f'/{BASE_URL}':
        return home.layout
    if pathname == f'/{BASE_URL}/home':
        return home.layout
    if pathname == f'/{BASE_URL}/archieve':
        return archieve.layout
    if pathname == f'/{BASE_URL}/about':
        return about_us.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
	app.run(debug=True)