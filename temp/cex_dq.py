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




curr_property_val = property_val - 9

#increase the size of the counterexample graph until its 
#probability surpasses the probability bound specified by
#user 
while curr_property_val <= property_val:
	count = 0
	seed_count = 0
	prob = 0
	curr_csl_prop = csl_prop[:csl_prop.rfind('=')+1] + str(curr_property_val) + ']'
	curr_bound = 1
	print(curr_csl_prop)
	print('=========================')

	if curr_property_val == 11:
		curr_prob_bound = 0.5
	elif curr_property_val == 12:
		curr_prob_bound = 0.25
	elif curr_property_val == 13:
		curr_prob_bound = 0.1
	elif curr_property_val == 14:
		curr_prob_bound = 0.01
	elif curr_property_val == 15:
		curr_prob_bound = 0.002
	elif curr_property_val == 16:
		curr_prob_bound = 0.001
	elif curr_property_val == 17:
		curr_prob_bound = 1e-4
	elif curr_property_val == 18:
		curr_prob_bound = 1e-5
	elif curr_property_val == 19:
		curr_prob_bound = 1e-6
	elif curr_property_val == property_val:
		curr_prob_bound = prob_bound
	while (prob<curr_prob_bound): 
		
		print('bound: ' + str(curr_bound))
		solver = Solver()
		#add the initial state constraint
		init_const = []
		for n in graph.node_list:
			var_values = []
			if n.var_dict[property_var] == curr_property_val: 
				continue
			for s in n.var_dict: 
				x = Int (s + '.0')
				temp_const = (x == n.var_dict[s])
				var_values.append(temp_const)
			init_const.append(And(var_values))
		init_const = Or(init_const)
		solver.add(init_const)
		#add the constraints up to and including the starting bound
		for i in range(1, curr_bound):
			solver.add(get_encoding(model, i))
			#solver.add(loop_constraint(model, i))
		solver.add(get_encoding(model, curr_bound))
		solver.add(exclude_graph(graph, curr_bound))

		x = Int(property_var + '.' + str(curr_bound))
		property_constraint = (x==curr_property_val)
		#print(property_constraint)
		
		flag = False

		while(solver.check(property_constraint)==sat):
			flag = True
			count = count+1
			seed_count = seed_count + 1
			#print(seed_count)
			path = solver.model()
			#print(path)
			graph.add_path(path)
			solver.add(exclude_path(path))
			if seed_count>100:
				seed_count = 0
				count, prob, terminate = construct_path_2(graph, model, model_name, prism, curr_csl_prop, cp_bound, count, prob, prob_bound, property_var, curr_property_val, mc_step)
				if terminate: 
					break

			if (count%mc_step)==0: 
				prob = graph.model_check(model, model_name, prism, curr_csl_prop)
				print(prob)
				if prob>=prob_bound:
					break
		
		# if not flag: 
		# 	count, prob, terminate = construct_path(graph, model, model_name, prism, csl_prop, cp_bound, count, prob, prob_bound, property_var, property_val, mc_step)
		# 	if terminate: 
		# 		print('total # of paths so far: ' + str(count))
		# 		print('# of seed paths so far: ' + str(seed_count))
		# 		print('probability= ' + str(prob))
		# 		break
				
		# print('total # of paths so far: ' + str(count))
		# print('# of seed paths so far: ' + str(seed_count))
		# prob = graph.model_check(model, model_name, prism, csl_prop)
		# print('probability= ' + str(prob))
		# print('-' * 40)
		curr_bound = curr_bound+1
		#solver.add(get_encoding(model, curr_bound))
		prob = graph.model_check(model, model_name, prism, curr_csl_prop)

	curr_property_val = curr_property_val + 1

print('=' * 40)
print('=' * 40)
print('Result:')
print('total # of paths: ' + str(count))
print('# of seed paths: ' + str(seed_count))
prob = graph.model_check(model, model_name, prism, csl_prop)
print('probability of the counterexample subgraph= ' + str(prob))


