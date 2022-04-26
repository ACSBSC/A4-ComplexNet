import numpy.random as rnd
import numpy as np
import math
import networkx as nx
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


def init_state(G):
    """Initialise all node in the graph to be susceptible."""
    for i in G.node.keys():
        G.node[i]['state'] = 'S'
    return G

def start_infection(G, pSick):
    """Inject a random proportion of nodes in the graph."""
    for i in G.node.keys():
        if(rnd.random() <= pSick):
            G.node[i]['state'] = 'I'
    return G

def SIS(G):
    S = 'S'                 #Healthy
    I = 'I'                 #Infected
    recovery = 0.5          #probability of getting cured
    infection = 0.5         #probability of getting infected
    list_fraq_infected = [] #average fraction of infected node per cycle
    time_step = 1000
    
    for i in range(time_step):
        for i in G.nodes.keys():
            if G.node[i]['state'] == I:
                rn = rnd.random()
                if rn <recovery:
                    G.node[i]['state']=S
            elif G.node[i]['state'] == S:
                for n in G.neighbors(i):
                    rn = rnd.random()
                    if rn < infection:
                        G.node[i]['state']=I
                         
    return G
    
    #avrg_fraq_infected = sum(list_fraq_infected)/len(list_fraq_infected) #average of averages fraction of infected node
    
n=10
p = 0.1
infected_per = 0.05                   #initial percentage of infected population
G = nx.erdos_renyi_graph(n, p)
G = init_state(G) 
G = start_infection(G,infected_per)   