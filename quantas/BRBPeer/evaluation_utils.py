import pathlib 
import os
import numpy as np
import json
import math
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re
from matplotlib import animation
import time
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import distinctipy

# base tests
ma1_multi_wheel_n99_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA1" / "multipartite_wheel" / "n99_k6"
ma2_multi_wheel_n99_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA2" / "multipartite_wheel" / "n99_k6"
ma3_multi_wheel_n99_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA3" / "multipartite_wheel" / "n99_k6"

ma1_gener_wheel_n100_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA1" / "generalized_wheel" / "n100_k6"
ma2_gener_wheel_n100_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA2" / "generalized_wheel" / "n100_k6"
ma3_gener_wheel_n100_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA3" / "generalized_wheel" / "n100_k6"

ma1_gener_wheel_byz_center_n100_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA1" / "generalized_wheel_byz_center" / "n100_k6"
ma2_gener_wheel_byz_center_n100_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA2" / "generalized_wheel_byz_center" / "n100_k6"
ma3_gener_wheel_byz_center_n100_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA3" / "generalized_wheel_byz_center" / "n100_k6"

ma1_random_graph_n100_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA1" / "random_graph" / "n100_k6"
ma2_random_graph_n100_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA2" / "random_graph" / "n100_k6"
ma3_random_graph_n100_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA3" / "random_graph" / "n100_k6"

ma1_random_graph_n100_k6_e500 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA1" / "random_graph" / "n100_k6_e500"
ma2_random_graph_n100_k6_e500 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA2" / "random_graph" / "n100_k6_e500"
ma3_random_graph_n100_k6_e500 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA3" / "random_graph" / "n100_k6_e500"

ma1_random_graph_n100_k6_e600 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA1" / "random_graph" / "n100_k6_e600"
ma2_random_graph_n100_k6_e600 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA2" / "random_graph" / "n100_k6_e600"
ma3_random_graph_n100_k6_e600 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA3" / "random_graph" / "n100_k6_e600"

ma1_random_graph_n100_k6_e700 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA1" / "random_graph" / "n100_k6_e700"
ma2_random_graph_n100_k6_e700 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA2" / "random_graph" / "n100_k6_e700"
ma3_random_graph_n100_k6_e700 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA3" / "random_graph" / "n100_k6_e700"

ma1_random_graph_pruned_n100_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA1" / "random_graph_pruned" / "n100_k6"
ma2_random_graph_pruned_n100_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA2" / "random_graph_pruned" / "n100_k6"
ma3_random_graph_pruned_n100_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "MA3" / "random_graph_pruned" / "n100_k6"

ma1_random_graph_n100_k6_byz_high_conn = pathlib.Path(__file__).parent.parent.parent / "results" / "MA1" / "random_graph_byz_high_conn" / "n100_k6"
ma2_random_graph_n100_k6_byz_high_conn = pathlib.Path(__file__).parent.parent.parent / "results" / "MA2" / "random_graph_byz_high_conn" / "n100_k6"
ma3_random_graph_n100_k6_byz_high_conn = pathlib.Path(__file__).parent.parent.parent / "results" / "MA3" / "random_graph_byz_high_conn" / "n100_k6"


img_path = pathlib.Path(__file__).parent.parent.parent / "results_img" 


def get_name(s):
    return s.split("_n")[0]
    
def extract_info(s):
    n = -1
    k = -1
    t = -1
    d = -1
    if "_n" in s:
        match = re.search(r'_n(\d+)', s)
        if match:
            n = int(match.group(1))
    if "_k" in s:
        match = re.search(r'_k(\d+)', s)
        if match:
            k = int(match.group(1))
    if "_t" in s:
        match = re.search(r'_t(\d+)', s)
        if match:
            t = int(match.group(1))
    if "_d" in s:
        match = re.search(r'_d(\d+)', s)
        if match:
            d = int(match.group(1))
    return n, k, t, d

