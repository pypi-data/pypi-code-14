from pylab import *  # @UnusedWildImport
import matplotlib.pyplot as plt  # @Reimport

"""
Plotting Module
"""


def den_plot(x_ref, y_fwd_smoothed, y_rvs_smoothed, nt, file_fig,
             file_name, onscreen, x_label, plot_y_lim, pub=False):
    """
    Single alignment profile
    :param x_ref: x co-ords (list(int))
    :param y_fwd_smoothed: positive y co-ords (list(float))
    :param y_rvs_smoothed: negative y co-ords (list(float))
    :param nt: aligned read length (int)
    :param file_fig: output plot to pdf (bool)
    :param file_name: output filename (str)
    :param onscreen: show plot on screen (bool)
    :param x_label: x label (str)
    :param plot_y_lim: + / - y-axis limit (int)
    :param pub: publication plot (bool)
    """
    plt.plot(x_ref, y_fwd_smoothed, color=_nt_colour(nt),
             label='{0} nt'.format(nt), lw=2)
    plt.plot(x_ref, y_rvs_smoothed, color=_nt_colour(nt), lw=2)
    axhline(y=0)
    if pub:
        _pub_plot()
    else:
        xlabel(x_label)
        ylabel('Reads per million reads')
        plt.legend(loc='best', fancybox=True, framealpha=0.5)
    _generate_profile(file_fig, file_name, onscreen, plot_y_lim)


def den_multi_plot_21_22_24(x_ref,
                            y_fwd_smoothed_21, y_rvs_smoothed_21,
                            y_fwd_smoothed_22, y_rvs_smoothed_22,
                            y_fwd_smoothed_24, y_rvs_smoothed_24, file_fig,
                            file_name, onscreen, x_label, plot_y_lim,
                            pub=False):
    """
    21, 22 and 24nt combined alignment profile
    :param x_ref: x co-ords (list(int))
    :param y_fwd_smoothed_21: 21 nt positive y co-ords (list(float))
    :param y_rvs_smoothed_21: 21 nt negative y co-ords (list(float))
    :param y_fwd_smoothed_22: 22 nt positive y co-ords (list(float))
    :param y_rvs_smoothed_22: 22 nt negative y co-ords (list(float)):
    :param y_fwd_smoothed_24: 24 nt positive y co-ords (list(float))
    :param y_rvs_smoothed_24: 24 nt negative y co-ords (list(float))
    :param nt: aligned read length (int)
    :param file_fig: output plot to pdf (bool)
    :param file_name: output filename (str)
    :param onscreen: show plot on screen (bool)
    :param x_label: x label (str)
    :param plot_y_lim: + / - y-axis limit (int)
    :param pub: publication plot (bool)
    """
    plt.plot(x_ref, y_fwd_smoothed_21, color='#00CC00', label='21 nt', lw=2)
    plt.plot(x_ref, y_rvs_smoothed_21, color='#00CC00', lw=2)
    plt.plot(x_ref, y_fwd_smoothed_22, color='#FF3399', label='22 nt', lw=2)
    plt.plot(x_ref, y_rvs_smoothed_22, color='#FF3399', lw=2)
    plt.plot(x_ref, y_fwd_smoothed_24, color='#3333FF', label='24 nt', lw=2)
    plt.plot(x_ref, y_rvs_smoothed_24, color='#3333FF', lw=2)
    axhline(y=0)
    if pub:
        _pub_plot()

    else:  # no_publication
        xlabel(x_label)
        ylabel('Reads per million reads')
        plt.rc('font') #remove?
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                   ncol=3, mode="expand", borderaxespad=0., fontsize=12)
    _generate_profile(file_fig, file_name, onscreen, plot_y_lim)


def cdp_plot(counts_by_ref, seq1, seq2, nt, onscreen, file_fig, file_name, pub):
    """
    Scatter plot of alignments to references
    :param counts_by_ref: dict of (x,y) counts for each reference (dict)
    :param seq1: x label (str)
    :param seq2: y label (str)
    :param nt: aligned read length (int)
    :param file_fig: output plot to pdf (bool)
    :param file_name: output filename (str)
    :param onscreen: show plot on screen (bool)
    :param pub: publication plot (bool)
    """
    results_list = []  # list of results
    for counts in counts_by_ref.values():
        results_list.append((counts[0] + 0.01, counts[1] + 0.01))
        # hack that allows zero values to be plotted on a log scale
    results_list = sorted(results_list)

    _max = max(results_list[-1][0], results_list[-1][1])  # sets up max x and y scale values
    _max += float(_max / 2)

    plt.scatter(*list(zip(*results_list)),
                s=10,
                color=_nt_colour(nt),
                marker='o',
                label="{0} nt".format(nt))

    arrow(0.1, 0.1, _max, _max, color='r')
    xscale('log')
    yscale('log')
    xlim(0.1, _max)
    ylim(0.1, _max)
    if pub:
        _pub_plot()
    else:
        plt.legend(loc='upper left', fancybox=True, framealpha=0.5)
        xlabel(seq1)
        ylabel(seq2)
    _shared_plot(file_fig, file_name, onscreen)


def _generate_profile(file_fig, file_name, onscreen, plot_y_lim):
    """
    Generate profile
    :param file_fig: output plot to pdf (bool)
    :param file_name: output filename (str)
    :param onscreen: show plot on screen (bool)
    :param plot_y_lim: + / - y-axis limit (int)
    """
    if plot_y_lim != 0:
        ylim(-plot_y_lim, plot_y_lim)
    _shared_plot(file_fig, file_name, onscreen)


def _pub_plot():
    """
    Remove axis, labels, legend from plot
    """
    plt.tick_params(
        axis='both',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom='on',  # ticks along the bottom edge are off
        top='off',
        right='on',
        left='on',  # ticks along the top edge are off
        labelbottom='off',
        labelleft='off',
        labelright='off',
        labelsize=15)  # labels along the bottom edge are off
    _clear_frame()


def _clear_frame(ax=None):
    """
    Removes frame for publishing plots
    """
    if ax is None:
        ax = plt.gca()
    ax.xaxis.set_visible(True)
    ax.yaxis.set_visible(True)
    for spine in ax.spines.values():
        spine.set_visible(False)


def _shared_plot(file_fig, file_name, onscreen):
    """

    :param file_fig: output plot to pdf (bool)
    :param file_name: output filename (str)
    :param onscreen: show plot on screen (bool)
    """
    fig1 = plt.gcf()
    if onscreen:
        plt.show()
    if file_fig:
        fig1.savefig(file_name, format='pdf')
    plt.close(fig1)


def _nt_colour(nt):
    """
    Set default colours for 21, 22 and 24 nt sRNAs
    :param nt: aligned read length (int)
    :return: colour code (str)
    """
    if nt == 21:
        col = '#00CC00'
    elif nt == 22:
        col = '#FF3399'
    elif nt == 24:
        col = '#3333FF'
    else:
        col = 'black'
    return col
