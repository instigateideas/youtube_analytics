from dash import Dash, html, dcc, Input, Output, State
from flask import Flask
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import dash
import base64
import os

# Pages
from pages import home
from pages import about_us
from pages import archieve

# Data & other analysis
from load_data import clean_and_load_data, save_words_in_excel, get_word_count_analysis
from correlation_analysis import get_heatmap_figure
from pages.trend_chart import generate_data_for_trendgraph, generate_data_for_most_popular
from misc_analysis import save_hastags_in_excel, get_hastag_analysis


YOUTUBE_LOGO = '/assets/img/youtube-logo.png'
BASE_URL = 'youtube_analytics'

cwd = os.getcwd()
IMG_DIR = os.path.join(cwd, "assets", "img")

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, 
	   #use_pages=True,
       server=Flask(__name__),
	   meta_tags=[{"name": "viewport", "content": "width=device-width"}],
	   suppress_callback_exceptions=True,
       serve_locally=True,
       external_stylesheets=external_stylesheets)
server = Flask = app.server


# Load data
cleaned_usa_df, cleaned_ind_df = clean_and_load_data()

# # Prepare the Wordcloud
# usa_title_wc = save_words_in_excel(df=cleaned_usa_df, col_name='title', country="usa")
# usa_desc_wc = save_words_in_excel(df=cleaned_usa_df, col_name='description', country="usa")
# usa_tags_wc = save_words_in_excel(df=cleaned_usa_df, col_name='tags', country="usa")
# ind_title_wc = save_words_in_excel(df=cleaned_ind_df, col_name='title', country="ind")
# ind_desc_wc = save_words_in_excel(df=cleaned_ind_df, col_name='description', country="ind")
# ind_tags_wc = save_words_in_excel(df=cleaned_ind_df, col_name='tags', country="ind")

# # Prepare the Hastags
# usa_title_ht = save_hastags_in_excel(df=cleaned_usa_df, col_name='title', country="usa")
# usa_desc_ht = save_hastags_in_excel(df=cleaned_usa_df, col_name='description', country="usa")
# usa_tags_ht = save_hastags_in_excel(df=cleaned_usa_df, col_name='tags', country="usa")
# ind_title_ht = save_hastags_in_excel(df=cleaned_ind_df, col_name='title', country="ind")
# ind_desc_ht = save_hastags_in_excel(df=cleaned_ind_df, col_name='description', country="ind")
# ind_tags_ht = save_hastags_in_excel(df=cleaned_ind_df, col_name='tags', country="ind")

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

