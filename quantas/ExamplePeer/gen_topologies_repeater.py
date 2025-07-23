import os 
import pathlib
import json
import copy
import random

top_path = pathlib.Path(__file__).parent / "test_topologies"
test_topo_path = pathlib.Path(__file__).parent / "test_topologies_repeater"
        

with open(top_path/f"random_graph_k4.json","r") as f:
    dict = json.load(f)
    exp_list = dict["experiments"]
    for i in range(len(exp_list)):
        exp = dict["experiments"][i]
        exp["correctBehaviorType"] = "repeater"
        exp["logFile"] = exp["logFile"].replace("random_graph_","random_graph_repeater_").replace("base","repeater")
        exp["logFile"] = exp["logFile"].replace("random_graph/k4/","")
    
    with open(test_topo_path/f"random_graph_repeater_k4.json","w+") as fw:
        json.dump(dict,fw,indent=4)
        
with open(top_path/f"random_graph_pruned_k4.json","r") as f:
    dict = json.load(f)
    exp_list = dict["experiments"]
    for i in range(len(exp_list)):
        exp = dict["experiments"][i]
        exp["correctBehaviorType"] = "repeater"
        exp["logFile"] = exp["logFile"].replace("random_graph_pruned_","random_graph_pruned_repeater_").replace("base","repeater")
        exp["logFile"] = exp["logFile"].replace("random_graph_pruned/k4/","")
        
    with open(test_topo_path/f"random_graph_pruned_repeater_k4.json","w+") as fw:
        json.dump(dict,fw,indent=4)
  

    