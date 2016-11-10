import pandas as pd

from stopword import stopword

def cooc_plot(data,stop_words=""):

    import seaborn as sns
    import matplotlib.pyplot as plt 

    tweet_text = data.text.str.replace('[^A-Za-z0-9@#]+', " ")
    words_keyword = pd.Series(' '.join(tweet_text).lower().split())
    words_keyword = [line.decode('utf-8').strip() for line in words_keyword]
    words_keyword = pd.Series(words_keyword).replace('[^A-Za-z0-9#]+', " ")

    ## MODULE FOR KEYWORD ANALYSIS

    l = []
    for word in words_keyword:
        if word not in stop_words:
            if word not in stopword():
                if len(word) > 2:
                    l.append(word)

    l = pd.Series(l)

    l = l.str.strip(":")

    ## word co-occurance

    i = -1
    ll = []

    for word in l:
        try:
            i = i + 1
            ii = i + 1
            ll.append(unicode(l[i]) + ' ' + unicode(l[ii]))
        except KeyError:
            cooc_df = pd.DataFrame(pd.Series(ll).value_counts()).head(10).reset_index()
            cooc_df.columns = ['keyword','value']
            break

    ### sns.set(style="whitegrid")
    sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 0})

    x = cooc_df.head(20)['keyword']
    y = cooc_df.head(20)['value'].astype(int)

    f, ax = plt.subplots(figsize=(16, 3))

    sns.set_style('white')

    ## change color of the bar based value
    colors = ['black' if _y >=0 else 'red' for _y in y]

    sns.barplot(x, y, palette=colors, ax=ax)

    ax.set_xticklabels('')
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.tick_params(axis='both', which='major', pad=30)

    for n, (label, _y) in enumerate(zip(x, y)):
        ax.annotate(
            s='{:.1f}'.format(abs(_y)),
            xy=(n, _y),
            ha='center',va='center',
            xytext=(0,-10),
            size=12,
            textcoords='offset points',
            color="white",
            weight="bold"
        )
    ax.set_yticklabels("");
    ax.set_xticklabels(cooc_df.head(20)['keyword'],rotation=25,ha="right");
    ax.tick_params(axis='both', which='major', pad=15)
    sns.despine(left=True)