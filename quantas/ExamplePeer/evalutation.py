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
multi_wheel_n24_k4 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "multipartite_wheel" / "n24_k4"
multi_wheel_n48_k8 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "multipartite_wheel" / "n48_k8"
multi_wheel_n99_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "multipartite_wheel" / "n99_k6"

gener_wheel_n24_k4 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "generalized_wheel" / "n24_k4"
gener_wheel_n48_k8 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "generalized_wheel" / "n48_k8"
gener_wheel_n100_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "generalized_wheel" / "n100_k6"

gener_wheel_byz_center_n24_k4 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "generalized_wheel_byz_center" / "n24_k4"
gener_wheel_byz_center_n48_k8 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "generalized_wheel_byz_center" / "n48_k8"
gener_wheel_byz_center_n100_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "generalized_wheel_byz_center" / "n100_k6"

diamond_k4 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "k-diamond"
pasted_tree_k4 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "k-pasted-tree"

random_graph_n24_k4 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "random_graph" / "n24_k4"
random_graph_n48_k8 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "random_graph" / "n48_k8"
random_graph_n100_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "random_graph" / "n100_k6"
random_graph_pruned_n24_k4 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "random_graph_pruned" / "n24_k4"
random_graph_pruned_n48_k8 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "random_graph_pruned" / "n48_k8"
random_graph_pruned_n100_k6 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "random_graph_pruned" / "n100_k6"

random_graph_n100_k6_e500 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "random_graph_half_edges" / "n100_k6_e500"
random_graph_n100_k6_e600 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "random_graph_half_edges" / "n100_k6_e600"
random_graph_n100_k6_e700 = pathlib.Path(__file__).parent.parent.parent / "results" / "base" / "random_graph_half_edges" / "n100_k6_e700"


# delays tests
random_graph_n24_k4_delay = pathlib.Path(__file__).parent.parent.parent / "results" / "delay" / "normal" / "n24_k4"
random_graph_pruned_n24_k4_delay = pathlib.Path(__file__).parent.parent.parent / "results" / "delay" / "pruned" / "n24_k4"
random_graph_n48_k8_delay = pathlib.Path(__file__).parent.parent.parent / "results" / "delay" / "normal" / "n48_k8"
random_graph_pruned_n48_k8_delay = pathlib.Path(__file__).parent.parent.parent / "results" / "delay" / "pruned" / "n48_k8"

# coin flip tests
random_graph_n24_k4_coin_flip = pathlib.Path(__file__).parent.parent.parent / "results" / "coin_flip" / "normal" / "n24_k4"
random_graph_pruned_n24_k4_coin_flip = pathlib.Path(__file__).parent.parent.parent / "results" / "coin_flip" / "pruned" / "n24_k4"
random_graph_n48_k8_coin_flip = pathlib.Path(__file__).parent.parent.parent / "results" / "coin_flip" / "normal" / "n48_k8"
random_graph_pruned_n48_k8_coin_flip = pathlib.Path(__file__).parent.parent.parent / "results" / "coin_flip" / "pruned" / "n48_k8"

# high conn first
random_graph_n24_k4_byz_high_conn = pathlib.Path(__file__).parent.parent.parent / "results" / "byz_high_conn" / "normal" / "n24_k4"
random_graph_pruned_n24_k4_byz_high_conn = pathlib.Path(__file__).parent.parent.parent / "results" / "byz_high_conn" / "pruned" / "n24_k4"
random_graph_n48_k8_byz_high_conn = pathlib.Path(__file__).parent.parent.parent / "results" / "byz_high_conn" / "normal" / "n48_k8"
random_graph_pruned_n48_k8_byz_high_conn = pathlib.Path(__file__).parent.parent.parent / "results" / "byz_high_conn" / "pruned" / "n48_k8"
random_graph_n100_k6_byz_high_conn = pathlib.Path(__file__).parent.parent.parent / "results" / "byz_high_conn" / "normal" / "n100_k6"
random_graph_pruned_n100_k6_byz_high_conn = pathlib.Path(__file__).parent.parent.parent / "results" / "byz_high_conn" / "pruned" / "n100_k6"

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

