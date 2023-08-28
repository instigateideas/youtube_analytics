import numpy as np
import pandas as pd
import os
from contractions import contractions_dict
import random
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.util import ngrams
from nltk import download as nltk_download
from matplotlib import pyplot as plt
from collections import Counter
from datetime import timedelta
import wordcloud
import base64
from io import BytesIO
import re

cwd = os.getcwd()

# For word clouds
WC_MAX_FZ = 400 
WC_RS = 0.5

def read_data():
    # current working directory
    cwd = os.getcwd()

    # load the dataframes
    data_path = os.path.join(cwd, "data")
    india_df = pd.read_csv(os.path.join(data_path, "india_ytb_data.csv"))
    usa_df = pd.read_csv(os.path.join(data_path, "usa_ytb_data.csv"))
    category_df = pd.read_csv(os.path.join(data_path, "category_id.csv"))

    # Merge the categories
    cat_df = category_df[["id", "snippet/title"]]
    india_df = india_df.merge(cat_df, how="left", left_on="category_id", right_on="id")
    usa_df = usa_df.merge(cat_df, how="left", left_on="category_id", right_on="id")

    return usa_df, india_df

def url_data_for_promotion_analysis(df, col_name):
    final_data = []
    for txt in df[col_name]:
        try:
            url_list = get_links(txt)
        except TypeError:
            pass
        data = {"Facebook": 0, "Instagram": 0, "Twitter": 0, "Youtube": 0, "Google": 0, "Others": 0}
        for url in url_list:
            if check(url, "fb"):
                data["Facebook"] = data["Facebook"] + 1 
            elif check(url, "instagram"):
                data["Instagram"] = data["Instagram"] +1 
            elif check(url, "twitter"):
                data["Twitter"] = data["Twitter"] +1 
            elif check(url, "goo.gl"):
                data["Google"] = data["Google"] + 1
            elif check(url, "youtube"):
                data["Youtube"] = data["Youtube"] + 1
            elif check(url, "youtube"):
                data["Youtube"] = data["Youtube"] + 1 
            else:
                data["Others"] = data["Others"] + 1 
        final_data.append(data)

    return pd.DataFrame(final_data)

def filter_data(df, day_frame):
    df["TrendingDate"] = pd.to_datetime(df['trending_date'], format='%y.%d.%m')
    df["PublishTime"] = pd.to_datetime(df['publish_time'], format='%Y-%m-%dT%H:%M:%S.%fZ')
    df["TrendingTimeTaken"] = (df['TrendingDate'] - df['PublishTime']).dt.total_seconds() / 60 / 60
    df["trending_time_taken"] = df["TrendingTimeTaken"].abs()
    max_date = df['PublishTime'].agg(['max'])
    subtracted_date = pd.to_datetime(max_date) - timedelta(days=day_frame)
    final_df = df.loc[df['PublishTime'] >= subtracted_date["max"]]

    return final_df

def generate_cols_for_temperature_analysis(df):
    df = df.copy()
    df["sequential"] = df.groupby('video_id').cumcount()+1
    age_df = df.groupby(["video_id"]).agg({"views":np.max, "likes":np.max , "comment_count":np.max , "dislikes":np.max , "sequential": np.max}).reset_index()
    age_df.rename(columns={"views": "total_view", "likes": "total_likes", "comment_count": "total_comment", "dislikes": "total_dislikes", "sequential": "age_in_days"}, inplace=True)
    age_df["views_per_hr"] = age_df["total_view"]/(age_df["age_in_days"]*8)
    age_df["likes_per_hr"] = age_df["total_likes"]/(age_df["age_in_days"]*8)
    age_df["comment_per_hr"] = age_df["total_comment"]/(age_df["age_in_days"]*8)
    age_df["dislikes_per_hr"] = age_df["total_dislikes"]/(age_df["age_in_days"]*8)

    # Dropping the duplicate - analysing only at the time of trending
    df.drop_duplicates(subset=['video_id'], inplace=True)
    df.drop(df[df["video_id"] == "#NAME?"].index, inplace=True)
    df.drop(df[df["video_id"] == "#VALUE!"].index, inplace=True)

    # Merge the age & temperature data
    final_df = df.merge(age_df, how='left', on='video_id')

    return final_df

