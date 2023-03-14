# Cultural-Connectivity
The model used here is a simplified version of the model proposed in Kolodny et al. 2015 (https://doi.org/10.1073/pnas.1520492112). Both versions simulate the accumulation and loss of tools over many generations with the rates of tool invention and tool loss being dependent on population size. In the original model, There are three pathways through which tools can be invented: (1) inventions that are independent of the existing cultural repertoire (2) inventions of tools that are part of the same toolkit of the existing tools or are direct analogies from existing tools (3) invetions by cominations of existing tools. In the version of the model used here, for somplicity, we simulated only the first investion process. In this model, new tools are invented with a probability of P_inv per individual per time step. Each new tool is associated with a positive selection coefficient s, which is drawn from an exponential distribution with parameter beta. We use the approximation that the probability of fixation of an adaptive allele is s instead of explicitly simulating the establishment of the tool (i.e. its transmission within the population). Thus, we assume that a newly invented tool is established with probability s, and that it immediately reaches its equilibrium frequency in the population. Afterwards, we assume established tools can still be lost in the population with a probability P_loss, which is divided by the number of individuals in the population. Thus, an isolated population will reach its equilibrium repertoire size when P_inv X beta X N = P_{loss}/N, where N is the population size. From this equation, for a given repertoire size of an interconnected population, we can calculate its "effective cultural population size", that is, the population size at which an isolated population would be expected to have the same repertoire size. For simplicity, we did not consider in this model inter-dependence in invention, spread or retention of tools whose functions are related. These are worthy of future exploration in the contexts of the proposed phenomena.

The parameter values we chose for this proof-of-principle model (P_inv = 0.001, beta = 0.1$, P_loss = 0.1) were chosen such that they would yield reasonable repertoire sizes for moderate population sizes. However, qualitatively similar results can be found for a wide parameter range.

Migration between populations occurs with a probability P_mig per individual. Migration events occur from the focal population to the neighbor and vice-versa and do not affect their population sizes. Each migrating individual carries with it a fraction f of its native population's cultural repertoire. In the presented results, we set f to 1, since we found that changing f had virtually the same effect as changing P_mig (meaning 2 individuals carrying each 10% of their population's tools had a very similar effect to 1 individual carrying 20% of the population's tools). For each tool carried to another population, we assume the tool establishes in that population with  probability s, as above when tools are invented.

Repertoire sizes at equilibrium were calculated by averaging the repertoire sizes between time steps 100,000 (at which point repertoire size had already plateaued) and 200,000. Within the same time range, the average number of tools unique to the focal population was estimated by sampling the number of unique tools once every 100 time steps and averaging them.

Main code.py contains the model version used in the report, including all the relevant functions used
Create Model version with limited migrant toolkit size.py contains the model version in which the number of tools carried by a single migrant is limited