def plot_graph_compare_slim(data_dict, topologies, t_fix, n, k, output_name = ""):
    
    lw = 6      #linewidth
    fs = 32     #fontsize
    
    title1_avgdelnodes = f"avgCorrectDeliveredNodes n={n} k={k} (fixed t={t_fix})"
    title1_avgdeltime = f"avgDeliveryTime n={n} k={k} (fixed t={t_fix})"
    title1_totmsgsent = f"totalMsgSent n={n} k={k} (fixed t={t_fix})"
    xlabel1 = "Message Adversary Power (d)"
    ylabel_avgdelnodes = "AvgCorrectNodesDelivered"
    ylabel_avgdeltime = "AvgDeliveryTime"
    ylabel_totmsgsent = "totalMsgSent (millions)"
    
    total_nodes = n
    
    import matplotlib.pyplot as plt
    #plt.rcParams.update({'font.size': 8})
    #plt.rcParams.update({'figure.titlesize': 10})
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
        short_name = short_name.replace("random_graph_n24_k4_delay","rg_delay_n24_k4")
        short_name = short_name.replace("random_graph_n100_k6_delay","rg_delay_n100_k6")
        short_name = short_name.replace("random_graph_n24_k4_byz_high_conn","rg_high_n24_k4")
        short_name = short_name.replace("random_graph_n100_k6_byz_high_conn","rg_high_n100_k6")
        short_name = short_name.replace("random_graph","rg")
        short_name = short_name.replace("_n24_k4","").replace("_n100_k6","").replace("n99_k6","")
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
    plt.legend(fontsize=fs, ncol=2)
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
        short_name = short_name.replace("diamond","d").replace("pasted_tree","pt")
        short_name = short_name.replace("random_graph_pruned","rg_pruned")
        short_name = short_name.replace("random_graph_n24_k4_delay","rg_delay_n24_k4")
        short_name = short_name.replace("random_graph_n100_k6_delay","rg_delay_n100_k6")
        short_name = short_name.replace("random_graph_n24_k4_byz_high_conn","rg_high_n24_k4")
        short_name = short_name.replace("random_graph_n100_k6_byz_high_conn","rg_high_n100_k6")
        short_name = short_name.replace("random_graph","rg")
        short_name = short_name.replace("_n24_k4","").replace("_n100_k6","").replace("n99_k6","")
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
    plt.legend(fontsize=fs, ncol=2)
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
        short_name = short_name.replace("diamond","d").replace("pasted_tree","pt")
        short_name = short_name.replace("random_graph_pruned","rg_pruned")
        short_name = short_name.replace("random_graph_n24_k4_delay","rg_delay_n24_k4")
        short_name = short_name.replace("random_graph_n100_k6_delay","rg_delay_n100_k6")
        short_name = short_name.replace("random_graph_n24_k4_byz_high_conn","rg_high_n24_k4")
        short_name = short_name.replace("random_graph_n100_k6_byz_high_conn","rg_high_n100_k6")
        short_name = short_name.replace("random_graph","rg")
        short_name = short_name.replace("_n24_k4","").replace("_n100_k6","").replace("n99_k6","")
        axs1.plot(x_shifted, y, marker='o', label=f"{short_name}", color=color_map[topology_name], linewidth=lw)
        axs1.fill_between(x_shifted, lower_bounds, upper_bounds, alpha=0.2)
        idx += 1
    
    axs1.set_title(title1_totmsgsent, fontsize=fs)
    axs1.set_xlabel(xlabel1, fontsize=fs)
    axs1.set_ylabel(ylabel_totmsgsent, fontsize=fs)
    axs1.set_ylim(0,2100000)
    axs1.grid(True)
    axs1.legend()
    plt.xticks(fontsize=fs)  # x-axis tick numbers
    plt.yticks(fontsize=fs)  # y-axis tick numbers
    plt.legend(fontsize=fs, ncol=2)
    plt.savefig(img_path/output_name.replace(".jpg","c.jpg"), dpi=100)
    plt.close()
    
    
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
        plot_title = "Total Msgs Sent (million)"
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
    
# Extract the list of topology names (your dict values)
topology_labels = [
    "multi_wheel_n24_k4", 
    "multi_wheel_n48_k8",
    "multi_wheel_n99_k6",
    "generalized_wheel_n24_k4",
    "generalized_wheel_n48_k8",
    "generalized_wheel_n100_k6",
    "generalized_wheel_byz_center_n24_k4",
    "generalized_wheel_byz_center_n48_k8",
    "generalized_wheel_byz_center_n100_k6",
    "diamond_n24_k4",
    "pasted_tree_n24_k4",
    "random_graph_n24_k4",
    "random_graph_n48_k8",
    "random_graph_n100_k6",
    
    "random_graph_pruned_n24_k4",
    "random_graph_pruned_n48_k8",
    "random_graph_pruned_n100_k6",
    
    "random_graph_n100_k6_e500",
    "random_graph_n100_k6_e600",
    "random_graph_n100_k6_e700",
    
    "random_graph_n24_k4_delay",
    "random_graph_pruned_n24_k4_delay",
    "random_graph_n48_k8_delay",
    "random_graph_pruned_n48_k8_delay",
    "random_graph_n24_k4_byz_high_conn",
    "random_graph_n48_k8_byz_high_conn",
    "random_graph_n100_k6_byz_high_conn",
    "random_graph_pruned_n24_k4_byz_high_conn",
    "random_graph_pruned_n48_k8_byz_high_conn",
    "random_graph_pruned_n100_k6_byz_high_conn"
]

""" 
# Use tab20 and extend with Set3 if needed
tab_colors = plt.get_cmap('tab20').colors
set_colors = plt.get_cmap('Set3').colors
all_colors = list(tab_colors) + list(set_colors)


# Make sure we have enough colors
assert len(topology_labels) <= len(all_colors)

# Create the color map
color_map = {label: all_colors[i] for i, label in enumerate(topology_labels)} 
"""

