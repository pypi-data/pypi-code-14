import seaborn as sns
import matplotlib.pyplot as plt

def neg_plot(data):

    sns.set(style="whitegrid")
    sns.set_context("notebook", font_scale=3, rc={"lines.linewidth": 0.3})

    sns.set_color_codes("bright")

    temp = (1500 / float(data.neg.max()))
    size = data.neg * temp

    size = 10000 * (data.neg ** 1.9)
    g = sns.PairGrid(data, hue="egg_account", palette="Reds", y_vars="influence_score", x_vars="reach_score" , size=12, aspect=3)
    g.map(plt.scatter, s=size);
    g.set(xscale="symlog")
    g.add_legend(title="Egg Account", label_order=['True','False'], bbox_to_anchor=(0.9, 0.55), fontsize=38,
                    prop={'weight':'roman','size':'small'})

    plt.title('Are negative tweets amplified by influence and reach?', fontsize=48, y=1.12, color="gray");
    plt.suptitle('bigger bubble = more negative tweet', verticalalignment='top', fontsize=38, y=1.01, color="gray")
    plt.xlabel('more reach - >', fontsize=38, labelpad=30, color="gray");
    plt.ylabel('higher influence - >', fontsize=38, labelpad=30, color="gray");
    plt.axhline(linewidth=2.5, color="black");
    plt.axvline(linewidth=2.5, color="black");
    plt.ylim(0,);
    plt.xlim(0,);

    plt.tick_params(axis='both', which='major', pad=25)