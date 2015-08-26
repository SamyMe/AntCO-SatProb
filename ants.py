# -*- coding: utf-8 -*-
import sys , os
from copy import deepcopy
from random import randint, random
import threading
# from time import time


#--------------------------- READ CNF FILE ----------------------------------
def readCnf(cnfFile):
	clauses=[]
	nbL=0
	with open(cnfFile) as f:
 		for clause in enumerate(f):
			c=clause[1].strip('\n').strip('\r').strip('\n').split(" ")
			c = filter(None,c)
			if 'p' in c :
				nbL=int(c[-2])
			elif not ( 'c' in c) and len(c)>1:
				clauses.append(map(int,(c[:-1])))

	return clauses,nbL

#------------------------------- CHECK ---------------------------------
def check_all(clause,etat):
	clauses = deepcopy(clause)
	# print etat
	for l in etat:
		i=0
		while i < len(clauses):
			if l in clauses[i]:
				clauses.remove(clauses[i]) #suppression des clauses contenant l
			else:
				i=i+1
	# print clauses
	return len(clauses)


#------------------------ BESTSOL ANT ---------------------------------

def bestSol(sol,clauses,nbC):
	best=0
	bestS=0
	val=0
	count=0

	for i in sol:
		val=(nbC-check_all(clauses[:],i))/float(nbC)
		if val>best:
			best=val
			bestS=i
		count=count+val

	print "Mean: "+str(count/len(sol))+"\tBest val: "+str(best)


	
	if best==1:
		return True
	return bestS
	

#------------------------------- REMOVED VAL ---------------------------
def removedVal(clauses,inst):
	i=0
	nbC=len(clauses)
	# print inst
	while i < len(clauses):
		if inst in clauses[i]:
			clauses.remove(clauses[i]) #suppression des clauses contenant l
		else:
			i=i+1

	return nbC-len(clauses)

#--------------------------- GO ANT ------------------------------------

def goAnt(lock, clauses, nbL, pheromones,nb,contributions,solutions):
	nbC=len(clauses)
	solution=[0]*nbL

	lock.acquire()
	clausesUsed=deepcopy(clauses)
	lock.release()

	#construct a solution
	for i in range(1,nbL):
		valP=removedVal(clausesUsed[:],i)
		valN=removedVal(clausesUsed[:],-i)

		sumAll=pheromones[i]*valP+pheromones[-i]*valN

		if random() > pheromones[i]*valP/sumAll:
			sign=-1
		else:
			sign=1

		solution[i]=sign*i
		removedVal(clausesUsed,sign*i)

		lock.acquire()
		contributions[sign*i]=contributions[sign*i]+1
		lock.release()

	lock.acquire()
	solutions[nb]=solution
	lock.release()

#---------------------------- ANT COLONY -------------------------------

def antColony(clauses,nbL,nbAnts,p,nbIter):
	lock = threading.Lock()
	nbC=len(clauses)

	ant=[0]*nbAnts

	contributions={}
	solutions=[[0]]*nbAnts	

	pheromones={}

	
	for i in range(nbL):
		pheromones[i]=1/float(nbL)
		pheromones[-i]=1/float(nbL)

	for i in range(nbIter):

		#Initialise contributions
		for i in range(nbL):
			contributions[i]=0
			contributions[-i]=0
	
		#Launch ants
		for t in range(nbAnts):
			ant[t] = threading.Thread(target=goAnt, args=(lock, clauses[:], nbL, pheromones,t,contributions,solutions))
		
		for t in range(nbAnts):	
			ant[t].start()

		for t in range(nbAnts):	
			ant[t].join()

		checking=bestSol(solutions,clauses[:],nbC)
		if checking==True:
			print "OPTIMAL SOLUTION FOUND !!"
			print checking
			print ((len(clauses)-check_all(clauses[:],checking))/float(len(clauses)))
			return True
				
		#Update pheromones	
		for j in checking:
			pheromones[j]=pheromones[j]+2
				
			
		for j in range(nbL):
			pheromones[j]=pheromones[j]*(1-p)+contributions[j]*(p/nbL)
			pheromones[-j]=pheromones[-j]*(1-p)+contributions[-j]*(p/nbL)

	return checking, ((len(clauses)-check_all(clauses[:],checking))/float(len(clauses)))



#antColony(clauses,nbL,20,p,nbC)