topology_labels = [
    "multi_wheel_n24_k4", 
    "multi_wheel_n99_k6",
    "generalized_wheel_n24_k4",
    "generalized_wheel_n100_k6",
    "generalized_wheel_byz_center_n24_k4",
    "generalized_wheel_byz_center_n100_k6",
    "diamond_n24_k4",
    "pasted_tree_n24_k4",
    "random_graph_n24_k4",
    "random_graph_n100_k6",
    
    "random_graph_pruned_n24_k4",
    "random_graph_pruned_n100_k6",
    
    "random_graph_n100_k6_e500",
    "random_graph_n100_k6_e600",
    "random_graph_n100_k6_e700",
    
    "random_graph_n24_k4_delay",
    "random_graph_pruned_n24_k4_delay",
    "random_graph_n24_k4_byz_high_conn",
    "random_graph_n100_k6_byz_high_conn",
    "random_graph_pruned_n24_k4_byz_high_conn",
    "random_graph_pruned_n100_k6_byz_high_conn"
]

# Generate 30+ perceptually distinct colors
colors = distinctipy.get_colors(len(topology_labels))

# Create the color map
color_map = {label: colors[i] for i, label in enumerate(topology_labels)}


topologies = {
    multi_wheel_n24_k4 : "multi_wheel_n24_k4", 
    multi_wheel_n48_k8 : "multi_wheel_n48_k8",
    multi_wheel_n99_k6 : "multi_wheel_n99_k6",
    gener_wheel_n24_k4 : "generalized_wheel_n24_k4",
    gener_wheel_n48_k8 : "generalized_wheel_n48_k8",
    gener_wheel_n100_k6 : "generalized_wheel_n100_k6",
    gener_wheel_byz_center_n24_k4 : "generalized_wheel_byz_center_n24_k4",
    gener_wheel_byz_center_n48_k8 : "generalized_wheel_byz_center_n48_k8",
    gener_wheel_byz_center_n100_k6 : "generalized_wheel_byz_center_n100_k6",
    diamond_k4 : "diamond_n24_k4",
    pasted_tree_k4 : "pasted_tree_n24_k4",
    random_graph_n24_k4 : "random_graph_n24_k4",
    random_graph_n48_k8 : "random_graph_n48_k8",
    random_graph_n100_k6 : "random_graph_n100_k6",

    random_graph_pruned_n24_k4 : "random_graph_pruned_n24_k4",
    random_graph_pruned_n48_k8 : "random_graph_pruned_n48_k8",
    random_graph_pruned_n100_k6 : "random_graph_pruned_n100_k6",
    
    random_graph_n100_k6_e500 : "random_graph_n100_k6_e500",
    random_graph_n100_k6_e600 : "random_graph_n100_k6_e600",
    random_graph_n100_k6_e700 : "random_graph_n100_k6_e700",

    random_graph_n24_k4_delay : "random_graph_n24_k4_delay",
    random_graph_pruned_n24_k4_delay : "random_graph_pruned_n24_k4_delay",
    random_graph_n48_k8_delay : "random_graph_n48_k8_delay",
    random_graph_pruned_n48_k8_delay : "random_graph_pruned_n48_k8_delay",
    
    random_graph_n24_k4_byz_high_conn : "random_graph_n24_k4_byz_high_conn",
    random_graph_n48_k8_byz_high_conn : "random_graph_n48_k8_byz_high_conn",
    random_graph_n100_k6_byz_high_conn : "random_graph_n100_k6_byz_high_conn",
    random_graph_pruned_n24_k4_byz_high_conn : "random_graph_pruned_n24_k4_byz_high_conn",
    random_graph_pruned_n48_k8_byz_high_conn : "random_graph_pruned_n48_k8_byz_high_conn",
    random_graph_pruned_n100_k6_byz_high_conn : "random_graph_pruned_n100_k6_byz_high_conn",
}

topologies_compare_n24 = {
    multi_wheel_n24_k4 : "multi_wheel_n24_k4", 
    gener_wheel_n24_k4 : "generalized_wheel_n24_k4",
    gener_wheel_byz_center_n24_k4 : "generalized_wheel_byz_center_n24_k4",
    diamond_k4 : "diamond_n24_k4",
    pasted_tree_k4 : "pasted_tree_n24_k4",
    random_graph_n24_k4 : "random_graph_n24_k4",
    random_graph_pruned_n24_k4 : "random_graph_pruned_n24_k4",
    random_graph_n24_k4_delay : "random_graph_n24_k4_delay",
    random_graph_n24_k4_byz_high_conn : "random_graph_n24_k4_byz_high_conn",
}
dict_compare_n24 = {}

topologies_compare_n48 = {
    multi_wheel_n48_k8 : "multi_wheel_n48_k8",
    gener_wheel_n48_k8 : "generalized_wheel_n48_k8",
    gener_wheel_byz_center_n48_k8 : "generalized_wheel_byz_center_n48_k8",
    random_graph_n48_k8 : "random_graph_n48_k8",
    random_graph_pruned_n48_k8 : "random_graph_pruned_n48_k8",
    random_graph_n48_k8_delay : "random_graph_n48_k8_delay",
    random_graph_n48_k8_byz_high_conn : "random_graph_n48_k8_byz_high_conn",
}
dict_compare_n48 = {}

