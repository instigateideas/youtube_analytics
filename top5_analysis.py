import re
from collections import Counter
from nltk.util import ngrams
from nltk.tokenize import RegexpTokenizer
import emoji

data = {"img": "/assets/img/top5.png", "title": "Top 5's Analysis", 
        "analysis": [
            {"title": "Most Popular Emoji's used", "data_usa": ":), :(", "data_ind":  ":), :("},
            {"title": "Most Popular Symbols used", "data_usa": "&, #", "data_ind": "&, #"},
            {"title": "Most Popular common Bi-gram", "data_usa": "super-test, Mario-yet", "data_ind": "super-test, Mario-yet"},
            {"title": "Most Popular common Tri-gram", "data_usa": "chat-gpt-ml", "data_ind": "chat-gpt-ml"},
        ]
}

def most_popular_bigram_trigram(df, col_name='title'):
    tokenizer = RegexpTokenizer(r"[\w']+")
    ng2 = [ngrams(tokenizer.tokenize(t.lower()), n=2) for t in df[col_name]]
    # flatenning the list
    ng2 = [x for y in ng2 for x in y]

    ngrams2 = Counter(ng2).most_common(25)

    tokenizer = RegexpTokenizer(r"[\w']+")
    ng3 = [ngrams(tokenizer.tokenize(t.lower()), n=3) for t in df['title']]
    # flatenning the list
    ng3 = [x for y in ng3 for x in y]

    ngrams3 = Counter(ng3).most_common(25)

    return ngrams2, ngrams3

def most_popular_symbols_emoji(df, col_name='title'):
    all_titles = ' '.join([x.lower() for x in df[col_name]])
    title_symbols = re.sub(r'\w', '', all_titles)
    title_symbols = re.sub(r'\s', '', title_symbols)
    title_symbols = list(title_symbols)
    common_symbol = Counter(title_symbols).most_common(10)

    title_emojis = [x for x in title_symbols if x in emoji.EMOJI_DATA]
    common_emoji = Counter(title_emojis).most_common(10)

    return common_emoji, common_symbol

def filter_top5(data):
    top5 = ""
    for datum in data[0:5]:
        txt = "-".join(datum[0])
        top5 = top5 + f"{txt}; "
    
    return top5[:-2]

def calc_top5s(df):
    bigram_x, trigram_x = most_popular_bigram_trigram(df)
    emoji_x, symbol_x = most_popular_symbols_emoji(df)

    emoji_x = filter_top5(emoji_x)
    symbol_x = filter_top5(symbol_x)
    bigram_x = filter_top5(bigram_x)
    trigram_x = filter_top5(trigram_x)


    x = [
        emoji_x,
        symbol_x,
        bigram_x,
        trigram_x
    ]

    return x


def update_top5_analysis(x, default_data, country="data_usa"):
    for num_, datum in enumerate(default_data["analysis"]):
        datum[country] = x[num_]

    return default_data


def get_top5_analysis(usa_df, ind_df, default_data=data):
    x = calc_top5s(usa_df)
    y = calc_top5s(ind_df)

    default_data_x = update_top5_analysis(x, default_data, country="data_usa")
    final_data = update_top5_analysis(y, default_data_x, country="data_ind")

    return final_data