import os 
import pathlib
import json
import copy
import random

top_path = pathlib.Path(__file__).parent / "topologies"
test_topo_path = pathlib.Path(__file__).parent / "test_topologies"

def block(node,x):
    return node//x

def next_block(node,x,y):
    b = block(node,x)
    if b==(y-1):
        return 0
    return b+1

def prev_block(node,x,y):
    b = block(node,x)
    if b==0:
        return y-1
    return b-1

def get_nodes(block,x):
    a = (block*x)
    ret = []
    for i in range(x):
        ret.append(a+i)
    return ret

def multipartite_wheel(node_group,groups): 
    n = node_group*groups
    d = {}
    for i in range(n):
        b = block(i,node_group)
        next_b = next_block(i,node_group,groups)
        prev_b = prev_block(i,node_group,groups)
        next_n = get_nodes(next_b,node_group)
        prev_n = get_nodes(prev_b,node_group)
        
        d[str(i)] = []
        for val in next_n:
            d[str(i)].append(val)
        for val in prev_n:
            d[str(i)].append(val)
        
        #print(f"i:{i} block:{b} next:{next_n} prev:{prev_n}")

    return d


def generalized_wheel(node_center,total_nodes):
    d = {}
    for i in range(total_nodes-node_center):
        next_n = (i+1)%(total_nodes-node_center)
        prev_n = (i-1)
        if (next_n == total_nodes-node_center):
            next_n = 0
        if (prev_n == -1):
            prev_n = (total_nodes-node_center-1)
        
        d[str(i)]=[prev_n,next_n]
        for j in range(total_nodes-node_center,total_nodes):
            d[str(i)].append(j)
    
    
    for i in range(total_nodes-node_center,total_nodes):
        d[str(i)] = []
        for j in range(0,total_nodes-node_center):
            d[str(i)].append(j)
    
    
    return d

"""     

# k-pasted-tree
dict = {}
with open(top_path/"k-pasted-tree.json","r") as f:
    dict = json.load(f)

exp = dict["experiments"][0]
counter = 1

k = 4
for ma_power in range(0,k):
    for byz_node in range(0,k):
        total_nodes = 24
            
        print(f"pasted-tree_n{total_nodes}_k{k}_t{byz_node}_d{ma_power}.json")
        tmp = copy.deepcopy(exp)
        tmp["logFile"] = f"results/base/k-pasted-tree/pasted-tree_n{total_nodes}_k{k}_t{byz_node}_d{ma_power}.json"
        
        tmp["topology"]["initialPeers"]=total_nodes
        tmp["topology"]["totalPeers"]=total_nodes
        
        tmp["topology"]["byzantine"]["total"]=byz_node
        
        tmp["topology"]["messageAdversary"]["power"]=ma_power
        
        tmp["tests"]=1000
    
        dict["experiments"].append(tmp)
        counter += 1

if "experiments" in dict and exp in dict["experiments"]:
    dict["experiments"].remove(exp)
print(counter)
with open(test_topo_path/f"k-pasted-tree_n{total_nodes}_k{k}.json","w") as f:
    json.dump(dict,f,indent=4)
    
    
    
# k-diamond
dict = {}
with open(top_path/"k-diamond.json","r") as f:
    dict = json.load(f)

exp = dict["experiments"][0]
counter = 1

k = 4
for ma_power in range(0,k):
    for byz_node in range(0,k):
        total_nodes = 24
            
        print(f"diamond_n{total_nodes}_k{k}_t{byz_node}_d{ma_power}.json")
        tmp = copy.deepcopy(exp)
        tmp["logFile"] = f"results/base/k-diamond/diamond_n{total_nodes}_k{k}_t{byz_node}_d{ma_power}.json"
        
        tmp["topology"]["initialPeers"]=total_nodes
        tmp["topology"]["totalPeers"]=total_nodes
        
        tmp["topology"]["byzantine"]["total"]=byz_node
        
        tmp["topology"]["messageAdversary"]["power"]=ma_power
        
        tmp["tests"]=1000
    
        dict["experiments"].append(tmp)
        counter += 1

if "experiments" in dict and exp in dict["experiments"]:
    dict["experiments"].remove(exp)
print(counter)
with open(test_topo_path/f"k-diamond_n{total_nodes}_k{k}.json","w") as f:
    json.dump(dict,f,indent=4)
    
"""  