topologies_compare_n100 = {
    multi_wheel_n99_k6 : "multi_wheel_n99_k6",
    gener_wheel_n100_k6 : "generalized_wheel_n100_k6",
    gener_wheel_byz_center_n100_k6 : "generalized_wheel_byz_center_n100_k6",
    random_graph_n100_k6 : "random_graph_n100_k6",
    random_graph_pruned_n100_k6 : "random_graph_pruned_n100_k6",
    random_graph_n100_k6_byz_high_conn : "random_graph_n100_k6_byz_high_conn",
    
    random_graph_n100_k6_e500 : "random_graph_n100_k6_e500",
    random_graph_n100_k6_e600 : "random_graph_n100_k6_e600",
    random_graph_n100_k6_e700 : "random_graph_n100_k6_e700",
    
}
dict_compare_n100 = {}

topologies_compare_gen_wheel = {
    gener_wheel_n24_k4 : "generalized_wheel_n24_k4",
    gener_wheel_n48_k8 : "generalized_wheel_n48_k8",
    gener_wheel_n100_k6 : "generalized_wheel_n100_k6",
}
dict_compare_gen_wheel = {}

topologies_compare_gen_wheel_bc = {
    gener_wheel_byz_center_n24_k4 : "generalized_wheel_byz_center_n24_k4",
    gener_wheel_byz_center_n48_k8 : "generalized_wheel_byz_center_n48_k8",
    gener_wheel_byz_center_n100_k6 : "generalized_wheel_byz_center_n100_k6",
}
dict_compare_gen_wheel_bc = {}

topologies_compare_multi_wheel = {
    multi_wheel_n24_k4 : "multi_wheel_n24_k4", 
    multi_wheel_n48_k8 : "multi_wheel_n48_k8",
    multi_wheel_n99_k6 : "multi_wheel_n99_k6",
}
dict_compare_multi_wheel = {}

topologies_compare_random_graph = {
    random_graph_n24_k4 : "random_graph_n24_k4",
    random_graph_n48_k8 : "random_graph_n48_k8",
    random_graph_n100_k6 : "random_graph_n100_k6", 
    random_graph_pruned_n24_k4 : "random_graph_pruned_n24_k4",
    random_graph_pruned_n48_k8 : "random_graph_pruned_n48_k8",
    random_graph_pruned_n100_k6 : "random_graph_pruned_n100_k6", 
    random_graph_n100_k6_e500 : "random_graph_n100_k6_e500",
    random_graph_n100_k6_e600 : "random_graph_n100_k6_e600",
    random_graph_n100_k6_e700 : "random_graph_n100_k6_e700", 
}
dict_compare_random_graph = {}

topologies_compare_random_graph_ndh = {
    random_graph_n48_k8 : "random_graph_n48_k8",
    random_graph_n48_k8_delay : "random_graph_n48_k8_delay",
    random_graph_n48_k8_byz_high_conn : "random_graph_n48_k8_byz_high_conn",
    random_graph_pruned_n48_k8 : "random_graph_pruned_n48_k8",
}
dict_compare_random_graph_ndh = {}
            