def compute_confidence_bounds(values):
    values = np.array(values)
    if np.isnan(values).any():
        print("Warning: NaN values detected in the input array.")
    count = np.sum(~np.isnan(values))  # no axis
    mean = np.nanmean(values)
    std = np.nanstd(values, ddof=1)
    error = 2 * (std / np.sqrt(count))
    lower = mean - error
    upper = mean + error
    return mean, lower, upper


avg_dist = []
#-----------------------------------------------------------------------------------------------------------------------------
def plot_graph_compare_slim(data_dict, topologies, t_fix, n, k, output_name = ""):
    
    lw = 6      #linewidth
    fs = 32     #fontsize
    
    title1_avgdelnodes = f"avgCorrectDeliveredNodes n={n} k={k} (fixed t={t_fix})"
    title1_avgdeltime = f"avgDeliveryTime n={n} k={k} (fixed t={t_fix})"
    title1_totmsgsent = f"totalMsgSent n={n} k={k} (fixed t={t_fix})"
    xlabel1 = "Message Adversary Power (d)"
    ylabel_avgdelnodes = "AvgCorrectNodesDelivered"
    ylabel_avgdeltime = "AvgDeliveryTime"
    ylabel_totmsgsent = "totalMsgSent"
    
    total_nodes = n
    
    import matplotlib.pyplot as plt
    fig1, axs1 = plt.subplots(1, 1, figsize=(12,12),constrained_layout=True)

    x_d = [f"d={d}" for d in range(k)]
    x_t = [f"t={t}" for t in range(k)]

    
    epsilon = 0.01
    idx = 0
    # Subplot 1.1: for each t, plot over d
    for topology in topologies:
        y = []
        ci = []
        for d in range(k):
            topology_name = topologies[topology]
            if ((t_fix not in data_dict[topology_name]["avgDelTime"]) or (d not in data_dict[topology_name]["avgDelTime"][t_fix])):
                mean, lower, upper = np.nan, np.nan, np.nan
            else:
                mean, lower, upper = compute_confidence_bounds(data_dict[topology_name]["avgDelTime"][t_fix][d])
            y.append(mean)
            ci.append((lower, upper))
            
        lower_bounds = [ci[i][0] for i in range(k)]
        upper_bounds = [ci[i][1] for i in range(k)]
        x_shifted = [i + idx * epsilon for i in range(k)]  # Shift each line slightly
        short_name = topology_name
        short_name = short_name.replace("multi_wheel","ml")
        short_name = short_name.replace("generalized_wheel_center","gwc").replace("generalized_wheel","gw")
        short_name = short_name.replace("diamond","d").replace("pasted_tree","pt")
        short_name = short_name.replace("random_graph_pruned","rg_pruned")
        short_name = short_name.replace("random_graph_n100_k6_byz_high_conn","rg_high_n100_k6")
        short_name = short_name.replace("random_graph","rg")
        short_name = short_name.replace("_n24_k4","").replace("_n100_k6","").replace("_n99_k6","")
        axs1.plot(x_shifted, y, marker='o', label=f"{short_name}", color=color_map[topology_name], linewidth=lw)
        axs1.fill_between(x_shifted, lower_bounds, upper_bounds, alpha=0.2)
        idx += 1
    
    axs1.set_title(title1_avgdeltime, fontsize=fs)
    axs1.set_xlabel(xlabel1, fontsize=fs)
    axs1.set_ylabel(ylabel_avgdeltime, fontsize=fs)
    axs1.set_ylim(0,12)
    axs1.grid(True)
    axs1.legend()
    plt.xticks(fontsize=fs)  # x-axis tick numbers
    plt.yticks(fontsize=fs)  # y-axis tick numbers
    #plt.legend(fontsize=fs, ncol=2)
    plt.savefig(img_path/output_name.replace(".jpg","b.jpg"), dpi=100)
    plt.close()
    
    fig1, axs1 = plt.subplots(1, 1, figsize=(12,12),constrained_layout=True)
    epsilon = 0.01
    idx = 0
    # Subplot 2.1: for each t, plot over d
    for topology in topologies:
        y = []
        ci = []
        for d in range(k):
            topology_name = topologies[topology]
            if ((t_fix not in data_dict[topology_name]["avgDelTime"]) or (d not in data_dict[topology_name]["avgDelTime"][t_fix])):
                mean, lower, upper = np.nan, np.nan, np.nan
            else:
                mean, lower, upper = compute_confidence_bounds(data_dict[topology_name]["avgDelNodes"][t_fix][d])
            y.append(mean)
            ci.append((lower, upper))
        lower_bounds = [ci[i][0] for i in range(k)]
        upper_bounds = [ci[i][1] for i in range(k)]
        x_shifted = [i + idx * epsilon for i in range(k)]  # Shift each line slightly
        short_name = topology_name
        short_name = short_name.replace("multi_wheel","ml")
        short_name = short_name.replace("generalized_wheel_center","gwc").replace("generalized_wheel","gw")
        short_name = short_name.replace("random_graph_pruned","rg_pruned")
        short_name = short_name.replace("random_graph_n100_k6_delay","rg_delay_n100_k6")
        short_name = short_name.replace("random_graph_n100_k6_byz_high_conn","rg_high_n100_k6")
        short_name = short_name.replace("random_graph","rg")
        short_name = short_name.replace("_n24_k4","").replace("_n100_k6","").replace("_n99_k6","")
        axs1.plot(x_shifted, y, marker='o', label=f"{short_name}", color=color_map[topology_name], linewidth=lw)
        axs1.fill_between(x_shifted, lower_bounds, upper_bounds, alpha=0.2)
        idx += 1
    
    axs1.set_title(title1_avgdelnodes, fontsize=fs)
    axs1.set_xlabel(xlabel1, fontsize=fs)
    axs1.set_ylabel(ylabel_avgdelnodes, fontsize=fs)
    axs1.set_ylim(0,105)
    axs1.grid(True)
    axs1.legend()
    plt.xticks(fontsize=fs)  # x-axis tick numbers
    plt.yticks(fontsize=fs)  # y-axis tick numbers
    #plt.legend(fontsize=fs, ncol=2)
    plt.savefig(img_path/output_name.replace(".jpg","a.jpg"), dpi=100)
    plt.close()
    
    fig1, axs1 = plt.subplots(1, 1, figsize=(12,12),constrained_layout=True)
    epsilon = 0.01
    idx = 0
    # Subplot 3.1: for each t, plot over d
    for topology in topologies:
        y = []
        ci = []
        for d in range(k):
            topology_name = topologies[topology]
            if ((t_fix not in data_dict[topology_name]["totMsgSent"]) or (d not in data_dict[topology_name]["totMsgSent"][t_fix])):
                mean, lower, upper = np.nan, np.nan, np.nan
            else:
                mean, lower, upper = compute_confidence_bounds(data_dict[topology_name]["totMsgSent"][t_fix][d])
            y.append(mean)
            ci.append((lower, upper))
        lower_bounds = [ci[i][0] for i in range(k)]
        upper_bounds = [ci[i][1] for i in range(k)]
        x_shifted = [i + idx * epsilon for i in range(k)]  # Shift each line slightly
        short_name = topology_name
        short_name = short_name.replace("multi_wheel","ml")
        short_name = short_name.replace("generalized_wheel_center","gwc").replace("generalized_wheel","gw")
        short_name = short_name.replace("random_graph_pruned","rg_pruned")
        short_name = short_name.replace("random_graph_n100_k6_delay","rg_delay_n100_k6")
        short_name = short_name.replace("random_graph_n100_k6_byz_high_conn","rg_high_n100_k6")
        short_name = short_name.replace("random_graph","rg")
        short_name = short_name.replace("_n24_k4","").replace("_n100_k6","").replace("_n99_k6","")
        axs1.plot(x_shifted, y, marker='o', label=f"{short_name}", color=color_map[topology_name], linewidth=lw)
        axs1.fill_between(x_shifted, lower_bounds, upper_bounds, alpha=0.2)
        idx += 1
    
    axs1.set_title(title1_totmsgsent, fontsize=fs)
    axs1.set_xlabel(xlabel1, fontsize=fs)
    axs1.set_ylabel(ylabel_totmsgsent, fontsize=fs)
    axs1.set_ylim(0,500000)
    axs1.grid(True)
    axs1.legend()
    plt.xticks(fontsize=fs)  # x-axis tick numbers
    plt.yticks(fontsize=fs)  # y-axis tick numbers
    #plt.legend(fontsize=fs, ncol=2)
    plt.savefig(img_path/output_name.replace(".jpg","c.jpg"), dpi=100)
    plt.close()
