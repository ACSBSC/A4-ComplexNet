import numpy.random as rnd
import numpy as np
import math
import networkx as nx
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


def init_state(G):
    for i in G.nodes.keys():
        G.nodes[i]['state'] = 'S'
    return G

def start_infection(G, pSick):
    infected=0
    for i in G.nodes.keys():
        if(rnd.random() <= pSick):
            G.nodes[i]['state'] = 'I'
            infected+=1
    return G, infected

def SIS(G, N, recovery, infection):
    infected_per = 0.2                                     #Initial percentage of infected population
    G = init_state(G)                                       #Initialise all node in the graph to be susceptible
    G, init_infected_num = start_infection(G,infected_per)  #Inject a random proportion of infected nodes in the graph
    
    S = 'S'                                #Healthy
    I = 'I'                                #Infected
    
    list_infected = [init_infected_num]    #total num of infected nodes per step
    list_healthy = [N-init_infected_num]   #total num of healthy nodes per step
    time_step = 10
    
    for i in range(time_step):                      #Cycle of spreading infection
        infected_count = 0
        for i in G.nodes.keys():                    #Go through every node / population
            if G.nodes[i]['state'] == I:            #If node is infected, see if it recovers
                rn = rnd.random()
                if rn <recovery:
                    G.nodes[i]['state']=S
            elif G.nodes[i]['state'] == S:          #If node is healthy, see if it gets infected
                for n in G.neighbors(i):            #survey its neighbours to see if any of them is infected
                    if G.nodes[n]['state'] == 'I':  #if a neighbouring node is infected, calculate if the healthy node gets infected
                        rn = rnd.random()
                        if rn < infection:
                            G.nodes[i]['state']=I
        
        for i in G.nodes.keys():                    #count the number of final infected nodes
            if G.nodes[i]['state'] == I:
                infected_count+=1
        
        list_infected.append(infected_count)
        list_healthy.append(N-infected_count)
                         
    return list_healthy, list_infected
    
    
    
n=100
p = 0.1

G = nx.erdos_renyi_graph(n, p)

recovery_rate = 0.2                         #probability of getting cured
infected_rate = 0.8                         #probability of getting infected 
healthy, infected = SIS(G,n, recovery_rate, infected_rate)

print('healthy')
print(healthy)
print('infected')
print(infected)