for topology in topologies:
    l = os.listdir(topology)
    l.sort()
    maxDeliveryTime = {}
    avgDeliveryTime = {}
    avgDeliveryNodes = {}
    totalMsgSent = {}
    
    for file in l:
        n, k, t, d = extract_info(file)
        if t not in avgDeliveryNodes:
            avgDeliveryNodes[t] = {}
        if t not in avgDeliveryTime:
            avgDeliveryTime[t] = {}
        if t not in maxDeliveryTime:
            maxDeliveryTime[t] = {}
        if t not in totalMsgSent:
            totalMsgSent[t] = {}
        
        avgDeliveryNodes[t][d] = []
        avgDeliveryTime[t][d] = []
        maxDeliveryTime[t][d] = []
        totalMsgSent[t][d] = []
        with open(topology/file,"r") as f:
            data = json.load(f)
            for test in data["tests"]:
                avgDeliveryNodes[t][d].append(data["tests"][test]["avgDeliveryNodes"])
                avgDeliveryTime[t][d].append(data["tests"][test]["avgDeliveryTime"])
                maxDeliveryTime[t][d].append(data["tests"][test]["maxDeliveryTime"])
                totalMsgSent[t][d].append(data["tests"][test]["totalMsgSent"])
        
    
    dict_all = {}
    dict_all["avgDelTime"] = avgDeliveryTime
    dict_all["avgDelNodes"] = avgDeliveryNodes
    dict_all["maxDelTime"] = maxDeliveryTime
    dict_all["totMsgSent"] = totalMsgSent

    if ("_n24_k4" in topologies[topology] ) and ("coin_flip" not in topologies[topology]):
        dict_compare_n24[topologies[topology]] = {}
        dict_compare_n24[topologies[topology]]["avgDelTime"] = avgDeliveryTime
        dict_compare_n24[topologies[topology]]["avgDelNodes"] = avgDeliveryNodes
        dict_compare_n24[topologies[topology]]["maxDelTime"] = maxDeliveryTime
        dict_compare_n24[topologies[topology]]["totMsgSent"] = totalMsgSent
    if ("_n48_k8" in topologies[topology] ) and ("coin_flip" not in topologies[topology]):
        dict_compare_n48[topologies[topology]] = {}
        dict_compare_n48[topologies[topology]]["avgDelTime"] = avgDeliveryTime
        dict_compare_n48[topologies[topology]]["avgDelNodes"] = avgDeliveryNodes
        dict_compare_n48[topologies[topology]]["maxDelTime"] = maxDeliveryTime
        dict_compare_n48[topologies[topology]]["totMsgSent"] = totalMsgSent
    if (("_n100_k6" in topologies[topology] ) or ("_n99_k6" in topologies[topology])) and ("coin_flip" not in topologies[topology]):
        dict_compare_n100[topologies[topology]] = {}
        dict_compare_n100[topologies[topology]]["avgDelTime"] = avgDeliveryTime
        dict_compare_n100[topologies[topology]]["avgDelNodes"] = avgDeliveryNodes
        dict_compare_n100[topologies[topology]]["maxDelTime"] = maxDeliveryTime
        dict_compare_n100[topologies[topology]]["totMsgSent"] = totalMsgSent
    if ("generalized_wheel_n" in topologies[topology]):
        dict_compare_gen_wheel[topologies[topology]] = {}
        dict_compare_gen_wheel[topologies[topology]]["avgDelTime"] = avgDeliveryTime
        dict_compare_gen_wheel[topologies[topology]]["avgDelNodes"] = avgDeliveryNodes
        dict_compare_gen_wheel[topologies[topology]]["maxDelTime"] = maxDeliveryTime
        dict_compare_gen_wheel[topologies[topology]]["totMsgSent"] = totalMsgSent
    if ("generalized_wheel_byz_center_n" in topologies[topology]):
        dict_compare_gen_wheel_bc[topologies[topology]] = {}
        dict_compare_gen_wheel_bc[topologies[topology]]["avgDelTime"] = avgDeliveryTime
        dict_compare_gen_wheel_bc[topologies[topology]]["avgDelNodes"] = avgDeliveryNodes
        dict_compare_gen_wheel_bc[topologies[topology]]["maxDelTime"] = maxDeliveryTime
        dict_compare_gen_wheel_bc[topologies[topology]]["totMsgSent"] = totalMsgSent
    if ("multi_wheel_n" in topologies[topology]):
        dict_compare_multi_wheel[topologies[topology]] = {}
        dict_compare_multi_wheel[topologies[topology]]["avgDelTime"] = avgDeliveryTime
        dict_compare_multi_wheel[topologies[topology]]["avgDelNodes"] = avgDeliveryNodes
        dict_compare_multi_wheel[topologies[topology]]["maxDelTime"] = maxDeliveryTime
        dict_compare_multi_wheel[topologies[topology]]["totMsgSent"] = totalMsgSent
    if ("random_graph" in topologies[topology]) and ("high_conn" not in topologies[topology]) and ("delay" not in topologies[topology]):
        dict_compare_random_graph[topologies[topology]] = {}
        dict_compare_random_graph[topologies[topology]]["avgDelTime"] = avgDeliveryTime
        dict_compare_random_graph[topologies[topology]]["avgDelNodes"] = avgDeliveryNodes
        dict_compare_random_graph[topologies[topology]]["maxDelTime"] = maxDeliveryTime
        dict_compare_random_graph[topologies[topology]]["totMsgSent"] = totalMsgSent
    if ("random_graph_n48_k8" in topologies[topology]) or ("random_graph_pruned_n48_k8" in topologies[topology]):
        dict_compare_random_graph_ndh[topologies[topology]] = {}
        dict_compare_random_graph_ndh[topologies[topology]]["avgDelTime"] = avgDeliveryTime
        dict_compare_random_graph_ndh[topologies[topology]]["avgDelNodes"] = avgDeliveryNodes
        dict_compare_random_graph_ndh[topologies[topology]]["maxDelTime"] = maxDeliveryTime
        dict_compare_random_graph_ndh[topologies[topology]]["totMsgSent"] = totalMsgSent
    

