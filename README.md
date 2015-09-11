This is an application of the [Ant Colony Optimisation algorithm](https://en.wikipedia.org/wiki/Ant_colony_optimization) that mimics the behavior of ants while searching for food.
We applied it to the [Boolean Satisfiability problem](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem) (more precisely [max-sat](https://en.wikipedia.org/wiki/Maximum_satisfiability_problem)).

The main steps behind ACO algorithmes are:

1. Generating an ant colony
2. Each ant construct a path toward the solution (in other words)
3. When they all have explored their paths, they return they store their solution in a list (solutions)
4. The pheromone table is changed by incrementing the pheromones in each node where the Ants walked and incrementing a second time the nodes of the best solution found.
5. All the pheromone values are then decremented (by 1-p. Evaporation) 

###Usage
The algorithm takes as input: 

**antColony** *(clauses,nbL,nbAnts,p,nbIter)*
- clauses:	List of clauses (list of lists). A clause being a list of literal instences.
- nbL:		Number of literals.
- nbAnts:	Number of ants in the population.
- nbIter: 	Number of iterations.
- p:		Evaporation rate (float between 0.0 and 1.0).

And returns a tuple (bestInstence, bestVal) of the best solution (literals instentiation) found, and the best satisfaction rate.

To use the algorithme:
```python
from ants import readCnf, antColony
clauses,nbL=readCnf(filePath)
antColony(clauses,nbL,nbL/2,0.2,500)
```

###Ant implementation
**goAnt** *(lock, clauses, nbL, pheromones,nb,contributions,solutions)*
- lock:		Semaphore for ressource access control
- clauses:	List of clauses (list of lists). A clause being a list of literal instences.
- nbL:		Number of literals.
- pheromones:	Dictionary with pheromone values for each variable instentiation
- nb:		Ant's number
- contributions:Dictionary containing the number of times each instentiation was chosen in ants paths construction
- solutions:	Solution constructed by the ant


### Helping functions:
**readCnf** *(cnfFile)*: 		reads a cnf file and returns *clauses* list of lists, and number of literals *nbL*.
- inputFile:	path to cnf file (Examples of cnf files can be downloaded from [satlib.org](http://www.satlib.org/))

**removedVal** *(clauses,inst)* : 	number of clauses removed from *clauses* by instentiating the literal *inst*
- clauses:	List of clauses (list of lists). A clause being a list of literal instences.
- inst:		A literal instentiation

**random_sol** *(nbL)* : 		Generates a random solution
- nbL:		number of literals.

**check_all** *(clause,state)*: 	returns the number of not satisfied clauses left by *state* instentiation.
- state:	An instentation of the literals (a solution)

***

###License:
This is published under GNU GPL Lisence.
For more informations about the terms: https://www.gnu.org/licenses/gpl.html

![Image Alt](https://www.gnu.org/graphics/gplv3-127x51.png)