#-----------------------------------------------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------------------------------------------
def plot_multiple_surfaces(list_M, k, list_names, title, gif_title):
    
    fs = 28
    
    # Create t and d axes (0 to 7)
    t = np.arange(k)
    d = np.arange(k)
    T, D = np.meshgrid(t, d)  # Build 2D grids for t and d

    # Build the plot
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111, projection='3d')
    
    new_list_name = []

    # Plot each surface
    for i, M in enumerate(list_M):
        topology_name = list_names[i]
        topology_name = topology_name.replace("multi_wheel","ml")
        topology_name = topology_name.replace("generalized_wheel_center","gwc").replace("generalized_wheel","gw")
        topology_name = topology_name.replace("diamond","d").replace("pasted_tree","pt")
        topology_name = topology_name.replace("random_graph_pruned","rg_pruned")
        topology_name = topology_name.replace("random_graph_n24_k4_delay","rg_delay_n24_k4")
        topology_name = topology_name.replace("random_graph_n100_k6_delay","rg_delay_n100_k6")
        topology_name = topology_name.replace("random_graph_n24_k4_byz_high_conn","rg_high_n24_k4")
        topology_name = topology_name.replace("random_graph_n100_k6_byz_high_conn","rg_high_n100_k6")
        topology_name = topology_name.replace("random_graph","rg")
        topology_name = topology_name.replace("_n24_k4","").replace("_n100_k6","").replace("n99_k6","")
        new_list_name.append(topology_name)
        ax.plot_surface(T, D, M, shade=False, alpha=0.8, label=topology_name, color=color_map[list_names[i]])  


    # Labels
    plot_title = title
    if title == "Total Msgs Sent":
        plot_title = "Total Msgs Sent"
    ax.set_xlabel('Message adversary power (d)', fontsize=fs, labelpad=20)
    ax.set_ylabel('Byzantine nodes (t)', fontsize=fs, labelpad=20)
    ax.set_zlabel(plot_title, fontsize=fs, labelpad=40)
    ax.zaxis.set_tick_params(labelsize=fs, pad=15)
    ax.set_title(title, fontsize=fs, y=1.10)
    ax.legend(new_list_name, fontsize=fs, loc='upper right', bbox_to_anchor=(1.10, 1), ncol=3)
    #ax.legend(list_names, loc='upper left', fontsize=fs)
    
    # Set axes limits
    from matplotlib.ticker import MultipleLocator
    ax.set_xlim(0, k)
    ax.set_ylim(0, k)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    if title == "Avg Delivery Time":
        ax.set_zlim(0, 12)
    if title == "Avg Delivery Nodes":
        ax.set_zlim(0, 105)
    if title == "Total Msgs Sent":
        ax.set_zlim(0,2000000)
        
    # Update function for animation
    def update(frame):
        ax.view_init(elev=10, azim=frame)

    # Create animation
    #ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=50)
    # Save as GIF
    #ani.save("results_img_3d/"+gif_title, writer='pillow', fps=20)
    
    ax.view_init(elev=10, azim=45)
    
    plt.xticks(fontsize=fs)  # x-axis tick numbers
    plt.yticks(fontsize=fs)  # y-axis tick numbers
    fig.subplots_adjust(left=0.1, right=0.90, bottom=0, top=0.95)
    plt.savefig("results_img_3d/"+gif_title.replace(".gif",".png"), dpi=100)
    #plt.savefig("results_img_3d/"+gif_title.replace(".gif",".png"), bbox_inches='tight', pad_inches=0.4, dpi=600)
    print(gif_title)
    #plt.show()
    plt.close()
