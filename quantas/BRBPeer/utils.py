import json 
import os 
import pathlib 
import random 
import ast
import re

path_base_topologies = pathlib.Path(__file__).parent / "base_topologies"
path_ma1 = pathlib.Path(__file__).parent / "topologies_<alg>" / "MA1_topologies"
path_ma2 = pathlib.Path(__file__).parent / "topologies_<alg>" / "MA2_topologies"
path_ma3 = pathlib.Path(__file__).parent / "topologies_<alg>" / "MA3_topologies"
path_results = pathlib.Path(__file__).parent.parent.parent / "results"


def getNetwork(network_path):
    with open(network_path, "r") as f:
        net_json = json.load(f)
    return net_json

def add_self_loop_edge(nodes_dict):
    for key in nodes_dict:
        n = int(key)
        nodes_dict[key].append(n)
    return nodes_dict

def getRandomNode(start, end):
    x = random.randint(start,end)
    return x

def getRandomCorrectNodes(quantity: int=0, start: int=0, end: int=0, sender:int=0, nodes_to_avoid: list=[]):
    byz_list = []
    while len(byz_list)<quantity:
        x = random.randint(start,end)
        if (x not in byz_list) and (x != sender) and (x not in nodes_to_avoid):
            byz_list.append(x)
    return byz_list

def removeRandomEdges(quantity: int=0, edges: dict={}):
    all_edges_list = []
    for node in edges:
        for neighbor in edges[node]:
            if (int(neighbor) == int(node)):
                continue
            if (int(neighbor),int(node)) not in all_edges_list:
                all_edges_list.append((int(node),int(neighbor)))
    
    i = 0
    while i<quantity:
        x = random.randint(0,len(all_edges_list)-1)
        a = int(all_edges_list[x][0])
        b = int(all_edges_list[x][1])
        all_edges_list.pop(x)
        i += 1
        
        #print(f"removing ({a,b}) - ({b,a})")
        edges[str(a)].remove(b)
        edges[str(b)].remove(a)
        
    return edges

def isolateNodes(edges: dict={}, nodes_list: list=[]):
    for node in nodes_list:
        node = str(node)
        edges[node] = []
    
    for node in edges:
        neigh = edges[node]
        for tmp in nodes_list:
            if tmp in neigh:
                neigh.remove(tmp)
    
    return edges


def extractNK(net_name):
    match = re.search(r"_n(\d+)_k(\d+)", net_name)
    if not match:
        raise ValueError(f"Could not extract k from network name: {net_name}")
    return int(match.group(1)),int(match.group(2))


def gen_t_d_combination(n: int = 0,k: int = 0):
    if n == 0:
        l = []
        for t in range(k):
            for d in range(k-t):
                l.append((t,d))
        return l
    
    l = []
    x = min(15,n/3)
    for t in range(x):
        for d in range(k):
            l.append((t,d))
    return l


def getOutputFile(net_name, ma_type, byz_num, ma_power, algorithm):
    name = net_name.split("_n")[0]
    category = "n"+net_name.split("_n")[1]
    exp = f"t{byz_num}_d{ma_power}.json"
    path = path_results / "MA1"
    if ma_type == "ma2":
        path = path_results / "MA2"
    if ma_type == "ma3":
        path = path_results / "MA3"
    output_file_name = path / name / category / algorithm / exp 
    output_file_name = str(output_file_name).split("BRB/")[1]
    os.makedirs(path / name / category / algorithm, exist_ok=True)
    return str(output_file_name) 

def changeAlg(net_json, alg):
    if (alg=="bracha"):
        net_json["experiments"][0]["logFile"] = net_json["experiments"][0]["logFile"].replace("opodis","bracha")
    else:
        net_json["experiments"][0]["logFile"] = net_json["experiments"][0]["logFile"].replace("bracha","opodis")
    topology = net_json["experiments"][0]["topology"]
    topology["algorithm"] = alg
    return net_json


