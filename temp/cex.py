############################################################
############################################################
#Notes: 
#	1-this module works only for models with a single initial state
#	2-only properties of type "a U<=t b" where b is of the form "var=value"
#	  is accepted currently	
############################################################
############################################################

from z3 import *
import models
from Graph import graph, node
from utils import *
import sys
import json
import numpy as np
import os

#read json elements
f = open(sys.argv[1])
json_data = json.load(f)
model_name = json_data['model']
starting_bound = int(json_data['starting_bound'])
csl_prop = json_data['csl_property']
prism = json_data['prism_binary']
prob_bound = float(json_data['probability_bound'])
property_var = json_data['property_variable']
property_val = int(json_data['property_value'])
mc_step = int(json_data['model_check_step'])
cp_bound = int(json_data['construct_path_bound'])

#counterexample will be saved in results folder
if not os.path.exists('./results'): 
	os.makedirs('./results')

#'model' will point to the specific model class within 
#models module
constructor = getattr(models, model_name)
model = constructor()
graph = graph()


#adding the initial state to the graph
initial_state_vector = model.initial_state()
var_dict = {}
for i, s in enumerate(model.species_vector()):
	var_dict[s] = initial_state_vector[i]
node_ = node(var_dict)
node_.make_initial()
graph.add_node(node_)


curr_bound = starting_bound
prob = 0
count = 0
seed_count = 0
#increase the size of the counterexample graph until its 
#probability surpasses the probability bound specified by
#user 

while (prob<prob_bound): 
	
	bound_count = 0
	print('bound: ' + str(curr_bound))
	solver = Solver()
	#add the initial state constraint
	solver.add(get_initial_state(model))
	#add the constraints up to and including the starting bound
	for i in range(1, curr_bound+1):
		solver.add(get_encoding_2(model, i))
	#solver.add(exclude_graph(graph, curr_bound))

	x = Int(property_var + '.' + str(curr_bound))
	property_constraint = (x==property_val) 
	
	flag = False

	while(solver.check(property_constraint)==sat):
		flag = True
		bound_count = bound_count + 1
		count = count+1
		seed_count = seed_count + 1
		print(seed_count)
		path = solver.model()
		#print(path)
		graph.add_path(path)
		solver.add(exclude_path(path))
		if seed_count>200:
			print('here')
			count, prob, terminate = construct_path_2(graph, model, model_name, prism, csl_prop, cp_bound, count, prob, prob_bound, property_var, property_val, mc_step)
			if terminate: 
				break

		if (count%mc_step)==0: 
			prob = graph.model_check(model, model_name, prism, csl_prop)
			if prob>=prob_bound:
				break
	
	if not flag: 
		count, prob, terminate = construct_path(graph, model, model_name, prism, csl_prop, cp_bound, count, prob, prob_bound, property_var, property_val, mc_step)
		if terminate: 
			print('total # of paths so far: ' + str(count))
			print('# of seed paths so far: ' + str(seed_count))
			print('probability= ' + str(prob))
			break
			
	print('total # of paths so far: ' + str(count))
	print('# of seed paths so far: ' + str(seed_count))
	prob = graph.model_check(model, model_name, prism, csl_prop)
	print('probability= ' + str(prob))
	print('-' * 40)
	curr_bound = curr_bound+1
	#solver.add(get_encoding(model, curr_bound))

print('=' * 40)
print('=' * 40)
print('Result:')
print('total # of paths: ' + str(count))
print('# of seed paths: ' + str(seed_count))
prob = graph.model_check(model, model_name, prism, csl_prop)
print('probability of the counterexample subgraph= ' + str(prob))

