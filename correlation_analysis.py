import plotly.graph_objs as go
from dash import html, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc

# Function to assign color based on correlation value
def get_annotation_color(val):
    if val >= 0.7:
        return 'green'
    elif val <= -0.7:
        return 'red'
    else:
        return 'black'


def get_heatmap_figure(df, country='USA'):
    data = df[['views', 'likes', 'dislikes', 'comment_count', 'num_tags',
                    'tags_length', 'title_length', 'desc_length', 'publish_hour']]
    correlation_matrix = data.corr()

    annotations = []
    for i, row in enumerate(correlation_matrix.values):
        for j, val in enumerate(row):
            annotations.append(
                {
                    "x": correlation_matrix.columns[j],
                    "y": correlation_matrix.index[i],
                    "text": f"{val:.2f}",
                    "showarrow": False,
                    "font": {"color": get_annotation_color(val)}
                }
            )

    corr_fig = go.Figure(
            data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            colorscale='Viridis',  # Choose a colorscale
            hoverongaps=False,  # Prevent displaying annotations for missing values
            showscale=True,  # Hide the color scale
            text=correlation_matrix.round(2).values,  # Display correlation values
            # text_template='%{text:.2f}',  # Use a specific text template for annotation text
            # textfont_color=[get_annotation_color(val) for val in correlation_matrix.values.flat],  # Assign colors based on correlation
        ),
        layout=go.Layout(
            title=f'{country} Correlation Matrix',
            paper_bgcolor='#262b49',  # Set background color to transparent
            plot_bgcolor='#262b49',   # Set plot area background color to transparent
            font=dict(color='white'),       # Set font color to white
            annotations=annotations,
            xaxis=dict(title="Youtube Attributes", showgrid=False),     # Turn off x-axis grid lines
            yaxis=dict(title="Youtube Attributes", showgrid=False),     # Turn off y-axis grid lines

        )
    )

    return corr_fig

def get_btns_layout_of_countries():
    btns = html.Div(children=[html.Div(children=[
        html.Button("USA Correlation Chart", id="btn-corr-usa-chart", className="corr-metric-btn-name", disabled=False),
            ],className="corr-metric1-trend"),
        html.Div(children=[
            html.Button("IND Correlation Chart", id="btn-corr-ind-chart", className="corr-metric-btn-name", disabled=False),
        ],className="corr-metric2-trend"),
        html.Div(children=[
            html.Button("USA - Title WC", id="btn-wc-title-usa-chart", className="wc-metric-btn-name", disabled=True),
        ],className="corr-metric2-trend"),
        html.Div(children=[
            html.Button("IND - Title WC", id="btn-wc-title-ind-chart", className="wc-metric-btn-name", disabled=True),
        ],className="corr-metric2-trend"),
        html.Div(children=[
            html.Button("USA - Description WC", id="btn-wc-desc-usa-chart", className="wc-metric-btn-name", disabled=True),
        ],className="corr-metric2-trend"),
        html.Div(children=[
            html.Button("IND - Description WC", id="btn-wc-desc-ind-chart", className="wc-metric-btn-name", disabled=True),
        ],className="corr-metric2-trend"),
        html.Div(children=[
            html.Button("USA - Tag WC", id="btn-wc-tag-usa-chart", className="wc-metric-btn-name", disabled=True),
        ],className="corr-metric2-trend"),
        html.Div(children=[
            html.Button("IND - Tag WC", id="btn-wc-tag-ind-chart", className="wc-metric-btn-name", disabled=True),
        ],className="corr-metric2-trend")
    ], className="corr-btns")

    return btns

def get_correlation_analysis_layout(default_fig):
    rwt = html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                    html.Div(children=[
                        html.Div("Correlation & Word Cloud Analysis", className="corr-title"),
                        html.Button("Collapse", id="corr-collapse-btn", className="corr-expand-btn"),
                    ], className="corr-title-box"),
                    dbc.Collapse([
                        html.Div(children=[
                        html.Div([
                            daq.ToggleSwitch(
                                id='my-toggle-switch',
                                className='toggle-switch',
                                size=40,
                                label="",
                                value=False
                            ),
                            html.Div(id='my-toggle-switch-output', className="toggle-desc")
                        ], className="toggle-container"),
                        get_btns_layout_of_countries(),
                        html.Div(children=[
                            html.Div(children=[
                                    dcc.Graph(figure=default_fig, id='correlation-heatmap', className="corr-graph"),
                                ], className='graph-content')
                            ], className="corr-analysis-container", id="corr-analysis-container-id", style={'display': 'block'}),
                            html.Div(children=[
                                html.Div(children=[
                                    html.Img(src="/assets/img/usa-wc-title.png", id="wordcloud-image-id", className="wordcloud-image")
                                ], className='wordcloud-image-content')
                            ], className="wordcloud-analysis-container", id="wordcloud-analysis-container-id", style={'display': 'none'})
                    ], className='corr-wc-container'),
                ], id="corr-text-id", className="corr-text-container", is_open=False)
            ], id='corr-box-id', className="corr-box"),
        ], className="corr-content")
    ], className="corr-container")  

    return rwt