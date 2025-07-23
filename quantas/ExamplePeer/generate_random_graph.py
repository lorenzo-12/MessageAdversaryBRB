import networkx as nx
import matplotlib.pyplot as plt
import json
import pathlib
import random

d1 = {}
d2 = {}

k = 6
n = 100

""" 
k_connected = False 
while not k_connected:
    G = nx.erdos_renyi_graph(n, 0.2)
        
    k_connected = nx.is_k_edge_connected(G, k)
    print(k_connected)
    
    if k_connected:
        # Compute layout once to keep node positions consistent
        pos = nx.spring_layout(G, seed=42)
    
        for node in G.nodes():
            neighbors = list(nx.all_neighbors(G, node))
            print(f'"{node}": {neighbors},')
            d1[node] = neighbors

        # Draw original graph
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=800, font_size=10)
        plt.title("Erdős–Rényi Graph (original k-edge-connected)")
        plt.savefig(f"random_graph_n{n}_k{k}.png")
        plt.close()
    


for node in G.nodes():
    neighbors = list(nx.all_neighbors(G, node))
    for neig in neighbors:
        G.remove_edge(node, neig)
        k_connected = nx.is_k_edge_connected(G, k)
        if k_connected:
            print(f"removed edge ({node}-{neig}) and graph is still k-edge-connected")
        else:
            G.add_edge(node, neig) 

for node in G.nodes():
    neighbors = list(nx.all_neighbors(G, node))
    print(f'"{node}": {neighbors},')
    d2[node] = neighbors

# Draw pruned graph using the same layout
plt.figure(figsize=(10, 8))
nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=800, font_size=10)
plt.title("Pruned Graph (still k-edge-connected)")
plt.savefig(f"random_graph_pruned_n{n}_k{k}.png")
plt.close()


top_path = pathlib.Path(__file__).parent / "topologies"
test_top_path = pathlib.Path(__file__).parent / "test_topologies"

with open(top_path / f"random_graph_n{n}_k{k}.json", "r") as f:
    js = json.load(f)
    js["experiments"][0]["topology"]["list"] = d1
with open(top_path / f"random_graph_n{n}_k{k}.json", "w") as f:
    json.dump(js, f, indent=4)

with open(top_path / f"random_graph_pruned_n{n}_k{k}.json", "r") as f:
    js = json.load(f)
    js["experiments"][0]["topology"]["list"] = d2
with open(top_path / f"random_graph_pruned_n{n}_k{k}.json", "w") as f:
    json.dump(js, f, indent=4)
    
    
"""



# generate random graph but with n100 k6 500 edges
d = {}
edge_list = []
top_path = pathlib.Path(__file__).parent / "topologies"
test_top_path = pathlib.Path(__file__).parent / "test_topologies"

with open(test_top_path / f"random_graph_n{n}_k{k}.json", "r") as f:
    js = json.load(f)
    d = js["experiments"][0]["topology"]["list"]

G = nx.Graph()
for node in d:
    G.add_node(node)

for node in d:
    for neigh in d[node]:
        if ( (str(node),str(neigh)) not in edge_list) and ((str(neigh),str(node)) not in edge_list ):
            edge_list.append((str(node),str(neigh)))
        G.add_edge(str(node),str(neigh))
        
print(G)

while len(edge_list)>600:
    x = random.randint(0,len(edge_list)-1)
    node, neig = edge_list[x]
    G.remove_edge(node, neig)
    k_connected = nx.is_k_edge_connected(G, k)
    if k_connected:
        #print(f"removed edge ({node}-{neig}) and graph is still k-edge-connected")
        edge_list.remove((node,neig))
    else:
        G.add_edge(node, neig) 

print(G)
    
d2 = {}
for node in G.nodes():
    neighbors = list(nx.all_neighbors(G, node))
    neigh = [int(x) for x in neighbors]
    #print(f'"{node}": {neigh},')
    d2[node] = neigh


with open(test_top_path / f"random_graph_n{n}_k{k}.json", "r") as f:
    js = json.load(f)
    js["experiments"][0]["topology"]["list"] = d2
with open(top_path / f"random_graph_n{n}_k{k}_e{len(edge_list)}.json", "w") as f:
    json.dump(js, f, indent=4)
  
 
 
 
 
 
 