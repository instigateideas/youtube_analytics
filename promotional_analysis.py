import re
import pandas as pd


data = {"img": "/assets/img/promotion.png", "title": "Social Promotion",
    "analysis": [
        {"title": "No. of Youtube links in Video Description", "data_usa": "3200", "data_ind": "3200"},
        {"title": "Average of Youtube links in Video Description", "data_usa": "34", "data_ind": "3200"},
        {"title": "No. of Social Media domains links in Description eg. Instagram, Facebook, Twitter", "data_usa": "320", "data_ind": "3200"},
        {"title": "Average no of Social Media domain links in Description eg. Instagram, Facebook, Twitter", "data_usa": "11", "data_ind": "3200"},
        {"title": "No. of Google links in Description", "data_usa": "320", "data_ind": "3200"},
        {"title": "Average no of Google  links in Description", "data_usa": "11", "data_ind": "3200"},
        {"title": "No. of Other domain links in Description", "data_usa": "320", "data_ind": "3200"},
        {"title": "Average no of Other domain  links in Description", "data_usa": "11", "data_ind": "3200"}
]}


def calc_promotional_analysis(df):
    ytb_links = df["Youtube"].sum()
    ytb_df = df[df["Youtube"] > 0]
    avg_ytb_links = int(ytb_df["Youtube"].mean())
    df["social_media"] = df["Facebook"] + df["Instagram"] + df["Twitter"]
    social_media_links = df["social_media"].sum()
    socio_df = df[df["social_media"] > 0]
    avg_social_media_links = int(socio_df["social_media"].mean())
    google_domain_links = df["Google"].sum()
    google_df = df[df["Google"] > 0]
    avg_google_domain_links = int(google_df["Google"].mean())
    other_domain_links = df["Others"].sum()
    others_df = df[df["Others"] > 0]
    avg_other_domain_links = int(others_df["Others"].mean())

    x = [
            ytb_links, avg_ytb_links, 
            social_media_links, avg_social_media_links, 
            google_domain_links, avg_google_domain_links, 
            other_domain_links, avg_other_domain_links
        ]
    
    return x

def update_data_promtional_analysis(x, default_data, country="data_usa"):
    for num_, datum in enumerate(default_data["analysis"]):
        datum[country] = x[num_]

    return default_data


def get_promotional_analysis(usa_df, ind_df, default_data=data):
    x = calc_promotional_analysis(usa_df)
    y = calc_promotional_analysis(ind_df)

    default_data_x = update_data_promtional_analysis(x, default_data, country="data_usa")
    final_data = update_data_promtional_analysis(y, default_data_x, country="data_ind")

    return final_data



