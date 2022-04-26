import networkx as nx
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


n=10
p = 0.1

G = nx.erdos_renyi_graph(n, p)

print(G.nodes)

for i in G.nodes.keys():
    G.nodes[i]['state'] = 'S'
    
print(G.nodes(data=True))