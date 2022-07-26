import numpy as np
import random
import matplotlib.pyplot as plt

class tool:
    def __init__(self,s,pop):
        self.s = s  #Each tool has a selective value
        self.pop = pop  #and a population of origin

class pop:
    
    def __init__(self,name,size,toollist = []):
        self.name = name    #Each population has a name (which will be saved
                            #under "pop" for tools created in it)
        self.size = size    #a size (number of individuals)
        self.toollist = toollist    #and a list of all the existing tools in a given time step

    def __repr__(self):
        #the representation format of a population is:
        #"Population X
        #N = Y; Tools = Z"
        #(Where X is the name of the population, Y is the number of individuals
        #and Z is the number of tools
        
        return ("Population "+str(self.name)+"\n(N = "+str(self.size)+"; Tools = "+str(len(self.toollist))+")")
    
    def tick(self, p_lucky, p_loss, beta): #progress between time steps (not including migration)
        #p_lucky - the individual probability of inventing a new tool per time step
        #p_loss - the "individual" probability of losing a tool (divided by the population size
        #to receive the population level probability)
        #beta - the mean value of the exponential distribution from which new tools'
        #selective value will be drawn
        
        if self.size == 0: #Populations sized 0 cannot accumulate tools
            return None
        updated_toollist = []
        for t in self.toollist: #go tool by tool
            if random.random() > p_loss/self.size: #draw whether the tool survived
                updated_toollist += [t] #if it did, add it to the updated tool list
        
        discovered_tools = np.random.binomial(self.size,p_lucky)    #draw the number of 
                                                                    #discovered tools
        tools_s = np.random.exponential(beta,discovered_tools)   #give each discovered tool
                                                                #a selection value
        draws = np.random.random(discovered_tools)
        for i in range(discovered_tools): #draw which tools will be fixated
            if draws[i] < tools_s[i]:
                updated_toollist += [tool(tools_s[i],self.name)]
        self.toollist = updated_toollist

    def migrant(self,source_pop,trans_frac):    #migration event from a "source_pop" population
                                                #trans_frac is the probability of a given tool
                                                #of source pop to be represented in the migrant's
                                                #toolkit
        if self.size == 0 or source_pop.size == 0:  #migration cannot happen between populations
                                                    #of size 0
            return None
        trans_tools = [] #the list of transmitted tools
        for t in source_pop.toollist: #go tool by tool in the tool list of the source population
            if random.random() < trans_frac*t.s and t not in self.toollist:
            #check if the tool was transmitted sucessfully. In order for that to happen:
            #1. The tool needs to not already exist in the recepient population's tool list
            #2. The tool needs to be in the migrant's toolkit (p = trans_frac)
            #3. The tool needs to establish succesfully (which depends on it's selective value)
                trans_tools += [t]

        self.toollist += trans_tools
    
def simulation(size1 = 200,size2 = 200,p_mig = 0.000001,t_max = 100000, burnin = 50000,
              trans_frac = 0.5,  p_lucky = 0.001, p_loss = 0.2, beta = 0.1):
    #simulate the accumulation of tools in two interconnected populations
    #size1 - the size of the focal population
    #size2 - the size of the neighboring population
    #p_mig - the individual probability of migration
    #t_max - the number of time steps in the simulation
    #burnin - the time step from which the focal population's repetoire and number of
    #unique tools will be averaged
    
    from1 = np.random.binomial(size1,p_mig,t_max)   #a list of the numbers of migrants
                                                    #in each time step from the focal population
                                                    #to the neighboring population
    from2 = np.random.binomial(size2,p_mig,t_max)   #same, but from the neighboring population

    pop1 = pop(1, size1, []) #create the focal population (named 1, of size size1 and with no tools
    pop2 = pop(2, size2, []) #same for the neighboring population
    
    n_tools1 = [] #a list of the number of tools in each time step in the focal population
    n_tools1_unique = []    #a list of samples of the number of tools unique to the focal 
                            #population in different time steps (we don't calculate it for 
                            #every time step to save time)
    n_tools2 = [] #a list of the number of tools in each time step in the neighboring population

    for t in range(t_max): #progress in time
        if (t+1)%25000 == 0:    #print the current time step every 10000 time steps to monitor
                            #the simulation's progress
            print (t+1)
            
        pop1.tick(p_lucky, p_loss, beta) #progess the focal population in time
        pop2.tick(p_lucky, p_loss, beta) #progess the neighboring population in time

        for m in range(from1[t]):   #preform migration events from the focal population
                                    #(if there are any)
            pop2.migrant(pop1,trans_frac)

        for m in range(from2[t]): #same for the neighboring population
            pop1.migrant(pop2,trans_frac)

        n_tools1 += [len(pop1.toollist)] #add the current number of tools to the list
        n_tools2 += [len(pop2.toollist)]
        if t > burnin and t%100 == 0:   #after burnin time steps, once in every 100 time steps
                                        #calculate the number of tools unique to the focal populatio
            unique = len(pop1.toollist)
            for tool in pop1.toollist:
                if tool in pop2.toollist:
                    unique -= 1
            n_tools1_unique += [unique]

    plt.plot(n_tools1)  #plot the accumulation of tools in the focal population
    plt.plot(n_tools2)  #plot the accumulation of tools in the neighboring population
    plt.show()

    return [np.mean(n_tools1[burnin:]),np.mean(n_tools1_unique)]
    #return the mean repertoire size in the focal population and
    #the mean number of tools unique to it