""" 
# multipartite wheel 
connectivity = [4,8]
dict = {}
with open(top_path/"multipartite_wheel.json","r") as f:
    dict = json.load(f)

exp = dict["experiments"][0]

counter = 1
for k in connectivity:
    dict = {}
    with open(top_path/"multipartite_wheel.json","r") as f:
        dict = json.load(f)
    for ma_power in range(0,k):
        for byza_node in range(0,k):
            node_group = int(k/2)
            groups = 12
            total_nodes = int(groups * (k/2))
            
            print(f"multipartite_wheel_n{total_nodes}_k{k}_t{byza_node}_d{ma_power}.json")
            tmp = copy.deepcopy(exp)
            tmp["logFile"] = f"results/base/multipartite_wheel/n{total_nodes}_k{k}/multipartite_wheel_n{total_nodes}_k{k}_t{byza_node}_d{ma_power}.json"
            
            tmp["topology"]["list"] = multipartite_wheel(node_group,groups)
            tmp["topology"]["initialPeers"]=total_nodes
            tmp["topology"]["totalPeers"]=total_nodes
            
            tmp["topology"]["byzantine"]["total"]=byza_node
            
            tmp["topology"]["messageAdversary"]["power"]=ma_power
            
            tmp["tests"]=1000
            
            dict["experiments"].append(tmp)
            counter += 1

    if "experiments" in dict and exp in dict["experiments"]:
        dict["experiments"].remove(exp)
    print(counter)
    file_name = f"multipartite_wheel_n{total_nodes}_k{k}.json"
    with open(test_topo_path/file_name,"w") as f:
        json.dump(dict,f,indent=4)
"""
 

"""
# generalized wheel
connectivity = [6]
dict = {}
with open(top_path/"generalized_wheel.json","r") as f:
    dict = json.load(f)

exp = dict["experiments"][0]
counter = 1

for k in connectivity:
    dict = {}
    with open(top_path/"generalized_wheel.json","r") as f:
        dict = json.load(f)
    for ma_power in range(0,k):
        for byz_node in range(0,k):
            total_nodes = 100
            
            
            print(f"generalized_wheel_n{total_nodes}_k{k}_t{byz_node}_d{ma_power}.json")
            tmp = copy.deepcopy(exp)
            tmp["logFile"] = f"results/base/generalized_wheel/n{total_nodes}_k{k}/generalized_wheel_n{total_nodes}_k{k}_t{byz_node}_d{ma_power}.json"
            
            tmp["topology"]["list"] = generalized_wheel(k-2,total_nodes)
            tmp["topology"]["initialPeers"]=total_nodes
            tmp["topology"]["totalPeers"]=total_nodes
            
            tmp["topology"]["byzantine"]["total"]=byz_node
            
            tmp["topology"]["messageAdversary"]["power"]=ma_power
            
            tmp["tests"]=1000
        
            dict["experiments"].append(tmp)
            counter += 1

    if "experiments" in dict and exp in dict["experiments"]:
        dict["experiments"].remove(exp)
    print(counter)
    file_name = f"generalized_wheel_n{total_nodes}_k{k}.json"
    with open(test_topo_path/file_name,"w") as f:
        json.dump(dict,f,indent=4)
"""    


