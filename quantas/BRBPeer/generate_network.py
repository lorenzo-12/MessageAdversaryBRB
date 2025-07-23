import json 
import os 
from utils import *


algorithm = "bracha"
            

def generate_net(algorithm):

    #----------------- GENERATE NETWORK MA1 -------------------------
    for file in path_base_topologies.rglob("*.json"):
        file = str(file)
        if ("n24" in file or "n48" in file):
            continue
        net_json = getNetwork(file)
        n,k = extractNK(file)
        td_list = gen_t_d_combination(0,k)
        
        net_json["experiments"] = []
        for t,d in td_list:
            x = generateRandomNetMA1(file,t,d,algorithm)
            net_json["experiments"].append(x)
        
        out = file.replace("base_topologies",f"topologies_{algorithm}/MA1_topologies")
        with open(out, "w+") as f:
            json.dump(net_json, f, indent=4)

    #----------------------------------------------------------------



    #----------------- GENERATE NETWORK MA2 -------------------------
    for file in path_base_topologies.rglob("*.json"):
        file = str(file)
        if ("n24" in file or "n48" in file):
            continue
        net_json = getNetwork(file)
        n,k = extractNK(file)
        td_list = gen_t_d_combination(0,k)
        
        net_json["experiments"] = []
        for t,d in td_list:
            x = generateRandomNetMA2(file,t,d,algorithm)
            net_json["experiments"].append(x)
        
        out = file.replace("base_topologies",f"topologies_{algorithm}/MA2_topologies")
        with open(out, "w+") as f:
            json.dump(net_json, f, indent=4)
            
    #----------------------------------------------------------------



    #----------------- GENERATE NETWORK MA3 -------------------------
    for file in path_base_topologies.rglob("*.json"):
        file = str(file)
        if ("n24" in file or "n48" in file):
            continue
        net_json = getNetwork(file)
        n,k = extractNK(file)
        td_list = gen_t_d_combination(0,k)
        
        net_json["experiments"] = []
        for t,d in td_list:
            x = generateRandomNetMA3(file,t,d,algorithm)
            net_json["experiments"].append(x)
        
        out = file.replace("base_topologies",f"topologies_{algorithm}/MA3_topologies")
        with open(out, "w+") as f:
            json.dump(net_json, f, indent=4)

    #----------------------------------------------------------------

#generate_net("opodis")
#generate_net("bracha")