plot_graph_compare_slim(dict_compare_n24, topologies_compare_n24, 3, 24,4, f"compare_topologies_n24_k4_t3.jpg")
#plot_graph_compare_slim(dict_compare_gen_wheel, topologies_compare_gen_wheel, 3, 24,4, f"compare_topologies_gen_wheel_t3.jpg")
#plot_graph_compare_slim(dict_compare_gen_wheel_bc, topologies_compare_gen_wheel_bc, 3, 24,4, f"compare_topologies_gen_wheel_byz_center_t3.jpg")
#plot_graph_compare_slim(dict_compare_multi_wheel, topologies_compare_multi_wheel, 3, 24,4, f"compare_topologies_multi_wheel_t3.jpg")
#plot_graph_compare_slim(dict_compare_random_graph, topologies_compare_random_graph, 3, 24,4, f"compare_topologies_random_graph_t3.jpg")
#print("----------------------------------")
#plot_graph_compare_slim(dict_compare_n48, topologies_compare_n48, 7, 48,8, f"compare_topologies_n48_k8_t7.jpg")
#plot_graph_compare_slim(dict_compare_random_graph_ndh, topologies_compare_random_graph_ndh, 7, 48,8, f"compare_topologies_random_graph_normVSdelayVShighconn_n48_k8_t7.jpg")
print("----------------------------------")
plot_graph_compare_slim(dict_compare_n100, topologies_compare_n100, 5, 100,6,f"compare_topologies_n100_k6_t5.jpg")




list_M_avgDelTime = []
list_M_avgDelNode = []
list_M_totalMsgs = []
list_names = []
k = 4
for topology in topologies_compare_n24:
    l = os.listdir(topology)
    l.sort()
    
    avgDeliveryNodes = np.full((k,k), np.nan)
    avgDeliveryTime = np.full((k,k), np.nan)
    totalMsgSent = np.full((k,k), np.nan)
    
    for file in l:
        n, k_read, t, d = extract_info(file)
        x = []
        y = []
        z = []
        with open(topology/file,"r") as f:
            data = json.load(f)
            for test in data["tests"]:
                x.append(data["tests"][test]["avgDeliveryNodes"])
                y.append(data["tests"][test]["avgDeliveryTime"])
                z.append(data["tests"][test]["totalMsgSent"])
        
        avgDeliveryNodes[t][d] = np.mean(x)
        avgDeliveryTime[t][d] = np.mean(y)
        totalMsgSent[t][d] = np.mean(z)
        
    list_M_avgDelTime.append(np.array(avgDeliveryTime))
    list_M_avgDelNode.append(np.array(avgDeliveryNodes))
    list_M_totalMsgs.append(np.array(totalMsgSent))
    list_names.append(topologies_compare_n24[topology])

plot_multiple_surfaces(list_M_avgDelTime, k, list_names, "Avg Delivery Time", "n24_k4_AvgDeliveryTime.gif")
plot_multiple_surfaces(list_M_avgDelNode, k, list_names, "Avg Delivery Nodes", "n24_k4_AvgDeliveryNodes.gif")
plot_multiple_surfaces(list_M_totalMsgs, k, list_names, "Total Msgs Sent", "n24_k4_TotalMsgSent.gif")


list_M_avgDelTime = []
list_M_avgDelNode = []
list_M_totalMsgs = []
list_names = []
k = 8
for topology in topologies_compare_n48:
    l = os.listdir(topology)
    l.sort()
    
    avgDeliveryNodes = np.full((k,k), np.nan)
    avgDeliveryTime = np.full((k,k), np.nan)
    totalMsgSent = np.full((k,k), np.nan)
    
    for file in l:
        n, k_read, t, d = extract_info(file)
        x = []
        y = []
        z = []
        with open(topology/file,"r") as f:
            data = json.load(f)
            for test in data["tests"]:
                x.append(data["tests"][test]["avgDeliveryNodes"])
                y.append(data["tests"][test]["avgDeliveryTime"])
                z.append(data["tests"][test]["totalMsgSent"])
        
        avgDeliveryNodes[t][d] = np.mean(x)
        avgDeliveryTime[t][d] = np.mean(y)
        totalMsgSent[t][d] = np.mean(z)
        
    list_M_avgDelTime.append(np.array(avgDeliveryTime))
    list_M_avgDelNode.append(np.array(avgDeliveryNodes))
    list_M_totalMsgs.append(np.array(totalMsgSent))
    list_names.append(topologies_compare_n48[topology])
    
#plot_multiple_surfaces(list_M_avgDelTime, k, list_names, "Avg Delivery Time", "n48_k8_AvgDeliveryTime.gif")
#plot_multiple_surfaces(list_M_avgDelNode, k, list_names, "Avg Delivery Nodes", "n48_k8_AvgDeliveryNodes.gif")
#plot_multiple_surfaces(list_M_totalMsgs, k, list_names, "Total Msgs Sent", "n48_k8_TotalMsgSent.gif")
    

list_M_avgDelTime = []
list_M_avgDelNode = []
list_M_totalMsgs = []
list_names = []
k = 6
for topology in topologies_compare_n100:
    l = os.listdir(topology)
    l.sort()
    
    avgDeliveryNodes = np.full((k,k), np.nan)
    avgDeliveryTime = np.full((k,k), np.nan)
    totalMsgSent = np.full((k,k), np.nan)
    
    for file in l:
        n, k_read, t, d = extract_info(file)
        x = []
        y = []
        z = []
        with open(topology/file,"r") as f:
            data = json.load(f)
            for test in data["tests"]:
                x.append(data["tests"][test]["avgDeliveryNodes"])
                y.append(data["tests"][test]["avgDeliveryTime"])
                z.append(data["tests"][test]["totalMsgSent"])
        
        avgDeliveryNodes[t][d] = np.mean(x)
        avgDeliveryTime[t][d] = np.mean(y)
        totalMsgSent[t][d] = np.mean(z)
        
    list_M_avgDelTime.append(np.array(avgDeliveryTime))
    list_M_avgDelNode.append(np.array(avgDeliveryNodes))
    list_M_totalMsgs.append(np.array(totalMsgSent))
    list_names.append(topologies_compare_n100[topology])
    
