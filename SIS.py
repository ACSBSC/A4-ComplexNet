import numpy.random as rnd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


def init_state(G):
    for i in G.nodes.keys():
        G.nodes[i]['state'] = 'S'
        G.nodes[i]['time'] = 0
    return G

def start_infection(G, pSick):
    infected=0
    for i in G.nodes.keys():
        if(rnd.random() <= pSick):
            G.nodes[i]['state'] = 'I'
            infected+=1
    return G, infected

def SIS_method(G, N, recovery, infection, infected_per, time_step, transitory_step):
    
    G = init_state(G)                                       #Initialise all node in the graph to be susceptible
    G, init_infected_num = start_infection(G,infected_per)  #Inject a random proportion of infected nodes in the graph
    
    S = 'S'                                #Healthy
    I = 'I'                                #Infected
    
    list_infected = [init_infected_num]    #total num of infected nodes per step
    list_healthy = [N-init_infected_num]   #total num of healthy nodes per step
    
    
    for t in range(time_step):                      #Cycle of spreading infection
        infected_count = 0
        for i in G.nodes.keys():                    #Go through every node / population
            if G.nodes[i]['state'] == I:            #If node is infected, see if it recovers
                rn = rnd.random()
                if rn < recovery:
                    G.nodes[i]['state']=S
                    G.nodes[i]['time']+=1
            elif G.nodes[i]['state'] == S:          #If node is healthy, see if it gets infected
                for n in G.neighbors(i):            #survey its neighbours to see if any of them is infected
                    if G.nodes[n]['state'] == 'I':  #if a neighbouring node is infected, calculate if the healthy node gets infected
                        if G.nodes[i]['time'] == G.nodes[n]['time']:
                            rn = rnd.random()
                            if rn < infection:
                                G.nodes[i]['state']=I
                                G.nodes[i]['time']+=1
                                break
        
        if t >= transitory_step:                        #stationarty steps that will be the ones to use for rho <p>
            for i in G.nodes.keys():                    #count the number of final infected nodes
                if G.nodes[i]['state'] == I:
                    infected_count+=1
            
            list_infected.append(infected_count)        #number of infected nodes per cycle
            list_healthy.append(N-infected_count)       #number of healthy nodes per cycle
                         
    return list_healthy, list_infected
    
 
def SIS(G,n,repetition, recovery_rate, infected_rate, init_infected_per, time_step, transitory_step):
    
    average_rho = []                                #list of rhos over repetition
    
    for r in range(repetition):
        print("Repetition nr: "+str(r+1)+" loading...")
        healthy, infected = SIS_method(G,n, recovery_rate, infected_rate, init_infected_per, time_step,transitory_step)    
        
        rho=(sum(infected)/len(infected))/n         #average number of infected over k cycles
        average_rho.append(rho)

    
    p=sum(average_rho)/len(average_rho)             #average of average of average of rhos per repetition
    
    return p

   
#graph settings   
n = [500,550,600]
p = 0.1
G = nx.erdos_renyi_graph(n[0], p)               #Graph with 500 nodes
'''G2 = nx.erdos_renyi_graph(n[1], p)              #Graph with 1000 nodes
G3 = nx.erdos_renyi_graph(n[2], p)               #Graph with 500 nodes'''

nx.write_pajek(G, "./NewNet/graph_1_500_ER.net")         #Save fist graph as .net pajek file
'''nx.write_pajek(G2, "./NewNet/graph_2_550_ER.net")        #Save second graph as .net pajek file
nx.write_pajek(G3, "./NewNet/graph_3_600_ER.net") '''       #Save second graph as .net pajek file

list_graphs=[G]#,G2,G3]

#SIS model settings
repetition = 50                                 #num of repetitions of the model
recovery_rate = [0.2,0.4,0.6,0.8,1.0]           #different probabilities of getting cured
infected_rate = np.arange(0.0, 1.02, 0.02)      #different probabilities of getting infected 
init_infected_per = 0.2                         #Initial percentage of infected population
time_step = 100                                #number of cycles 
transitory_step = 90                           #transitory steps



#go trhough different values of recovery rate
for i in range(len(list_graphs)):
    for mu in recovery_rate:
        averages_rhos_beta=[]
        for beta in infected_rate:  
            print("------------------------------ BETA: "+str(beta)+" MU: "+str(mu)+" ------------------------------")
            p = SIS(list_graphs[i],n[i],repetition, mu, beta, init_infected_per, time_step, transitory_step)
            
            averages_rhos_beta.append(p)            #save the average of average of rhos

        plt.plot(infected_rate, averages_rhos_beta) #plot rho values and beta values
        plt.xlabel('Infection rate (beta)')
        plt.ylabel('rho')
        plt.title('Population: '+str(n[i])+' Recovery rate: '+str(mu))
        plt.savefig('./NewPlots/Graph_'+str(i+1)+'Population_'+str(n[i])+'_Recovery rate_'+str(mu)+'.jpg')

        plt.close()
    
    
