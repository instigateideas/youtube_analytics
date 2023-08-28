import pandas as pd

# main filter based on days
kpi_data = [
    {"img": "/assets/img/channel-icon.png", "name": "No. of Youtube Channels", "usa_value": "", "ind_value": ""},
    {"img": "/assets/img/trending-video.png", "name": "No. of Trending Videos", "usa_value": "", "ind_value": ""},
    {"img": "/assets/img/social-engagement.png", "name": "No. of Total Engagements", "usa_value": "", "ind_value": ""},
    {"img": "/assets/img/engagement-per-video.png", "name": "Avg. Engagement/ video", "usa_value": "", "ind_value": ""},
    {"img": "/assets/img/publish-rate.png", "name": "Avg. Content Publishing/ Day", "usa_value": "", "ind_value": ""},
    {"img": "/assets/img/avg-trending.png", "name": "Avg. Time video Trends (Hours)", "usa_value": "", "ind_value": ""}
]

usa_metric_data_x = [
    {"img": "/assets/img/views.png", "title": "Views", "value": "", "avg": "", "temp": ""},
    {"img": "/assets/img/likes.png", "title": "Likes", "value": "", "avg": "", "temp": ""},
    {"img": "/assets/img/comment.png", "title": "Comments", "value": "", "avg": "", "temp": ""},
    {"img": "/assets/img/dislike.png", "title": "Dislike", "value": "", "avg": "", "temp": ""},
]

ind_metric_data_x = [
    {"img": "/assets/img/views.png", "title": "Views", "value": "", "avg": "", "temp": ""},
    {"img": "/assets/img/likes.png", "title": "Likes", "value": "", "avg": "", "temp": ""},
    {"img": "/assets/img/comment.png", "title": "Comments", "value": "", "avg": "", "temp": ""},
    {"img": "/assets/img/dislike.png", "title": "Dislike", "value": "", "avg": "", "temp": ""},
]


def millions(x):
    return '{}M'.format(int(x / 1000000))

def thousands(x):
    value = int(x / 1000)
    if value > 0:
        return '{}K'.format(value)
    else:
        return int(x)

def country_kpi_analysis(df):
    no_of_ytb_channels = df["channel_title"].nunique()
    no_of_trending_videos = df["video_id"].nunique()

    # KPI's Calculation
    total_engagement = df["engagement"].sum()
    avg_video_engagement = int(df["engagement"].mean())
    avg_no_of_video_published_in_day = int(pd.DataFrame(df.groupby(["publish_date"])["video_id"].count().reset_index())["video_id"].mean())

    # Metric data Calculation
    total_views = df["views"].sum()
    total_likes = df["likes"].sum()
    total_comments = df["comment_count"].sum()
    total_dislikes = df["dislikes"].sum()
    avg_views = int(df["views"].mean())
    avg_likes = int(df["likes"].mean())
    avg_comments = int(df["comment_count"].mean())
    avg_dislikes = int(df["dislikes"].mean())

    # Temperature analysis calculations
    avg_views_temp = int(df["views_per_hr"].mean())
    avg_likes_temp = int(df["likes_per_hr"].mean())
    avg_comments_temp = int(df["comment_per_hr"].mean())
    avg_dislikes_temp = int(df["dislikes_per_hr"].mean())

    # Video age is nothing but time it remains trending
    avg_time_to_video_trend = int(df['trending_time_taken'].mean())

    # KPI analysis
    x = [no_of_ytb_channels, 
         no_of_trending_videos, 
         millions(total_engagement), 
         avg_video_engagement, 
         avg_no_of_video_published_in_day, 
         avg_time_to_video_trend
    ]

    # Metric analysis
    y = [{"value": millions(total_views), "avg": thousands(avg_views), "temp": thousands(avg_views_temp)}, 
         {"value": millions(total_likes), "avg": thousands(avg_likes), "temp": thousands(avg_likes_temp)}, 
         {"value": millions(total_comments), "avg": thousands(avg_comments), "temp": thousands(avg_comments_temp)}, 
         {"value": millions(total_dislikes), "avg": thousands(avg_dislikes), "temp": thousands(avg_dislikes_temp)}
    ]

    return x, y

def update_kpi_data(country_val, update_data, default_kpi_data):
    for ind_, kpi_data in enumerate(default_kpi_data):
        default_kpi_data[ind_][country_val] = update_data[ind_]

    return default_kpi_data

def update_metrics_data(update_data, default_metric_data):
    for ind_, metric_data in enumerate(default_metric_data):
        default_metric_data[ind_]["value"] = update_data[ind_]["value"]
        default_metric_data[ind_]["avg"] = update_data[ind_]["avg"]
        default_metric_data[ind_]["temp"] = update_data[ind_]["temp"]

    return default_metric_data

def get_metrics_data(usa_df, ind_df):
    usa_data_metric = update_metrics_data(update_data=usa_df, default_metric_data=usa_metric_data_x)
    ind_data_metric = update_metrics_data(update_data=ind_df, default_metric_data=ind_metric_data_x)

    return usa_data_metric, ind_data_metric


def get_kpi_data(usa_df, ind_df, default_kpi_data):
    usa_x, usa_y = country_kpi_analysis(usa_df)
    ind_x, ind_y = country_kpi_analysis(ind_df)

    default_kpi_data = update_kpi_data(country_val="usa_value", update_data=usa_x, default_kpi_data=default_kpi_data)
    updated_kpi_data = update_kpi_data(country_val="ind_value", update_data=ind_x, default_kpi_data=default_kpi_data)

    return updated_kpi_data, usa_y, ind_y

def get_kpi_analysis(cleaned_usa_df, cleaned_ind_df):
    kpi_analysis_data, usa_metric_y, ind_metric_y = get_kpi_data(usa_df=cleaned_usa_df, ind_df=cleaned_ind_df, default_kpi_data=kpi_data)
    usa_metric, ind_metric = get_metrics_data(usa_df=usa_metric_y, ind_df=ind_metric_y)

    return kpi_analysis_data, usa_metric, ind_metric
