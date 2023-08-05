from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash


external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, use_pages=True, external_stylesheets=external_stylesheets)

YOUTUBE_LOGO = 'https://w7.pngwing.com/pngs/208/269/png-transparent-youtube-play-button-computer-icons-youtube-youtube-logo-angle-rectangle-logo.png'

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=YOUTUBE_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://youtube.com",
                style={"textDecoration": "none"},
            )
        ]
    ),
    color="dark",
    dark=True,
)




app.layout = html.Div([
	html.H1('Multi-page app with Dash Pages'),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

	dash.page_container
])

if __name__ == '__main__':
	app.run(debug=True)