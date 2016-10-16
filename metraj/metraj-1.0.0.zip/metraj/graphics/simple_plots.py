import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection, LineCollection
from matplotlib.patches import Ellipse, Circle


def plot_trajectory_scatter(frame, size_col=1):
    frame.plot(kind="scatter", x=frame.geo_cols[0], y=frame.geo_cols[1], s=size_col)
    plt.title(frame.id)
    plt.show()


def plot_trajectory_ellipse(frame, varx="attr_VARX", vary="attr_VARY", covxy="attr_COVXY", opacity_factor=1):
    """
    Draw the trajectory and uncertainty ellipses around teach point.
    1) Scatter of points 
    2) Trajectory lines
    3) Ellipses 
    :param frame: Trajectory
    :param opacity_factor: all opacity values are multiplied by this. Useful when used to plot multiple Trajectories in
     an overlay plot.
    :return: axis
    """
    ellipses = []    
    segments = []
    start_point = None

    for i, pnt in frame.iterrows():  
        # The ellipse
        U, s, V = np.linalg.svd(np.array([[pnt[varx], pnt[covxy]], 
                                          [pnt[covxy], pnt[vary]]]), full_matrices=True)
        w, h = s**.5 
        theta = np.arctan(V[1][0]/V[0][0])   # == np.arccos(-V[0][0])              
        ellipse = {"xy":pnt[list(frame.geo_cols)].values, "width":w, "height":h, "angle":theta}
        ellipses.append(Ellipse(**ellipse))
        
        # The line segment
        x, y = pnt[list(frame.geo_cols)][:2]
        if start_point:           
            segments.append([start_point, (x, y)])
        start_point = (x, y)

    ax = plt.gca()
    ellipses = PatchCollection(ellipses)
    ellipses.set_facecolor('none')
    ellipses.set_color("green")
    ellipses.set_linewidth(2)
    ellipses.set_alpha(.4*opacity_factor)
    ax.add_collection(ellipses)

    frame.plot(kind="scatter", x=frame.geo_cols[0], y=frame.geo_cols[1], marker=".", ax=plt.gca(), alpha=opacity_factor)

    lines = LineCollection(segments)
    lines.set_color("gray")
    lines.set_linewidth(1)
    lines.set_alpha(.2*opacity_factor)
    ax.add_collection(lines)
    return ax


def plot_trajectory_multistage(traj, count, shape, style):
    for i in range(count):
        plt.subplot(shape[0], shape[1], i+1)
        t = traj.get_next(depth=i)
        plot_trajectory_ellipse(t)
        plt.title(style["titles"][i])
    plt.suptitle(style["suptitle"])
    plt.show()


def trajectory_overlay_plot(trajectories, opacity):
    """
    Overlay plot multiple trajectories with different opacity. This allows for instance, to plot a processed
     Trajectory over the raw data, in order to see the change, or two stages in the processing side by side.
    :param trajectories: list of Trajectory objects
    :param opacity: list of opacity values, the same length as trajectories
    :return: axis
    """
    for t, o in zip(trajectories, opacity):
        ax = plot_trajectory_ellipse(t, opacity_factor=o)
    plt.show()


def plot_sparse_trajectory(trajectory, r=50, opacity_factor=1, plot_text=True,
                           num_col="segment_sparcify_n", min_static=100):
    """
    Plots a sparsified trajectory as circles with the number of points they represent as a number inside.
    :param trajectory: Trajectory object
    :param r: the radius of circles
    :param num_col: where to find the number to put in the circles
    :param min_static: minimum count to change color of circle
    :param plot_text: put the text with num of points in the circle?
    :return: ax
    """
    ax = plt.gca()
    trajectory.plot(kind="scatter", x=trajectory.geo_cols[0], y=trajectory.geo_cols[1], marker=".",
                    ax=plt.gca(), alpha=0.0*opacity_factor)

    circles = []
    segments = []
    start_point = None

    for i, pnt in trajectory.iterrows():
        circles.append(Circle(pnt[list(trajectory.geo_cols)].values, radius=r))

        if plot_text:
            plt.text(*pnt[list(trajectory.geo_cols)], s=str(int(pnt[num_col])), fontsize=12)

        x, y = pnt[list(trajectory.geo_cols)][:2]
        if start_point:
            segments.append([start_point, (x, y)])
        start_point = (x, y)

    circles = PatchCollection(circles)
    circles.set_facecolor(['none' if cnt < min_static else 'red' for cnt in trajectory[num_col].values])
    circles.set_alpha(.5*opacity_factor)
    ax.add_collection(circles)

    lines = LineCollection(segments)
    lines.set_color("gray")
    lines.set_alpha(.2*opacity_factor)
    ax.add_collection(lines)

    return ax
