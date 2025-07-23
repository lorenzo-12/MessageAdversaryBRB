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
from matplotlib.ticker import MultipleLocator

def filter_ticks(values, min_diff=10):
    """Only keep values that are at least `min_diff` apart"""
    filtered = []
    last = -float('inf')
    for v in sorted(values):
        if v - last >= min_diff:
            filtered.append(v)
            last = v
    return filtered

path = pathlib.Path(__file__).parent 

topologies = [
    "test_topologies_coin_flip",
    "test_topologies_delay",
    "test_topologies",
    "test_topologies_byz_high_conn",
]

ret = {}
for topology in topologies:
    files = os.listdir(path/topology)
    files.sort()
    for file in files:
        edges = 0
        with open(path/topology/file, "r") as f:
            d = json.load(f)
            net = d["experiments"][0]["topology"]["list"]
            for node in net:
                edges += len(net[node])
        ret[file.replace(".json","")] = int(edges/2)
        #print(f'topology: {file.replace(".json","")} - edges: {int(edges/2)}')
    
tmp = {}    
for topology in ret:
    name = topology.replace("_n24_k4","").replace("_n48_k8","").replace("_n100_k6","")
    if name not in tmp:
        tmp[name] = [ret[topology]]
    else:
        tmp[name].append(ret[topology])

tmp_y = {}
for key in tmp:
    if ("coin" in key) or ("delay" in key) or ("high" in key) or ("center" in key):
        continue
    if ("_e500" in key) or ("_e600" in key) or ("_e700" in key) or ("_n99" in key):
        x = np.full((3), np.nan)
        x[2] = tmp[key][0]
        tmp_y[key] = x
        print(key, tmp_y[key])
    else:
        x = np.full((3), np.nan)
        for i,val in enumerate(tmp[key]):
            x[i] = val
        x.sort() 
        tmp_y[key] = x
        print(key, tmp_y[key])
    
fig, axs = plt.subplots(1, 1, figsize=(6,6),constrained_layout=True)
x = ["n24_k4", "n48_k8", "n100_k6"]

epsilon = 0.002
idx = 0
for key in tmp_y:
    y = tmp_y[key]
    shifted_y = [val+(idx+epsilon) for val in tmp_y[key]]
    axs.plot(x, y, marker='o', label=key)
    idx+=1
axs.set_title("edges")
axs.set_xlabel("topology size (n,k)")
axs.set_ylabel("number of edges")
axs.grid(True)
all_y_values = sorted(set(val for arr in tmp_y.values() for val in arr if not np.isnan(val)))
filtered_y_values = filter_ticks(all_y_values, min_diff=20)
axs.set_yticks(filtered_y_values)
axs.tick_params(axis='y', labelrotation=45)
axs.legend()
plt.legend(fontsize=14)
plt.savefig(f"edges_plot.jpg", dpi=100)
plt.show()
plt.close()