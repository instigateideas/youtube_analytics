import re
import pandas as pd
import os

cwd = os.getcwd()
DATA_DIR = os.path.join(cwd, "assets", "wc_data")

# Descriptive
def count_of_upper_cased_words(df, col_name='title'):
    upper_counts = []
    for t in df[col_name].values:
        t = re.sub(r'[^\w]', ' ', t)
        t = t.split()
        c = 0
        for w in t:
            if w.isalpha() and w.isupper():
                c += 1
        upper_counts.append(c)

    return upper_counts

# Descriptive
def count_of_full_upper_cased_titles(df, col_name='title'):
    upper_cased_title = []
    for t in df[col_name].values:
        if str(t).isupper:
            upper_cased_title.append(1)
        else:
            upper_cased_title(0)

    return upper_cased_title

# Descriptive Title & Description
def count_of_hastags(df, col_name='title'):
    hashtag_counts = df[col_name].apply(lambda x: len(re.findall(r'\B\#\w+?\b', str(x))))

    return hashtag_counts

def save_hastags_in_excel(df, col_name, country):
    hastag_corpus = []
    for x in df[col_name]:
        hastags = re.findall(r'\B\#\w+?\b', str(x))
        hastag_corpus.extend(hastags)
    all_df = pd.DataFrame({"hastags": hastag_corpus}).reset_index()
    all_df.columns = ["index", "hastags"]
    save_df = pd.DataFrame(all_df.groupby(["hastags"])["index"].count().sort_values(ascending=False).reset_index())
    save_df.columns = ["hashtag", "count"]

    file_name = os.path.join(DATA_DIR, f"{country}_hastags_{col_name}.xlsx")
    save_df.to_excel(file_name)

def get_hastag_analysis(col_name, country, top=10):
    file_name = os.path.join(cwd, 'assets', 'wc_data', f'{country}_hastags_{col_name}.xlsx')
    word_df = pd.read_excel(file_name)
    word_df = word_df[0:top]

    return word_df


# do it for description as well
def percentage_of_hashtags(df, col_name='title'):
    title_contains_hashtag = df[col_name].apply(lambda x: True if re.search(r'\B\#\w+?\b', str(x)) else False)
    percent_val = title_contains_hashtag.sum() / df.shape[0] * 100

    return title_contains_hashtag, df.shape[0], percent_val

# description as well
def percentage_of_full_upper_case(df, col_name='title'):
    # considering only unique videos
    upper_cased_count = df.drop_duplicates(subset=['video_id'])[col_name].apply(str.isupper).sum()
    count_unique_videos = df.drop_duplicates(subset=['video_id']).shape[0]

    percent_val = upper_cased_count/ count_unique_videos * 100

    return upper_cased_count, count_unique_videos, percent_val


def percentage_of_title_cased(df, col_name='title'):
    titlecase_count = 0
    total_oppertunities = df.shape[0]
    for t in df[col_name].values:
        t = re.sub(r'[^\w]', ' ', t)
        t = t.split()
        word_count = len(t) 
        c = 0
        for w in t:
            if w[0].isalpha() and w[0].isupper():
                c += 1
        if c >= 0.7 * word_count:
            titlecase_count += 1

    print('{} titles out of {} titles are title-cased'.format(titlecase_count, total_oppertunities))
    percent_val = int(titlecase_count/total_oppertunities*100)

    return titlecase_count, total_oppertunities, percent_val
