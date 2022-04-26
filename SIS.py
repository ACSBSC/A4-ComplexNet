import random as rnd

def SIS(G):
    S = "S"                 #Healthy
    I = "I"                 #Infected
    recovery = 0.5          #probability of getting cured
    infection = 0.5         #probability of getting infected
    list_fraq_infected = [] #average fraction of infected node per cycle
    time_step = 1000
    
    for i in range(time_step):
        for node in G.nodes:
            if node =="I":
                rn = rnd.random()
                if rn <recovery:
                    G.node=S
            else:
              print()  
    
    
    #avrg_fraq_infected = sum(list_fraq_infected)/len(list_fraq_infected) #average of averages fraction of infected node
    
    
    