"""
def getRandomNumberExcept(min,max,exc):
    while True:
        x = random.randint(min,max)
        if x not in exc:
            return x
        
def getXRandomNumber(min,max,x):
    ret = []
    count = 0
    while count<x:
        n = random.randint(min,max)
        if n not in ret:
            ret.append(n)
            count += 1
    return ret
        
        

# generalized wheel byzantine center
connectivity = [6]
dict = {}
with open(top_path/"generalized_wheel.json","r") as f:
    dict = json.load(f)

exp = dict["experiments"][0]
counter = 1

for k in connectivity:
    dict = {}
    with open(top_path/"generalized_wheel.json","r") as f:
        dict = json.load(f)
    for ma_power in range(0,k):
        for byz_node in range(0,k):
            total_nodes = 100
            
                    
            print(f"generalized_wheel_byz_center_n{total_nodes}_k{k}_t{byz_node}_d{ma_power}.json")
            tmp = copy.deepcopy(exp)
            tmp["logFile"] = f"results/base/generalized_wheel_byz_center/n{total_nodes}_k{k}/generalized_wheel_byz_center_n{total_nodes}_k{k}_t{byz_node}_d{ma_power}.json"
            
            tmp["topology"]["list"] = generalized_wheel(int(k-2),total_nodes)
            tmp["topology"]["initialPeers"]=total_nodes
            tmp["topology"]["totalPeers"]=total_nodes
            
            tmp["topology"]["messageAdversary"]["power"]=ma_power
            
            tmp["tests"]=1000
            
            tmp["topology"]["byzantine"]["total"]=byz_node
            byz_vec = []
            if byz_node==0:
                tmp["topology"]["byzantine"]["list"]=[]
                tmp["topology"]["byzantine"]["type"]="random"
            elif byz_node>0:
                byz_vec = getXRandomNumber(total_nodes-k-2,total_nodes-1,byz_node)
                tmp["topology"]["byzantine"]["list"] = byz_vec
                tmp["topology"]["byzantine"]["type"]="userList"
            
            
            dict["experiments"].append(tmp)  
            counter += 1

    if "experiments" in dict and exp in dict["experiments"]:
        dict["experiments"].remove(exp)
    print(counter)
    file_name = f"generalized_wheel_byz_center_n{total_nodes}_k{k}.json"
    with open(test_topo_path/file_name,"w") as f:
        json.dump(dict,f,indent=4)
"""


""" 
for file in os.listdir(top_path):
    if "random_graph" not in file:
        continue 
    with open(top_path/file,"r") as f:
        dict = json.load(f)

    exp = dict["experiments"][0]
    
    counter = 1
    x = file.replace("random_graph","").replace("_pruned","").replace(".json","").split("_")
    for y in x:
        if "n" in y:
            n = int(y.replace("n",""))
        if "k" in y:
            k = int(y.replace("k",""))
    print(file,n,k)
    
    with open(top_path/file,"r") as f:
        dict = json.load(f)
    for ma_power in range(0,k):
        for byza_node in range(0,k):
            
            tmp = copy.deepcopy(exp)
            if "pruned" in file:
                print(f"random_graph_pruned_n{n}_k{k}_t{byza_node}_d{ma_power}.json")
                tmp["logFile"] = f"results/base/random_graph_pruned/n{n}_k{k}/random_graph_pruned_n{n}_k{k}_t{byza_node}_d{ma_power}.json"
            else:
                print(f"random_graph_n{n}_k{k}_t{byza_node}_d{ma_power}.json")
                tmp["logFile"] = f"results/base/random_graph/n{n}_k{k}/random_graph_n{n}_k{k}_t{byza_node}_d{ma_power}.json"


            tmp["topology"]["initialPeers"]=n
            tmp["topology"]["totalPeers"]=n
            
            tmp["topology"]["byzantine"]["total"]=byza_node
            
            tmp["topology"]["messageAdversary"]["power"]=ma_power
            
            tmp["tests"]=1000
            
            dict["experiments"].append(tmp)
            counter += 1

    if "experiments" in dict and exp in dict["experiments"]:
        dict["experiments"].remove(exp)
    print(counter)
    file_name = file
    with open(test_topo_path/file_name,"w") as f:
        json.dump(dict,f,indent=4) 
    
"""


n = 100
k = 6
e = 500
with open(top_path / f"random_graph_n{n}_k{k}_e{e}.json", "r") as f:
    dict = json.load(f)
    exp = dict["experiments"][0]
    print(len(dict["experiments"]))
    while len(dict["experiments"])>0:
        dict["experiments"].remove(dict["experiments"][0])
    print(len(dict["experiments"]))
    counter = 1
    for ma_power in range(0,k):
        for byza_node in range(0,k):
            tmp = copy.deepcopy(exp)
            tmp["logFile"] = f"results/base/random_graph_half_edges/n{n}_k{k}_e{e}/random_graph_n{n}_k{k}_e{e}_t{byza_node}_d{ma_power}.json"
            tmp["topology"]["initialPeers"]=n
            tmp["topology"]["totalPeers"]=n
            tmp["topology"]["byzantine"]["total"]=byza_node
            tmp["topology"]["messageAdversary"]["power"]=ma_power
            tmp["tests"]=1000
            dict["experiments"].append(tmp)
            counter += 1
    
    if "experiments" in dict and exp in dict["experiments"]:
        dict["experiments"].remove(exp)     
    print(counter)
        
with open(test_topo_path / f"random_graph_n{n}_k{k}_e{e}.json", "w") as f:
    json.dump(dict, f, indent=4)