def clean_create_neccessary_columns(df, days=90):
    # Filter the data
    df = filter_data(df, day_frame=days)
    df = df.copy()

    # Dropping the duplicate - analysing only at the time of trending
    df = generate_cols_for_temperature_analysis(df=df)

    # Create additional columns
    df["publish_date"] = df['PublishTime'].dt.strftime('%d-%m-%Y')
    df["trending_weekday"] = df['TrendingDate'].dt.day_name()
    df["trending_hour"] = df['TrendingDate'].dt.hour
    df["trending_month"] = df['TrendingDate'].dt.month_name()
    df["publish_weekday"] = df['PublishTime'].dt.day_name()
    df["publish_hour"] = df['PublishTime'].dt.hour
    df["publish_month"] = df['PublishTime'].dt.month_name() 
    df["engagement"] = df["likes"] + df["dislikes"] + df["comment_count"]
    df['title_length'] = df['title'].str.len()
    df['desc_length'] = df['description'].str.len()
    df['num_tags'] = df['tags'].apply(lambda x: len(x.split('|')) if x != '[none]' else 0)
    df['tags_length'] = df['tags'].apply(lambda x: len(x.replace('|', '')) if x != '[none]' else 0)

    # Create columns for promotional analysis
    url_df = url_data_for_promotion_analysis(df=df, col_name='description')
    df = pd.merge(df, url_df, left_index=True, right_index=True)

    return df

def clean_and_load_data():
    usa_df, ind_df = read_data()
    cleaned_usa = clean_create_neccessary_columns(df=usa_df)
    cleaned_ind = clean_create_neccessary_columns(df=ind_df)

    return cleaned_usa, cleaned_ind

def check(string, sub_str):
    if (string.find(sub_str) == -1):
        return 0
    else:
        return 1

def get_links(txt):
    myregex = r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}'
    url_list = re.findall(myregex, txt)

    return url_list

def get_cleaned_text(x):
    try:
        x = x.lower()
    except:
        x = ""

    return x

def clean_stopwords(df, col_name='title'):
    contractions = contractions_dict

    # nltk_download('stopwords')

    # if a contraction has more than one possible expanded forms, we replace it 
    # with a list of these possible forms
    tmp = {}
    for k,v in contractions.items():
        if "/" in v:
            tmp[k] = [x.strip() for x in v.split(sep="/")]
        else:
            tmp[k] = v
    contractions = tmp

    tokenizer = RegexpTokenizer(r"[\w']+")

    all_titles = ' '.join([get_cleaned_text(x) for x in df[col_name]])
    for k,v in contractions.items():
        if isinstance(v, list):
            v = random.choice(v)
        all_titles = all_titles.replace(k.lower(), v.lower())
        
    words = list(tokenizer.tokenize(all_titles))
    words_excl_stopwords = [x for x in words if x not in stopwords.words('english')]

    return words, words_excl_stopwords

def col_func(word, font_size, position, orientation, font_path, random_state):
    colors = ["#14110c", "#214658", "#e7aa27", "#dc4e24"]
    return colors[len(word)%len(colors)]

def save_words_in_excel(df, col_name, country):
    words, words_excl_stopwords = clean_stopwords(df=df, col_name=col_name)
    word_df = pd.DataFrame({"words": words_excl_stopwords}).reset_index()
    word_df.columns = ["index", "words"]
    save_df = pd.DataFrame(word_df.groupby(["words"])["index"].count().sort_values(ascending=False).reset_index())
    save_df.columns = ["words", "count"]
    file_name = os.path.join(cwd, 'assets', 'wc_data', f'{country}_wc_{col_name}.xlsx')
    save_df.to_excel(file_name)

def get_word_count_analysis(col_name, country, top=10):
    file_name = os.path.join(cwd, 'assets', 'wc_data', f'{country}_wc_{col_name}.xlsx')
    word_df = pd.read_excel(file_name)
    word_df = word_df[0:top]

    return word_df

def get_word_cloud_img_obj(col_name, country):
    file_name = os.path.join(cwd, 'assets', 'wc_data', f'{country}-wc-{col_name}.xlsx')
    word_df = pd.read_excel(file_name)
    words_excl_stopwords = list(word_df["words"])
    wc = wordcloud.WordCloud(width=1920, height=1080, collocations=False, 
                         background_color="#262b49", color_func=col_func, 
                         max_words=100,random_state=1, max_font_size=WC_MAX_FZ, 
                         relative_scaling=WC_RS
                        ).generate_from_frequencies(dict(Counter(words_excl_stopwords)))
    
    plt.figure(figsize=(8, 4))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")

    # Convert the plot to an image and encode it in base64
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    img_data = base64.b64encode(buffer.read()).decode()

    return img_data