def generateRandomNetMA1(net_name, byz_number, ma_power, algorithm: str = "bracha"):
    net_json = getNetwork(net_name)
    topology_name = net_name.split("/base_topologies/")[1].replace(".json","")
    
    net_json["experiments"][0]["algorithm"] = f"{topology_name}"
    net_json["experiments"][0]["logFile"] = getOutputFile(topology_name, "ma1", byz_number, ma_power, algorithm)
    net_json["experiments"][0]["tests"] = 100
    net_json["experiments"][0]["rounds"] = 200
    
    topology = net_json["experiments"][0]["topology"]
    
    topology["algorithm"] = algorithm
    topology["list"] = add_self_loop_edge(topology["list"])
    n = topology["totalPeers"]
    ma_section = topology["messageAdversary"]
    byz_section = topology["byzantine"]
    
    sender_id = getRandomNode(0,n-1)
    topology["sender_id"] = sender_id
    topology["msgToSend"] = 1
    
    byz_section["total"] = byz_number
    byz_nodes_list = getRandomCorrectNodes(quantity=byz_number, start=0, end=n-1, sender=sender_id, nodes_to_avoid=[])
    byz_section["list"] = byz_nodes_list
    byz_section["type"] = "userList"
    
    ma_section["behavior"] = "ma1"
    ma_section["power"] = ma_power
    
    return net_json["experiments"][0]


def generateRandomNetMA2(net_name, byz_number, ma_power, algorithm: str = "bracha"):
    net_json = getNetwork(net_name)
    topology_name = net_name.split("/base_topologies/")[1].replace(".json","")
    
    net_json["experiments"][0]["algorithm"] = f"{topology_name}"
    net_json["experiments"][0]["logFile"] = getOutputFile(topology_name, "ma2", byz_number, ma_power, algorithm)
    net_json["experiments"][0]["tests"] = 100
    net_json["experiments"][0]["rounds"] = 200
    
    topology = net_json["experiments"][0]["topology"]
    topology["algorithm"] = algorithm
    topology["list"] = add_self_loop_edge(topology["list"])
    n = topology["totalPeers"]
    ma_section = topology["messageAdversary"]
    byz_section = topology["byzantine"]
    
    sender_id = getRandomNode(0,n-1)
    topology["sender_id"] = sender_id
    topology["msgToSend"] = 1
    
    byz_section["total"] = byz_number
    byz_nodes_list = getRandomCorrectNodes(quantity=byz_number, start=0, end=n-1, sender=sender_id, nodes_to_avoid=[])
    byz_section["list"] = byz_nodes_list
    byz_section["type"] = "userList"
    
    ma_section["behavior"] = "ma2"
    ma_section["power"] = ma_power
    ma_isolated_nodes = getRandomCorrectNodes(quantity=ma_power, start=0, end=n-1, sender=sender_id, nodes_to_avoid=byz_nodes_list)
    ma_section["nodes_blocked"] = ma_isolated_nodes
    
    topology["list"] = isolateNodes(topology["list"],ma_isolated_nodes)
    
    return net_json["experiments"][0]


def generateRandomNetMA3(net_name, byz_number, ma_power, algorithm: str = "bracha"):
    net_json = getNetwork(net_name)
    topology_name = net_name.split("/base_topologies/")[1].replace(".json","")
    
    net_json["experiments"][0]["algorithm"] = f"{topology_name}"
    net_json["experiments"][0]["logFile"] = getOutputFile(topology_name, "ma3", byz_number, ma_power, algorithm)
    net_json["experiments"][0]["tests"] = 100
    net_json["experiments"][0]["rounds"] = 200
    
    topology = net_json["experiments"][0]["topology"]
    topology["algorithm"] = algorithm
    topology["list"] = add_self_loop_edge(topology["list"])
    n = topology["totalPeers"]
    ma_section = topology["messageAdversary"]
    byz_section = topology["byzantine"]
    
    sender_id = getRandomNode(0,n-1)
    topology["sender_id"] = sender_id
    topology["msgToSend"] = 1
    
    byz_section["total"] = byz_number
    byz_nodes_list = getRandomCorrectNodes(quantity=byz_number, start=0, end=n-1, sender=sender_id, nodes_to_avoid=[])
    byz_section["list"] = byz_nodes_list
    byz_section["type"] = "userList"
    
    ma_section["behavior"] = "ma3"
    ma_section["power"] = ma_power
    
    nodes_list = topology["list"]
    new_nodes_list = removeRandomEdges(quantity=ma_power, edges=nodes_list)
    topology["list"] = new_nodes_list
    
    return net_json["experiments"][0]


""" for file in path_base_topologies.rglob("*.json"):
    net_json = getNetwork(file)
    first_exp = net_json["experiments"][0]
    net_json["experiments"] = [first_exp]
    with open(file, "w+") as f:
        json.dump(net_json, f, indent=4) """ 
        


        
""" for file in os.listdir(path_ma1):
    with open(path_ma1/file,"r") as f:
        data = json.load(f)
        print(file,len(data["experiments"]))      """ 






