import matplotlib.pylab as plt
import seaborn as sns
import numpy as np

def hist_plot(data):

    sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 0})

    sns.set_style('white')

    fig, axes = plt.subplots(1, 3, figsize=(19, 5))
    
    axes[0].hist(data.influence_score,lw=0,color="indianred",bins=8);
    axes[0].set_xlabel("Influence Score")
    axes[0].tick_params(axis='both', which='major', pad=15)

    axes[1].hist(data.quality_score,lw=0,color="indianred",bins=7,align="left");
    axes[1].axis('tight')
    axes[1].tick_params(axis='both', which='major', pad=15)
    axes[1].set_xlabel("Quality Score")

    axes[0].set_yticklabels("");
    axes[1].set_yticklabels("");
    axes[2].set_yticklabels("");

    axes[2].hist(np.log(data.reach_score),lw=0,color="indianred",bins=9);
    axes[2].set_xlabel("Reach Score (log)");
    axes[2].tick_params(axis='both', which='major', pad=15)
    sns.despine(left=True)