#-----------------------------------------------------------------------------------------------------------------------------

    
# Extract the list of topology names (your dict values)
topology_labels = [
    "multi_wheel_n99_k6",
    "generalized_wheel_n100_k6",
    "generalized_wheel_byz_center_n100_k6",
    "random_graph_n100_k6",
    "random_graph_pruned_n100_k6",
    "random_graph_n100_k6_e500",
    "random_graph_n100_k6_e600",
    "random_graph_n100_k6_e700",
    "random_graph_n100_k6_byz_high_conn"
]

def get_distinct_colors(n, pastel_factor=0.0, cmap_name='hsv'):
    cmap = plt.get_cmap(cmap_name)
    hues = np.linspace(0, 1, n, endpoint=False)
    base_colors = cmap(hues)[:, :3]
    
    if pastel_factor > 0:
        # blend each color with white
        white = np.ones_like(base_colors)
        base_colors = (1 - pastel_factor) * base_colors + pastel_factor * white

    print(base_colors)
    return [tuple(c) for c in base_colors]

colors_9_hex = ["#d03f72",
                "#ca5340",
                "#c98542",
                "#999a3e",
                "#57a95b",
                "#45b2c4",
                "#7278cb",
                "#b85abe",
                "#be6c90"
                ]

colors = [mcolors.to_rgb(c) for c in colors_9_hex]
#colors = get_distinct_colors(len(topology_labels),0.2)