plot_multiple_surfaces(list_M_avgDelTime, k, list_names, "Avg Delivery Time", "n100_k6_AvgDeliveryTime.gif")
plot_multiple_surfaces(list_M_avgDelNode, k, list_names, "Avg Delivery Nodes", "n100_k6_AvgDeliveryNodes.gif")
plot_multiple_surfaces(list_M_totalMsgs, k, list_names, "Total Msgs Sent", "n100_k6_TotalMsgSent.gif")


list_M_avgDelTime = []
list_M_avgDelNode = []
list_M_totalMsgs = []
list_names = []
k = 8
for topology in topologies_compare_multi_wheel:
    l = os.listdir(topology)
    l.sort()
    
    avgDeliveryNodes = np.full((k,k), np.nan)
    avgDeliveryTime = np.full((k,k), np.nan)
    totalMsgSent = np.full((k,k), np.nan)
    
    for file in l:
        n, k_read, t, d = extract_info(file)
        x = []
        y = []
        z = []
        with open(topology/file,"r") as f:
            data = json.load(f)
            for test in data["tests"]:
                x.append(data["tests"][test]["avgDeliveryNodes"])
                y.append(data["tests"][test]["avgDeliveryTime"])
                z.append(data["tests"][test]["totalMsgSent"])
        
        avgDeliveryNodes[t][d] = np.mean(x)
        avgDeliveryTime[t][d] = np.mean(y)
        totalMsgSent[t][d] = np.mean(z)
        
    list_M_avgDelTime.append(np.array(avgDeliveryTime))
    list_M_avgDelNode.append(np.array(avgDeliveryNodes))
    list_M_totalMsgs.append(np.array(totalMsgSent))
    list_names.append(topologies_compare_multi_wheel[topology])
    
#plot_multiple_surfaces(list_M_avgDelTime, k, list_names, "Avg Delivery Time", "n24vsn48_multi_wheel_AvgDeliveryTime.gif")
#plot_multiple_surfaces(list_M_avgDelNode, k, list_names, "Avg Delivery Nodes", "n24vsn48_multi_wheel_AvgDeliveryNodes.gif")
#plot_multiple_surfaces(list_M_totalMsgs, k, list_names, "Total Msgs Sent", "n24vsn48_multi_wheel_TotalMsgSent.gif")


list_M_avgDelTime = []
list_M_avgDelNode = []
list_M_totalMsgs = []
list_names = []
k = 8
for topology in topologies_compare_gen_wheel:
    l = os.listdir(topology)
    l.sort()
    
    avgDeliveryNodes = np.full((k,k), np.nan)
    avgDeliveryTime = np.full((k,k), np.nan)
    totalMsgSent = np.full((k,k), np.nan)
    
    for file in l:
        n, k_read, t, d = extract_info(file)
        x = []
        y = []
        z = []
        with open(topology/file,"r") as f:
            data = json.load(f)
            for test in data["tests"]:
                x.append(data["tests"][test]["avgDeliveryNodes"])
                y.append(data["tests"][test]["avgDeliveryTime"])
                z.append(data["tests"][test]["totalMsgSent"])
        
        avgDeliveryNodes[t][d] = np.mean(x)
        avgDeliveryTime[t][d] = np.mean(y)
        totalMsgSent[t][d] = np.mean(z)
        
    list_M_avgDelTime.append(np.array(avgDeliveryTime))
    list_M_avgDelNode.append(np.array(avgDeliveryNodes))
    list_M_totalMsgs.append(np.array(totalMsgSent))
    list_names.append(topologies_compare_gen_wheel[topology])
    
#plot_multiple_surfaces(list_M_avgDelTime, k, list_names, "Avg Delivery Time", "n24vsn48_generalized_wheel_AvgDeliveryTime.gif")
#plot_multiple_surfaces(list_M_avgDelNode, k, list_names, "Avg Delivery Nodes", "n24vsn48_generalized_wheel_AvgDeliveryNodes.gif")
#plot_multiple_surfaces(list_M_totalMsgs, k, list_names, "Total Msgs Sent", "n24vsn48_generalized_wheel_TotalMsgSent.gif")

