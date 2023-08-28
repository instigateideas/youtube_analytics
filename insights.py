from dash import Dash, html, dcc, Input, Output, State

insights = {
    "Channel Diversity and Trends": ["India's 14% surplus channels foster a vibrant trending environment, with an average of 7 trending videos per channel—distinctly surpassing the USA's 2, underscoring India's robust creator landscape."],
    "Video Velocity": ["The USA publishes 16 videos daily per channel, while India excels with 63 videos, showcasing a higher content creation pace."],
    "Speedy Trending": ["India achieves trending videos 50% faster than the USA, suggesting different engagement dynamics and trend identification methods."],
    "Engagement Correlations": ["In the USA, comments correlate strongly (0.89) with likes, while India's trend relies on a correlation (0.76) between likes and views, implying distinct trend algorithms."],
    "Robust Promotion": ["Indian creators employ rich promotion strategies, linking to prior videos and diverse social media platforms."],
    "Top Trending Genres": ["Both regions prioritize entertainment, with India uniquely emphasizing News & Politics, highlighting YouTube's role in news dissemination."],
    "Content Insights": ["These insights underscore diverse content creation patterns, engagement dynamics, and trend mechanisms in YouTube trends across India and the USA."]
}

# insights = [
#     "The 14% more channels are available in country India than USA. Obviously possiblity of Trending videos are high. But analysing Trending Video per channel is 7 in India where as in USA it is only 2. So their good amount of content creators in India than USA.",
#     "Across all channels Publishing Average of USA is just 16 videos/day but India rate is 63 videos/day.",
#     "Despite fact in India their are good content creator and more videos published per day time taken to trend is shorter by 50% for India than in USA.",
#     "Understanding the Correlation between the subscibers engagement [likes, dislikes, comment] metrics Surpirsingly, USA - 0.89 positive correlation between comments_count & likes. But in India 0.76 positive correlation between likes and views to make a video trend.This clearly depicts the algorithm followed to make video trend is different across regions in Youtube.",
#     "Though their is difference in Algorithm. We could able to see the Promotion Strategy followed by Indians is always 50% in higher note than USA (refer depth analysis) more reference links to other youtube videos they have published earlier or other social platform links like FB, Insta, Twitter & other domain urls are also mentioned to drive engagement from subscribers.",
#     "Top Categories Entertainment in both regions. Indians more trending category have News & Politics followed by Music and Comedy category.",
# ]

insights_layout =html.Div(children=[
    html.Div(children=[
        html.Div(children=[
            html.Div("Key Insights Discovered", className="insights-title"),
            html.Div(children=[
                html.Div(children=[
                    html.Div(heads, className="insight-sub-head"),
                    html.Div(f"- {insight[0]}", className="sub-head-content")
                ])
            for heads, insight in insights.items()], className="insights-text"),
            html.Div("Last 90 days data is analysed to gather insights", className="insights-footer")
        ], className="insights-box")
    ], className="insights-content")  
], className="insights-container")