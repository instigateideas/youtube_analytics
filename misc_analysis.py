import re


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