list_M_avgDelTime = []
list_M_avgDelNode = []
list_M_totalMsgs = []
list_names = []
k = 8
for topology in topologies_compare_gen_wheel_bc:
    l = os.listdir(topology)
    l.sort()
    
    avgDeliveryNodes = np.full((k,k), np.nan)
    avgDeliveryTime = np.full((k,k), np.nan)
    totalMsgSent = np.full((k,k), np.nan)
    
    for file in l:
        n, k_read, t, d = extract_info(file)
        x = []
        y = []
        z = []
        with open(topology/file,"r") as f:
            data = json.load(f)
            for test in data["tests"]:
                x.append(data["tests"][test]["avgDeliveryNodes"])
                y.append(data["tests"][test]["avgDeliveryTime"])
                z.append(data["tests"][test]["totalMsgSent"])
        
        avgDeliveryNodes[t][d] = np.mean(x)
        avgDeliveryTime[t][d] = np.mean(y)
        totalMsgSent[t][d] = np.mean(z)
        
    list_M_avgDelTime.append(np.array(avgDeliveryTime))
    list_M_avgDelNode.append(np.array(avgDeliveryNodes))
    list_M_totalMsgs.append(np.array(totalMsgSent))
    list_names.append(topologies_compare_gen_wheel_bc[topology])
    
#plot_multiple_surfaces(list_M_avgDelTime, k, list_names, "Avg Delivery Time", "n24vsn48_generalized_wheel_byz_center_AvgDeliveryTime.gif")
#plot_multiple_surfaces(list_M_avgDelNode, k, list_names, "Avg Delivery Nodes", "n24vsn48_generalized_wheel_byz_center_AvgDeliveryNodes.gif")
#plot_multiple_surfaces(list_M_totalMsgs, k, list_names, "Total Msgs Sent", "n24vsn48_generalized_wheel_byz_center_TotalMsgSent.gif")

list_M_avgDelTime = []
list_M_avgDelNode = []
list_M_totalMsgs = []
list_names = []
k = 8
for topology in topologies_compare_random_graph:
    l = os.listdir(topology)
    l.sort()
    
    avgDeliveryNodes = np.full((k,k), np.nan)
    avgDeliveryTime = np.full((k,k), np.nan)
    totalMsgSent = np.full((k,k), np.nan)
    
    for file in l:
        n, k_read, t, d = extract_info(file)
        x = []
        y = []
        z = []
        with open(topology/file,"r") as f:
            data = json.load(f)
            for test in data["tests"]:
                x.append(data["tests"][test]["avgDeliveryNodes"])
                y.append(data["tests"][test]["avgDeliveryTime"])
                z.append(data["tests"][test]["totalMsgSent"])
        
        avgDeliveryNodes[t][d] = np.mean(x)
        avgDeliveryTime[t][d] = np.mean(y)
        totalMsgSent[t][d] = np.mean(z)
        
    list_M_avgDelTime.append(np.array(avgDeliveryTime))
    list_M_avgDelNode.append(np.array(avgDeliveryNodes))
    list_M_totalMsgs.append(np.array(totalMsgSent))
    list_names.append(topologies_compare_random_graph[topology])
    
#plot_multiple_surfaces(list_M_avgDelTime, k, list_names, "Avg Delivery Time", "n24vsn48vsn100_random_graph_AvgDeliveryTime.gif")
#plot_multiple_surfaces(list_M_avgDelNode, k, list_names, "Avg Delivery Nodes", "n24vsn48vsn100_andom_graph_AvgDeliveryNodes.gif")
#plot_multiple_surfaces(list_M_totalMsgs, k, list_names, "Total Msgs Sent", "n24vsn48vsn100_random_graph_TotalMsgSent.gif")


list_M_avgDelTime = []
list_M_avgDelNode = []
list_M_totalMsgs = []
list_names = []
k = 8
for topology in topologies_compare_random_graph_ndh:
    l = os.listdir(topology)
    l.sort()
    
    avgDeliveryNodes = np.full((k,k), np.nan)
    avgDeliveryTime = np.full((k,k), np.nan)
    totalMsgSent = np.full((k,k), np.nan)
    
    for file in l:
        n, k_read, t, d = extract_info(file)
        x = []
        y = []
        z = []
        with open(topology/file,"r") as f:
            data = json.load(f)
            for test in data["tests"]:
                x.append(data["tests"][test]["avgDeliveryNodes"])
                y.append(data["tests"][test]["avgDeliveryTime"])
                z.append(data["tests"][test]["totalMsgSent"])
        
        avgDeliveryNodes[t][d] = np.mean(x)
        avgDeliveryTime[t][d] = np.mean(y)
        totalMsgSent[t][d] = np.mean(z)
        
    list_M_avgDelTime.append(np.array(avgDeliveryTime))
    list_M_avgDelNode.append(np.array(avgDeliveryNodes))
    list_M_totalMsgs.append(np.array(totalMsgSent))
    list_names.append(topologies_compare_random_graph_ndh[topology])
    
#plot_multiple_surfaces(list_M_avgDelTime, k, list_names, "Avg Delivery Time", "normVSdelayVScoinVSconn_random_graph_AvgDeliveryTime_n48.gif")
#plot_multiple_surfaces(list_M_avgDelNode, k, list_names, "Avg Delivery Nodes", "normVSdelayVScoinVSconn_random_graph_AvgDeliveryNodes_n48.gif")
#plot_multiple_surfaces(list_M_totalMsgs, k, list_names, "Total Msgs Sent", "normVSdelayVScoinVSconn_random_graph_TotalMsgSent_n48.gif")

