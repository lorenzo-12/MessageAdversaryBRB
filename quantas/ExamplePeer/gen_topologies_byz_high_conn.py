import os 
import pathlib
import json
import copy
import random

top_path = pathlib.Path(__file__).parent / "test_topologies"
test_topo_path = pathlib.Path(__file__).parent / "test_topologies_byz_high_conn"

def select_byz(network, byz_num):
    d = {}
    for elem in network:
        #print(f"node {elem}: {len(network[elem])} neighbors")
        if len(network[elem]) not in d:
            d[len(network[elem])] = [elem]
        else:
            d[len(network[elem])].append(elem)
    keys = list(d.keys())
    keys.sort(reverse=True)
    for k in keys:
        print(f"degree {k}: {d[k]} nodes")
    
    byz_nodes = []
    for k in keys:
        for node in d[k]:
            if len(byz_nodes) < byz_num:
                byz_nodes.append(int(node))
            else:
                print(f"{byz_num} -> selected byzantine nodes: {byz_nodes}")
                return byz_nodes
                

with open(top_path/f"random_graph_n24_k4.json","r") as f:
    dict = json.load(f)
    exp_list = dict["experiments"]
    for i in range(len(exp_list)):
        exp = dict["experiments"][i]
        exp["logFile"] = exp["logFile"].replace("random_graph_","random_graph_byz_high_conn_").replace("base","byz_high_conn/normal")
        exp["logFile"] = exp["logFile"].replace("random_graph/","")
        net = exp["topology"]["list"]
        t = exp["topology"]["byzantine"]["total"]
        byz_nodes = select_byz(exp["topology"]["list"], t)
        exp["topology"]["byzantine"]["list"] = byz_nodes
        exp["topology"]["byzantine"]["type"] = "userList"
        print("--------------------")
        
    with open(test_topo_path/f"random_graph_byz_high_conn_n24_k4.json","w+") as fw:
        json.dump(dict,fw,indent=4)

with open(top_path/f"random_graph_n48_k8.json","r") as f:
    dict = json.load(f)
    exp_list = dict["experiments"]
    for i in range(len(exp_list)):
        exp = dict["experiments"][i]
        exp["logFile"] = exp["logFile"].replace("random_graph_","random_graph_byz_high_conn_").replace("base","byz_high_conn/normal")
        exp["logFile"] = exp["logFile"].replace("random_graph/","")
        net = exp["topology"]["list"]
        t = exp["topology"]["byzantine"]["total"]
        byz_nodes = select_byz(exp["topology"]["list"], t)
        exp["topology"]["byzantine"]["list"] = byz_nodes
        exp["topology"]["byzantine"]["type"] = "userList"
    
    with open(test_topo_path/f"random_graph_byz_high_conn_n48_k8.json","w+") as fw:
        json.dump(dict,fw,indent=4)

with open(top_path/f"random_graph_n100_k6.json","r") as f:
    dict = json.load(f)
    exp_list = dict["experiments"]
    for i in range(len(exp_list)):
        exp = dict["experiments"][i]
        exp["logFile"] = exp["logFile"].replace("random_graph_","random_graph_byz_high_conn_").replace("base","byz_high_conn/normal")
        exp["logFile"] = exp["logFile"].replace("random_graph/","")
        net = exp["topology"]["list"]
        t = exp["topology"]["byzantine"]["total"]
        byz_nodes = select_byz(exp["topology"]["list"], t)
        exp["topology"]["byzantine"]["list"] = byz_nodes
        exp["topology"]["byzantine"]["type"] = "userList"
    
    with open(test_topo_path/f"random_graph_byz_high_conn_n100_k6.json","w+") as fw:
        json.dump(dict,fw,indent=4)
        
with open(top_path/f"random_graph_pruned_n24_k4.json","r") as f:
    dict = json.load(f)
    exp_list = dict["experiments"]
    for i in range(len(exp_list)):
        exp = dict["experiments"][i]
        exp["logFile"] = exp["logFile"].replace("random_graph_pruned_","random_graph_pruned_byz_high_conn_").replace("base","byz_high_conn/pruned")
        exp["logFile"] = exp["logFile"].replace("random_graph_pruned/","")
        net = exp["topology"]["list"]
        t = exp["topology"]["byzantine"]["total"]
        byz_nodes = select_byz(exp["topology"]["list"], t)
        exp["topology"]["byzantine"]["list"] = byz_nodes
        exp["topology"]["byzantine"]["type"] = "userList"
        
    with open(test_topo_path/f"random_graph_pruned_byz_high_conn_n24_k4.json","w+") as fw:
        json.dump(dict,fw,indent=4)
        
with open(top_path/f"random_graph_pruned_n48_k8.json","r") as f:
    dict = json.load(f)
    exp_list = dict["experiments"]
    for i in range(len(exp_list)):
        exp = dict["experiments"][i]
        exp["logFile"] = exp["logFile"].replace("random_graph_pruned_","random_graph_pruned_byz_high_conn_").replace("base","byz_high_conn/pruned")
        exp["logFile"] = exp["logFile"].replace("random_graph_pruned/","")
        net = exp["topology"]["list"]
        t = exp["topology"]["byzantine"]["total"]
        byz_nodes = select_byz(exp["topology"]["list"], t)
        exp["topology"]["byzantine"]["list"] = byz_nodes
        exp["topology"]["byzantine"]["type"] = "userList"
        
    with open(test_topo_path/f"random_graph_pruned_byz_high_conn_n48_k8.json","w+") as fw:
        json.dump(dict,fw,indent=4)
    
with open(top_path/f"random_graph_pruned_n100_k6.json","r") as f:
    dict = json.load(f)
    exp_list = dict["experiments"]
    for i in range(len(exp_list)):
        exp = dict["experiments"][i]
        exp["logFile"] = exp["logFile"].replace("random_graph_pruned_","random_graph_pruned_byz_high_conn_").replace("base","byz_high_conn/pruned")
        exp["logFile"] = exp["logFile"].replace("random_graph_pruned/","")
        net = exp["topology"]["list"]
        t = exp["topology"]["byzantine"]["total"]
        byz_nodes = select_byz(exp["topology"]["list"], t)
        exp["topology"]["byzantine"]["list"] = byz_nodes
        exp["topology"]["byzantine"]["type"] = "userList"
        
    with open(test_topo_path/f"random_graph_pruned_byz_high_conn_n100_k6.json","w+") as fw:
        json.dump(dict,fw,indent=4)
        

  

    