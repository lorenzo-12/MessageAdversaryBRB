import os 
import pathlib
import json
import copy
import random

top_path = pathlib.Path(__file__).parent / "test_topologies"
test_topo_path = pathlib.Path(__file__).parent / "test_topologies_delay"
        

with open(top_path/f"random_graph_n24_k4.json","r") as f:
    dict = json.load(f)
    exp_list = dict["experiments"]
    for i in range(len(exp_list)):
        exp = dict["experiments"][i]
        exp["distribution"]["maxDelay"]=3
        exp["logFile"] = exp["logFile"].replace("random_graph_n24_k4","random_graph_delay_n24_k4").replace("base","delay/normal")
        exp["logFile"] = exp["logFile"].replace("random_graph/","")
        
    with open(test_topo_path/f"random_graph_delay_n24_k4.json","w+") as fw:
        json.dump(dict,fw,indent=4)

with open(top_path/f"random_graph_pruned_n24_k4.json","r") as f:
    dict = json.load(f)
    exp_list = dict["experiments"]
    for i in range(len(exp_list)):
        exp = dict["experiments"][i]
        exp["distribution"]["maxDelay"]=3
        exp["logFile"] = exp["logFile"].replace("random_graph_pruned_n24_k4","random_graph_pruned_delay_n24_k4").replace("base","delay/pruned")
        exp["logFile"] = exp["logFile"].replace("random_graph_pruned/","")
        
    with open(test_topo_path/f"random_graph_pruned_delay_n24_k4.json","w+") as fw:
        json.dump(dict,fw,indent=4)
        
with open(top_path/f"random_graph_n48_k8.json","r") as f:
    dict = json.load(f)
    exp_list = dict["experiments"]
    for i in range(len(exp_list)):
        exp = dict["experiments"][i]
        exp["distribution"]["maxDelay"]=3
        exp["logFile"] = exp["logFile"].replace("random_graph_n48_k8","random_graph_delay_n48_k8").replace("base","delay/normal")
        exp["logFile"] = exp["logFile"].replace("random_graph/","")
        
    with open(test_topo_path/f"random_graph_delay_n48_k8.json","w+") as fw:
        json.dump(dict,fw,indent=4)

with open(top_path/f"random_graph_pruned_n48_k8.json","r") as f:
    dict = json.load(f)
    exp_list = dict["experiments"]
    for i in range(len(exp_list)):
        exp = dict["experiments"][i]
        exp["distribution"]["maxDelay"]=3
        exp["logFile"] = exp["logFile"].replace("random_graph_pruned_n48_k8","random_graph_pruned_delay_n48_k8").replace("base","delay/pruned")
        exp["logFile"] = exp["logFile"].replace("random_graph_pruned/","")
        
    with open(test_topo_path/f"random_graph_pruned_delay_n48_k8.json","w+") as fw:
        json.dump(dict,fw,indent=4)
  
