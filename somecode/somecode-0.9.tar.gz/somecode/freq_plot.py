import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from stopword import stopword 

def freq_plot(data,stop_words="",color="steelblue"):
    
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

    # single instances (words, hashtags, mentions)

    text_df = l[l.str.contains("^[a-z0-9]")].value_counts().head(20).reset_index()
    text_df.columns = ['keyword','value']

    hashtag_df = l[l.str.strip(":").str.startswith("#")].value_counts().head(20).reset_index()
    hashtag_df.columns = ['keyword','value']

    mention_df = l[l.str.startswith("@")].value_counts().head(20).reset_index()
    mention_df.columns = ['keyword','value']

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

    sns.set_context("notebook", font_scale=1.7, rc={"lines.linewidth": 0})
    sns.set_context(rc = {'patch.linewidth': 0.1})
    sns.set_color_codes("pastel")
    sns.set_style("white", {'axes.grid' : False})

    fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(20,5))

    sns.barplot(x='value',y='keyword',data=text_df.head(10), color=color, saturation=1.1,  ax=ax1, alpha=.2);
    sns.barplot(x='value',y='keyword',data=mention_df.head(10), color=color, saturation=1.1,  ax=ax2, alpha=.2);
    sns.barplot(x='value',y='keyword',data=hashtag_df.head(10), color=color, saturation=1.1,  ax=ax3, alpha=.2);

    plt.tick_params(axis='both', which='major', pad=25)

    ax1.set_xticklabels('')
    ax1.set_ylabel('')
    ax1.set_xlabel('')
    ax1.tick_params(axis='both', which='major', pad=15)

    ax2.set_xticklabels('')
    ax2.set_ylabel('')
    ax2.set_xlabel('')
    ax2.tick_params(axis='both', which='major', pad=15)

    ax3.set_xticklabels('')
    ax3.set_ylabel('')
    ax3.set_xlabel('')
    ax3.tick_params(axis='both', which='major', pad=15)

    sns.despine(left=True, bottom=True)
    #fig.subplots_adjust(right=3)
    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=1, hspace=None)
    #plt.setp(ax1.patches, linewidth=3)