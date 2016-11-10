def retweet_plot(data):

    import seaborn as sns
    import matplotlib.pyplot as plt

    sns.set(style="whitegrid")
    sns.set_context("notebook", font_scale=3, rc={"lines.linewidth": 0.3})

    sns.set_color_codes("bright")

    temp = (1500 / float(data.retweet_count.max()))
    size = data.retweet_count * temp

    g = sns.PairGrid(data, hue="egg_account", palette="Blues", y_vars="influence_score", x_vars="reach_score" , size=12, aspect=3)
    g.map(plt.scatter, s=size);
    g.set(xscale="symlog")
    g.add_legend(title="Egg Account", label_order=['True','False'], bbox_to_anchor=(0.9, 0.6))

    plt.title('bigger size = more retweets', fontsize=48, y=1.12, color="gray");

    plt.suptitle('Are high retweet counts per tweet related with influence and reach?', verticalalignment='top', fontsize=30, y=1.01)
    plt.xlabel('more reach - >', fontsize=38, labelpad=30, color="gray");
    plt.ylabel('higher influence - >', fontsize=38, labelpad=30, color="gray");
    plt.axhline(linewidth=2.5, color="black");
    plt.axvline(linewidth=2.5, color="black");
    plt.ylim(0,);
    plt.xlim(0,);

    plt.tick_params(axis='both', which='major', pad=25)