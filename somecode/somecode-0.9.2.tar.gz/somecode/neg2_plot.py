import seaborn as sns
import matplotlib.pyplot as plt

def neg2_plot(data):
    
    sns.set(style="whitegrid")
    sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 0.3})

    sns.set_color_codes("bright")

    fig, ax = plt.subplots()
    sns.barplot(x='quality_score',y='neg',hue='egg_account',data=data,palette="Reds", saturation=1.1, ax=ax);
    fig.set_size_inches(20, 6)

    plt.title('Are poor quality accounts more associated with negative tweets?', fontsize=26, y=1.12, color="gray");
    plt.xlabel('better quality - >', fontsize=18, labelpad=30, color="gray");
    plt.ylabel('more negative - >', fontsize=18, labelpad=30, color="gray");
    plt.axhline(linewidth=2.5, color="black");
    plt.axvline(linewidth=2.5, color="black");
    plt.ylim(0,);
    plt.xlim(0,);

    plt.tick_params(axis='both', which='major', pad=25)