# Create the color map
color_map = {label: colors[i] for i, label in enumerate(topology_labels)}


ma1_topologies = {
	ma1_multi_wheel_n99_k6 : "multi_wheel_n99_k6",
	ma1_gener_wheel_n100_k6 : "generalized_wheel_n100_k6",
	ma1_gener_wheel_byz_center_n100_k6 : "generalized_wheel_byz_center_n100_k6",
	ma1_random_graph_n100_k6 : "random_graph_n100_k6",
	ma1_random_graph_pruned_n100_k6 : "random_graph_pruned_n100_k6",
	ma1_random_graph_n100_k6_e500 : "random_graph_n100_k6_e500",
	ma1_random_graph_n100_k6_e600 : "random_graph_n100_k6_e600",
	ma1_random_graph_n100_k6_e700 : "random_graph_n100_k6_e700",
	ma1_random_graph_n100_k6_byz_high_conn : "random_graph_n100_k6_byz_high_conn"
}

ma2_topologies = {
	ma2_multi_wheel_n99_k6 : "multi_wheel_n99_k6",
	ma2_gener_wheel_n100_k6 : "generalized_wheel_n100_k6",
	ma2_gener_wheel_byz_center_n100_k6 : "generalized_wheel_byz_center_n100_k6",
	ma2_random_graph_n100_k6 : "random_graph_n100_k6",
	ma2_random_graph_pruned_n100_k6 : "random_graph_pruned_n100_k6",
	ma2_random_graph_n100_k6_e500 : "random_graph_n100_k6_e500",
	ma2_random_graph_n100_k6_e600 : "random_graph_n100_k6_e600",
	ma2_random_graph_n100_k6_e700 : "random_graph_n100_k6_e700",
	ma2_random_graph_n100_k6_byz_high_conn : "random_graph_n100_k6_byz_high_conn"
}

ma3_topologies = {
	ma3_multi_wheel_n99_k6 : "multi_wheel_n99_k6",
	ma3_gener_wheel_n100_k6 : "generalized_wheel_n100_k6",
	ma3_gener_wheel_byz_center_n100_k6 : "generalized_wheel_byz_center_n100_k6",
	ma3_random_graph_n100_k6 : "random_graph_n100_k6",
	ma3_random_graph_pruned_n100_k6 : "random_graph_pruned_n100_k6",
	ma3_random_graph_n100_k6_e500 : "random_graph_n100_k6_e500",
	ma3_random_graph_n100_k6_e600 : "random_graph_n100_k6_e600",
	ma3_random_graph_n100_k6_e700 : "random_graph_n100_k6_e700",
	ma3_random_graph_n100_k6_byz_high_conn : "random_graph_n100_k6_byz_high_conn"
}