# Callbacks for Home Page
@app.callback(
    Output("correlation-heatmap", "figure"),  # Output component: the graph
    Input("btn-corr-usa-chart", "n_clicks"),  # Input component: button 1
    Input("btn-corr-ind-chart", "n_clicks")  # Input component: button 2
)
def update_chart(button1_clicks, button2_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "btn-corr-usa-chart":
        updated_fig = get_heatmap_figure(df=cleaned_usa_df, country="USA")  # Replace with your data generation logic
    elif trigger_id == "btn-corr-ind-chart":
        updated_fig = get_heatmap_figure(df=cleaned_ind_df, country="IND")  # Replace with your data generation logic
    else:
        updated_fig = [] # Handle other cases if needed

    return updated_fig

@app.callback(
    Output('corr-analysis-container-id', 'style'),
    Output('wordcloud-analysis-container-id', 'style'),
    Output('my-toggle-switch-output', 'children'),
    [Output("btn-corr-usa-chart",'disabled'), Output("btn-corr-ind-chart",'disabled'), \
    Output("btn-wc-title-usa-chart",'disabled'), Output("btn-wc-title-ind-chart",'disabled'), \
    Output("btn-wc-desc-usa-chart",'disabled'), Output("btn-wc-desc-ind-chart",'disabled'), \
    Output("btn-wc-tag-usa-chart",'disabled'),Output("btn-wc-tag-ind-chart",'disabled')],
    Input('my-toggle-switch', 'value'),
    [Input("btn-corr-usa-chart",'disabled'),Input("btn-corr-ind-chart",'disabled'), \
      Input("btn-wc-title-usa-chart",'disabled'), Input("btn-wc-title-ind-chart",'disabled'), \
      Input("btn-wc-desc-usa-chart",'disabled'),Input("btn-wc-desc-ind-chart",'disabled'), \
      Input("btn-wc-tag-usa-chart",'disabled'), Input("btn-wc-tag-ind-chart",'disabled')],
    [State('corr-analysis-container-id', 'style'), State('wordcloud-analysis-container-id', 'style')]
)
def update_output(value, usa_corr_btn, ind_corr_btn, usa_wc_btn_title, ind_wc_btn_title, \
                  usa_wc_btn_desc, ind_wc_btn_desc, usa_wc_btn_tags, ind_wc_btn_tags, \
                  graph_style, image_style):
    if value == True:
        usa_corr_btn = True
        ind_corr_btn= True
        usa_wc_btn_title= False
        ind_wc_btn_title= False
        usa_wc_btn_desc= False
        ind_wc_btn_desc= False
        usa_wc_btn_tags= False
        ind_wc_btn_tags= False
        analysis = "Word Cloud Analysis"
        new_graph_style = {'display': 'none'}
        new_image_style = {'display': 'block'}
        return new_graph_style, new_image_style, analysis, usa_corr_btn, ind_corr_btn, usa_wc_btn_title, ind_wc_btn_title, usa_wc_btn_desc, ind_wc_btn_desc, usa_wc_btn_tags, ind_wc_btn_tags
    else:
        analysis = "Correlation Analysis"
        if graph_style.get('display') == 'none':
            usa_corr_btn = False
            ind_corr_btn= False
            usa_wc_btn_title= True
            ind_wc_btn_title= True
            usa_wc_btn_desc= True
            ind_wc_btn_desc= True
            usa_wc_btn_tags= True
            ind_wc_btn_tags= True
            new_graph_style = {'display': 'block'}
            new_image_style = {'display': 'none'}
            return new_graph_style, new_image_style, analysis, usa_corr_btn, ind_corr_btn, usa_wc_btn_title, ind_wc_btn_title, usa_wc_btn_desc, ind_wc_btn_desc, usa_wc_btn_tags, ind_wc_btn_tags
        else:
            return graph_style, image_style, analysis, usa_corr_btn, ind_corr_btn, usa_wc_btn_title, ind_wc_btn_title, usa_wc_btn_desc, ind_wc_btn_desc, usa_wc_btn_tags, ind_wc_btn_tags

# Word Cloud Analysis
@app.callback(
    Output('wordcloud-image-id', 'src'),
    Input('btn-wc-title-usa-chart', 'n_clicks'),
    Input('btn-wc-title-ind-chart', 'n_clicks'),
    Input('btn-wc-desc-usa-chart', 'n_clicks'),
    Input('btn-wc-desc-ind-chart', 'n_clicks'),
    Input('btn-wc-tag-usa-chart', 'n_clicks'),
    Input('btn-wc-tag-ind-chart', 'n_clicks'),
    State('wordcloud-image-id', 'value'),
)
def update_img_src_wc(btn1, btn2, btn3, btn4, btn5, btn6, img_src):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "btn-wc-title-usa-chart":
        img_src = "/assets/img/usa-wc-title.png"
    elif trigger_id == "btn-wc-title-ind-chart":
        img_src = "/assets/img/ind-wc-title.png"
    elif trigger_id == "btn-wc-desc-usa-chart":
        img_src = "/assets/img/usa-wc-description.png"
    elif trigger_id == "btn-wc-desc-ind-chart":
        img_src = "/assets/img/ind-wc-description.png"
    elif trigger_id == "btn-wc-tag-usa-chart":
        img_src = "/assets/img/usa-wc-tags.png"
    elif trigger_id == "btn-wc-tag-ind-chart":
        img_src = "/assets/img/ind-wc-tags.png"
    else:
        img_src = "/assets/img/usa-wc-title.png"    

    return img_src

# Trendgraph of country
hist_graph_layout = go.Layout(
        # title='Dark Theme Bar Chart',
        paper_bgcolor='#262b49',  # Set background color to transparent
        plot_bgcolor='#262b49',   # Set plot area background color to transparent
        font=dict(color='white'),       # Set font color to white
        xaxis=dict(showgrid=False),     # Turn off x-axis grid lines
        yaxis=dict(type='log', showgrid=False),     # Turn off y-axis grid lines
        #margin=dict(t=60, b=30, l=10, r=10)  # Adjust margins for title and labels
)

def get_histograms(data, n_bins=15):
    fig = go.Figure(
        data=[go.Histogram(x=data, nbinsx=n_bins)],
        layout=hist_graph_layout
    )

    return fig

@app.callback(
    Output("usa-vertical-bar-chart", "figure"),  # Output component: the graph
    Output("usa-trend-head", "children"),
    Input("usa-views", "n_clicks"), # Input component: div 1
    Input("usa-likes", "n_clicks"), # Input component: div 2
    Input("usa-comments", "n_clicks"), # Input component: div 3
    Input("usa-dislike", "n_clicks"), # Input component: div 4
)
def usa_update_chart(div1_clicks, div2_clicks, div3_clicks, div4_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "usa-views":
        analysis = "Views"
        updated_data = generate_data_for_trendgraph(df=cleaned_usa_df, col_name="views")  # Replace with your data generation logic
    elif trigger_id == "usa-likes":
        analysis = "Likes"
        updated_data = generate_data_for_trendgraph(df=cleaned_usa_df, col_name="likes")  # Replace with your data generation logic
    elif trigger_id == "usa-comments":
        analysis = "Comments"
        updated_data = generate_data_for_trendgraph(df=cleaned_usa_df, col_name="comment_count")  # Replace with your data generation logic
    elif trigger_id == "usa-dislikes":
        analysis = "Dislikes"
        updated_data = generate_data_for_trendgraph(df=cleaned_usa_df, col_name="dislikes")  # Replace with your data generation logic
    else:
        analysis = ""
        updated_data = []  # Handle other cases if needed

    chart_title = "USA - Trending {} Analysis".format(analysis)
    updated_chart = get_histograms(data=updated_data)  # Replace with your chart update logic

    return updated_chart, chart_title

@app.callback(
    Output("ind-vertical-bar-chart", "figure"),  # Output component: the graph
    Output("ind-trend-head", "children"),
    Input("ind-views", "n_clicks"), # Input component: div 1
    Input("ind-likes", "n_clicks"), # Input component: div 2
    Input("ind-comments", "n_clicks"), # Input component: div 3
    Input("ind-dislike", "n_clicks"), # Input component: div 4
)
def ind_update_chart(div1_clicks, div2_clicks, div3_clicks, div4_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "ind-views":
        analysis = "Views"
        updated_data = generate_data_for_trendgraph(df=cleaned_ind_df, col_name="views")  # Replace with your data generation logic
    elif trigger_id == "ind-likes":
        analysis = "Likes"
        updated_data = generate_data_for_trendgraph(df=cleaned_ind_df, col_name="likes")  # Replace with your data generation logic
    elif trigger_id == "ind-comments":
        analysis = "Comments"
        updated_data = generate_data_for_trendgraph(df=cleaned_ind_df, col_name="comment_count")  # Replace with your data generation logic
    elif trigger_id == "ind-dislikes":
        analysis = "Dislikes"
        updated_data = generate_data_for_trendgraph(df=cleaned_ind_df, col_name="dislikes")  # Replace with your data generation logic
    else:
        analysis = ""
        updated_data = []  # Handle other cases if needed

    chart_title = "IND - Trending {} Analysis".format(analysis)
    updated_chart = get_histograms(data=updated_data)  # Replace with your chart update logic

    return updated_chart, chart_title

# Most Popular analysis
bar_graph_layout = go.Layout(
        # title='Dark Theme Bar Chart',
        paper_bgcolor='#262b49',  # Set background color to transparent
        plot_bgcolor='#262b49',   # Set plot area background color to transparent
        font=dict(color='white'),       # Set font color to white
        xaxis=dict(showgrid=False),     # Turn off x-axis grid lines
        yaxis=dict(showgrid=False),     # Turn off y-axis grid lines
        #margin=dict(t=60, b=30, l=10, r=10)  # Adjust margins for title and labels
)

wordcloud_layout = go.Layout(
        # title='Dark Theme Bar Chart',
        paper_bgcolor='#262b49',  # Set background color to transparent
        plot_bgcolor='#262b49',   # Set plot area background color to transparent
        font=dict(color='white'),       # Set font color to white
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        #margin=dict(t=60, b=30, l=10, r=10)  # Adjust margins for title and labels
)

# Create a bar chart with a dark theme
def get_category_graph_image(df, x, y):
    fig = go.Figure(
        data=[
            go.Bar(x=df[x], y=df[y])
        ],
        layout= bar_graph_layout
    )

    return fig

@app.callback(
    Output("usa-horizontal-bar-chart", "figure"),  # Output component: the graph
    Output("usa-channel-trend-head", "children"),
    Input("usa-day-most-popular-publish", "n_clicks"), # Input component: div 1
    Input("usa-hour-most-popular-publish", "n_clicks"), # Input component: div 2
    Input("usa-month-most-popular-publish", "n_clicks"), # Input component: div 3
    Input("usa-day-most-popular-trending", "n_clicks"), # Input component: div 4
    Input("usa-hour-most-popular-trending", "n_clicks"), # Input component: div 5
    Input("usa-month-most-popular-trending", "n_clicks"), # Input component: div 6
    Input("usa-title-word-count-analysis", "n_clicks"),
    Input("usa-desc-word-count-analysis", "n_clicks"),
    Input("usa-tag-word-count-analysis", "n_clicks"),
    Input("usa-title-hashtag-analysis", "n_clicks"),
    Input("usa-desc-hashtag-analysis", "n_clicks"),
    Input("usa-tag-hashtag-analysis", "n_clicks"),
)
def usa_channel_update_chart(div1_clicks, div2_clicks, div3_clicks, \
                             div4_clicks, div5_clicks, div6_clicks, \
                             div7_clicks, div8_clicks, div9_clicks, \
                             div10_clicks, div11_clicks, div12_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "usa-day-most-popular-publish":
        analysis = "Publish Day"
        x_dat = "publish_weekday"
        updated_data = generate_data_for_most_popular(df=cleaned_usa_df, col_name=x_dat)  # Replace with your data generation logic
    elif trigger_id == "usa-hour-most-popular-publish":
        analysis = "Publish Hour"
        x_dat = "publish_hour"
        updated_data = generate_data_for_most_popular(df=cleaned_usa_df, col_name=x_dat)  # Replace with your data generation logic
    elif trigger_id == "usa-month-most-popular-publish":
        analysis = "Publish Month"
        x_dat = "publish_month"
        updated_data = generate_data_for_most_popular(df=cleaned_usa_df, col_name=x_dat)  # Replace with your data generation logic
    elif trigger_id == "usa-day-most-popular-trending":
        analysis = "Trending Day"
        x_dat = "trending_weekday"
        updated_data = generate_data_for_most_popular(df=cleaned_usa_df, col_name=x_dat)  # Replace with your data generation logic
    elif trigger_id == "usa-hour-most-popular-trending":
        analysis = "Trending Hour"
        x_dat = "trending_hour"
        updated_data = generate_data_for_most_popular(df=cleaned_usa_df, col_name=x_dat)  # Replace with your data generation logic
    elif trigger_id == "usa-month-most-popular-trending":
        analysis = "Trending Month"
        x_dat = "trending_month"
        updated_data = generate_data_for_most_popular(df=cleaned_usa_df, col_name=x_dat)  # Replace with your data generation logic
    elif trigger_id == "usa-title-word-count-analysis":
        analysis = "Word Title"
        x_dat = "words"
        updated_data = get_word_count_analysis(col_name='title', country='usa', top=10)  # Replace with your data generation logic
    elif trigger_id == "usa-desc-word-count-analysis":
        analysis = "Word Description"
        x_dat = "words"
        updated_data = get_word_count_analysis(col_name='description', country='usa', top=10)  # Replace with your data generation logic
    elif trigger_id == "usa-tag-word-count-analysis":
        analysis = "Word Tags"
        x_dat = "words"
        updated_data = get_word_count_analysis(col_name='tags', country='usa', top=10)  # Replace with your data generation logic
    elif trigger_id == "usa-title-hashtag-analysis":
        analysis = "HashTag in Title"
        x_dat = "hashtag"
        updated_data = get_hastag_analysis(col_name='title', country='usa', top=10)  # Replace with your data generation logic
    elif trigger_id == "usa-desc-hashtag-analysis":
        analysis = "HashTag in Description"
        x_dat = "hashtag"
        updated_data = get_hastag_analysis(col_name='description', country='usa', top=10)  # Replace with your data generation logic
    elif trigger_id == "usa-tag-hashtag-analysis":
        analysis = "HashTag in Tags"
        x_dat = "hashtag"
        updated_data = get_hastag_analysis(col_name='tags', country='usa', top=10)  # Replace with your data generation logic
    else:
        analysis = ""
        updated_data = []  # Handle other cases if needed

    # Render the chart
    if "Word" in analysis.split(" "):
        chart_title = "USA - {} Analysis".format(analysis)
        updated_chart = get_category_graph_image(df=updated_data, x=x_dat, y='count')
    elif "HashTag" in analysis.split(" "):
        chart_title = "USA - Most Popular {}".format(analysis)
        updated_chart = get_category_graph_image(df=updated_data, x=x_dat, y='count')
    else:
        chart_title = "USA - Most Popular {} Analysis".format(analysis)
        updated_chart = get_category_graph_image(df=updated_data, x=x_dat, y='video_id')

    return updated_chart, chart_title


@app.callback(
    Output("ind-horizontal-bar-chart", "figure"),  # Output component: the graph
    Output("ind-channel-trend-head", "children"),
    Input("ind-day-most-popular-publish", "n_clicks"), # Input component: div 1
    Input("ind-hour-most-popular-publish", "n_clicks"), # Input component: div 2
    Input("ind-month-most-popular-publish", "n_clicks"), # Input component: div 3
    Input("ind-day-most-popular-trending", "n_clicks"), # Input component: div 4
    Input("ind-hour-most-popular-trending", "n_clicks"), # Input component: div 5
    Input("ind-month-most-popular-trending", "n_clicks"), # Input component: div 6
    Input("ind-title-word-count-analysis", "n_clicks"),
    Input("ind-desc-word-count-analysis", "n_clicks"),
    Input("ind-tag-word-count-analysis", "n_clicks"),
    Input("ind-title-hashtag-analysis", "n_clicks"),
    Input("ind-desc-hashtag-analysis", "n_clicks"),
    Input("ind-tag-hashtag-analysis", "n_clicks"),
)
def ind_channel_update_chart(div1_clicks, div2_clicks, div3_clicks, \
                             div4_clicks, div5_clicks, div6_clicks, \
                             div7_clicks, div8_clicks, div9_clicks, \
                             div10_clicks, div11_clicks, div12_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "ind-day-most-popular-publish":
        analysis = "Publish Day"
        x_dat = "publish_weekday"
        updated_data = generate_data_for_most_popular(df=cleaned_ind_df, col_name=x_dat)  # Replace with your data generation logic
    elif trigger_id == "ind-hour-most-popular-publish":
        analysis = "Publish Hour"
        x_dat = "publish_hour"
        updated_data = generate_data_for_most_popular(df=cleaned_ind_df, col_name=x_dat)  # Replace with your data generation logic
    elif trigger_id == "ind-month-most-popular-publish":
        analysis = "Publish Month"
        x_dat = "publish_month"
        updated_data = generate_data_for_most_popular(df=cleaned_ind_df, col_name=x_dat)  # Replace with your data generation logic
    elif trigger_id == "ind-day-most-popular-trending":
        analysis = "Trending Day"
        x_dat = "trending_weekday"
        updated_data = generate_data_for_most_popular(df=cleaned_ind_df, col_name=x_dat)  # Replace with your data generation logic
    elif trigger_id == "ind-hour-most-popular-trending":
        analysis = "Trending Hour"
        x_dat = "trending_hour"
        updated_data = generate_data_for_most_popular(df=cleaned_ind_df, col_name=x_dat)  # Replace with your data generation logic
    elif trigger_id == "ind-month-most-popular-trending":
        analysis = "Trending Month"
        x_dat = "trending_month"
        updated_data = generate_data_for_most_popular(df=cleaned_ind_df, col_name=x_dat)  # Replace with your data generation logic
    elif trigger_id == "ind-title-word-count-analysis":
        analysis = "Word Title"
        x_dat = "words"
        updated_data = get_word_count_analysis(col_name='title', country='ind', top=10)  # Replace with your data generation logic
    elif trigger_id == "ind-desc-word-count-analysis":
        analysis = "Word Description"
        x_dat = "words"
        updated_data = get_word_count_analysis(col_name='description', country='ind', top=10)  # Replace with your data generation logic
    elif trigger_id == "ind-tag-word-count-analysis":
        analysis = "Word Tags"
        x_dat = "words"
        updated_data = get_word_count_analysis(col_name='tags', country='ind', top=10)  # Replace with your data generation logic
    elif trigger_id == "ind-title-hashtag-analysis":
        analysis = "HashTag in Title"
        x_dat = "hashtag"
        updated_data = get_hastag_analysis(col_name='title', country='ind', top=10)  # Replace with your data generation logic
    elif trigger_id == "ind-desc-hashtag-analysis":
        analysis = "HashTag in Description"
        x_dat = "hashtag"
        updated_data = get_hastag_analysis(col_name='description', country='ind', top=10)  # Replace with your data generation logic
    elif trigger_id == "ind-tag-hashtag-analysis":
        analysis = "HashTag in Tags"
        x_dat = "hashtag"
        updated_data = get_hastag_analysis(col_name='tags', country='ind', top=10)  # Replace with your data generation logic
    else:
        analysis = ""
        updated_data = []  # Handle other cases if needed

    # Render the chart
    if "Word" in analysis.split(" "):
        chart_title = "IND - {} Analysis".format(analysis)
        updated_chart = get_category_graph_image(df=updated_data, x=x_dat, y='count')
    elif "HashTag" in analysis.split(" "):
        chart_title = "IND - Most Popular {}".format(analysis)
        updated_chart = get_category_graph_image(df=updated_data, x=x_dat, y='count')
    else:
        chart_title = "IND - Most Popular {} Analysis".format(analysis)
        updated_chart = get_category_graph_image(df=updated_data, x=x_dat, y='video_id')

    return updated_chart, chart_title

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