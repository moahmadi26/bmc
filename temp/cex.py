############################################################
############################################################
#Notes: 
#	1-this module works only for models with a single initial state
#	2-only properties of type "a U<=t b" where b is of the form "var=value"
#	  is accepted currently	
############################################################
############################################################

from z3 import Solver, And, Int, Or, sat, simplify
import sys
import subprocess
import os
import json
import models
from Graph import graph, node
import numpy as np

#get smt encoding for the initial state constraint
def get_inital_state(model):
	species_vector = model.species_vector()
	initial_state = model.initial_state()
	constraints = []
	for i, s in enumerate(species_vector): 
		var_name = s + '.' + '0'
		x = Int(var_name)
		init_value = initial_state[i]
		constraints.append(x == init_value)
	return And(constraints)

#get smt encoding for a bound
def get_encoding(model, bound):
	species_vector = model.species_vector()
	constraints = []
	for j, r in enumerate(model.reactions_vector()): 
		r_constraints = []
		for i, s in enumerate(species_vector): 
			var_name_prev = s + '.' + str(bound-1)
			var_name_curr = s + '.' + str(bound)
			x = Int(var_name_prev)
			y = Int(var_name_curr)
			r_constraints.append(y == (x + model.reactions_vector()[r][2][i]))
			r_constraints.append(y >= 0)
			reaction_var_name = 'selected_reaction.' + str(bound-1) 
			selected_reaction = Int(reaction_var_name)
		r_constraints.append(selected_reaction == (j+1))
		constraints.append(And(r_constraints))
	return simplify(Or(constraints))
############################################################
############################################################
############################################################
############################################################

#read the model name, starting bound and property
#from json file specified as first argument
f = open(sys.argv[1])
json_data = json.load(f)
model = json_data['model']
starting_bound = int(json_data['starting_bound'])
csl_prop = json_data['csl_property']
prism = json_data['prism_binary']
prob_bound = float(json_data['property_bound'])
property_var = json_data['property_variable']
property_val = int(json_data['property_value'])


cwd = os.getcwd()

#'model' will point to the specific model class within 
#models module
constructor = getattr(models, model)
model = constructor()
solver = Solver()
graph = graph()

#add the initial state constraint
solver.add(get_inital_state(model))
#adding the initial state to the graph
initial_state_vector = model.initial_state()
var_dict = {}
for i, s in enumerate(model.species_vector()):
	var_dict[s] = initial_state_vector[i]
node_ = node(var_dict)
node_.make_initial()
graph.add_node(node_)



#add the constraints up to and including the starting bound
for i in range(1, starting_bound+1):
	solver.add(get_encoding(model, i))

curr_bound = starting_bound
#increase the size of the counterexample graph until its 
#probability surpasses the probability bound specified by
#user 
prob = 0
while (prob<prob_bound): 
	x = Int(property_var + '.' + str(curr_bound))
	property_constraint = (x==property_val)  
	while(solver.check(property_constraint)):
		path = solver.model()
		graph.add_path(path)
		graph.to_file('a', model)
		break
	break




a = subprocess.run([prism], stdout=subprocess.PIPE)

#print('======')
#for i in range(0):
#	print(i)

a = np.array([[[1, 2], [3, 4]], [[7, 8], [9, 10]]])
#print(a.reshape(-1, a.shape[-1]).tolist())
#print(a.stdout.decode('utf-8'))