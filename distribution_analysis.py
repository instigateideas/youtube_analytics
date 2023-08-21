


data = {
    "img": "/assets/img/distribution.png", "title": "Distribution Analysis",
    "analysis": [
        {"title": "Distribution of Time Taken to Trend", "data_usa": "2 days", "data_ind": "2 days"},
        {"title": "Distribution of Title Length", "data_usa": "34", "data_ind": "2 days"},
        {"title": "Distribution of Description Length", "data_usa": "140", "data_ind": "2 days"},
        {"title": "Distribution of Tag Length", "data_usa": "11", "data_ind": "2 days"},
    ]
}

def distribuition_of_text_data(df, col_name):
    text_lengths = df[col_name].apply(lambda x: len(x))
    mini = int(text_lengths.min())
    qut25 = int(text_lengths.quantile(q=0.25))
    qut50 = int(text_lengths.quantile(q=0.50))
    qut75 = int(text_lengths.quantile(q=0.75))
    qut90 = int(text_lengths.quantile(q=0.90))
    maxi = int(text_lengths.max())
    avg = int(text_lengths.mean())

    data = f"Avg:{avg};[Min:{mini}; Quantile 25%-{qut25} 50%-{qut50} 75%-{qut75} 90%-{qut90}; Max: {maxi}]"

    return data

def len_checker(x):
    try:
        y = len(x)
    except TypeError:
        y = 0

    return y

def distribuition_of_text_data(df, col_name, dist_type='text'):
    if dist_type=="text":
        text_lengths = df[col_name].apply(lambda x: len_checker(x))
    elif dist_type=='integer':
        text_lengths = df[col_name]
    
    mini = int(text_lengths.min())
    qut25 = int(text_lengths.quantile(q=0.25))
    qut50 = int(text_lengths.quantile(q=0.50))
    qut75 = int(text_lengths.quantile(q=0.75))
    qut90 = int(text_lengths.quantile(q=0.90))
    maxi = int(text_lengths.max())
    avg = int(text_lengths.mean())

    data = f"Avg:{avg};[Min:{mini}; Quantile 25%-{qut25} 50%-{qut50} 75%-{qut75} 90%-{qut90}; Max: {maxi}]"

    return data

def calc_distributions(df):
    trend_time_dist = distribuition_of_text_data(df=df, col_name='trending_time_taken', dist_type='integer')
    title_dist = distribuition_of_text_data(df=df, col_name='title')
    desc_dist = distribuition_of_text_data(df=df, col_name='description')
    tag_dist = distribuition_of_text_data(df=df, col_name='tags')

    x = [
        trend_time_dist,
        title_dist,
        desc_dist,
        tag_dist
    ]

    return x


def update_data_distribution_analysis(x, default_data, country="data_usa"):
    for num_, datum in enumerate(default_data["analysis"]):
        datum[country] = x[num_]

    return default_data


def get_distribution_analysis(usa_df, ind_df, default_data=data):
    x = calc_distributions(usa_df)
    y = calc_distributions(ind_df)

    default_data_x = update_data_distribution_analysis(x, default_data, country="data_usa")
    final_data = update_data_distribution_analysis(y, default_data_x, country="data_ind")

    return final_data


