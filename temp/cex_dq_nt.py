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

############################################################
def expand_graph(graph, level, step, base, property_var, max_bound): 
	#base case: find a path from initial state to a state with
	#property_var == base + step which already is not part of graph
	#(search until max_bound and if nothing was found terminate) 
	#print(level)
	if level == base + step: 
		

		curr_target_list = []
		for n in graph.node_list: 
			for s in n.var_dict:
				if s == property_var:
					if n.var_dict[s] == (base + step):
						curr_target_list.append(n)
		
		
		bound = 1
		while bound<=max_bound:
			solver = Solver()
			solver.add(get_initial_state(model))

			t_constraints = []
			for n in curr_target_list: 
				var_values = []
				for s in n.var_dict: 
					x = Int (s + '.' + str(bound))
					temp_const = (x == n.var_dict[s])
					var_values.append(temp_const)
				t_constraints.append(And(var_values))
			solver.add(Not(Or(t_constraints))) 

			for j in range(1, bound+1):
				solver.add(get_encoding(model, j))

			x = Int(property_var + '.' + str(bound))
			property_constraint = (x==(base+step))
			if (solver.check(property_constraint) == sat): 
				path = solver.model()
				graph.add_path(path)
				break
			bound = bound+1

	else:
		expand_graph(graph, level-step, step, base, property_var, max_bound)
		#print(level)
		curr_init_list = []
		for n in graph.node_list: 
			for s in n.var_dict:
				if s == property_var:
					if n.var_dict[s] == (level-step):
						curr_init_list.append(n)

		

		curr_target_list = []
		for n in graph.node_list: 
			for s in n.var_dict:
				if s == property_var:
					if n.var_dict[s] == level:
						curr_init_list.append(n)

		
		for k, n in enumerate(curr_init_list):
			#print(k)
			bound = 1
			while bound<=max_bound:
				solver = Solver()
				
				var_values = []
				for s in n.var_dict: 
					x = Int (s + '.0')
					temp_const = (x == n.var_dict[s])
					var_values.append(temp_const)
				solver.add(And(var_values))

				t_constraints = []
				for n in curr_target_list: 
					var_values = []
					for s in n.var_dict: 
						x = Int (s + '.' + str(bound))
						temp_const = (x == n.var_dict[s])
						var_values.append(temp_const)
					t_constraints.append(And(var_values))
				solver.add(Not(Or(t_constraints))) 
				for j in range(1, bound+1):
					solver.add(get_encoding(model, j))
				x = Int(property_var + '.' + str(bound))
				property_constraint = (x==(level))
				count_temp = 0
				if (solver.check(property_constraint) == sat): 
					count_temp = count_temp + 1
					path = solver.model()
					graph.add_path(path)
					break
				bound = bound+1


def add_paths(graph, level, step, base, property_var, max_bound): 
	#base case: find a path from initial state to a state with
	#property_var == base + step which already is not part of graph
	#(search until max_bound and if nothing was found terminate) 
	#print(level)
	if level == base + step: 
		

		curr_target_list = []
		for n in graph.node_list: 
			for s in n.var_dict:
				if s == property_var:
					if n.var_dict[s] == (base + step):
						curr_target_list.append(n)
		
		
		bound = 1
		while bound<=max_bound:
			solver = Solver()
			solver.add(get_initial_state(model))

			t_constraints = []
			for n in curr_target_list: 
				var_values = []
				for s in n.var_dict: 
					x = Int (s + '.' + str(bound))
					temp_const = (x == n.var_dict[s])
					var_values.append(temp_const)
				t_constraints.append(And(var_values))
			solver.add(Not(Or(t_constraints))) 

			for j in range(1, bound+1):
				solver.add(get_encoding(model, j))

			x = Int(property_var + '.' + str(bound))
			property_constraint = (x==(base+step))
			if (solver.check(property_constraint) == sat): 
				path = solver.model()
				graph.add_path(path)
				break
			bound = bound+1

	else:
		expand_graph(graph, level-step, step, base, property_var, max_bound)
		#print(level)
		curr_init_list = []
		for n in graph.node_list: 
			for s in n.var_dict:
				if s == property_var:
					if n.var_dict[s] == (level-step):
						curr_init_list.append(n)

		

		curr_target_list = []
		for n in graph.node_list: 
			for s in n.var_dict:
				if s == property_var:
					if n.var_dict[s] == level:
						curr_init_list.append(n)

		
		for k, n in enumerate(curr_init_list):
			#print(k)
			bound = 1
			while bound<=max_bound:
				solver = Solver()
				
				var_values = []
				for s in n.var_dict: 
					x = Int (s + '.0')
					temp_const = (x == n.var_dict[s])
					var_values.append(temp_const)
				solver.add(And(var_values))

				t_constraints = []
				for n in curr_target_list: 
					var_values = []
					for s in n.var_dict: 
						x = Int (s + '.' + str(bound))
						temp_const = (x == n.var_dict[s])
						var_values.append(temp_const)
					t_constraints.append(And(var_values))
				solver.add(Not(Or(t_constraints))) 
				for j in range(1, bound+1):
					solver.add(get_encoding(model, j))
				x = Int(property_var + '.' + str(bound))
				property_constraint = (x==(level))
				count_temp = 0
				if (solver.check(property_constraint) == sat): 
					count_temp = count_temp + 1
					path = solver.model()
					graph.add_path(path)
					break
				bound = bound+1


def thicken_graph(graph, level, step, base, property_var, max_bound):
	curr = base

	while curr!=level:
		#print(curr)
		init_states = []
		if curr!=level-step:
			for n in graph.node_list:
				if n.var_dict[property_var] == curr or n.var_dict[property_var] == curr + step:
					init_states.append(n)
		else:
			for n in graph.node_list:
				if n.var_dict[property_var] == curr:
					init_states.append(n)

		target_states = []
		for n in graph.node_list:
			if n.var_dict[property_var] == curr or n.var_dict[property_var] == curr + step: 
				target_states.append(n)

		bound = 1
		while bound<=max_bound:
			solver = Solver()
			
			
			init_consts = []
			for n in init_states:
				var_values = []
				for s in n.var_dict: 
					x = Int (s + '.0')
					temp_const = (x == n.var_dict[s])
					var_values.append(temp_const)
				init_consts.append(And(var_values))
			solver.add(Or(init_consts))

			for j in range(1, bound+1):
				solver.add(get_encoding(model, j))

			#solver.add(exclude_graph(graph, bound))

			target_consts = []

			for n in target_states: 
				var_values = []
				for s in n.var_dict: 
					x = Int (s + '.' + str(bound))
					temp_const = (x == n.var_dict[s])
					var_values.append(temp_const)
				target_consts.append(And(var_values))
			
			count = 0
			while (solver.check(Or(target_consts)) == sat): 
				count = count + 1
				if count > 100: 
					break
				path = solver.model()
				graph.add_path(path)
				solver.add(exclude_path(path))
			bound = bound+1

		curr = curr + step





############################################################
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
base = int(json_data['base'])
step = int(json_data['step'])
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




prob = 0

#increase the size of the counterexample graph until its 
#probability surpasses the probability bound specified by
#user
max_search_bound = 2

while prob <= prob_bound:
	
	expand_graph(graph, property_val, step, base, property_var, max_search_bound)	
	prob = graph.model_check(model, model_name, prism, csl_prop)
	print('size: ' + str(len(graph.node_list)))
	#print(max_search_bound)
	print(prob)
	#add_paths(graph, property_val, step, base, property_var, max_search_bound)
	count = 0
	# #if prob> 1e-20:
	count, prob, terminate = construct_path_2(graph, model, model_name, prism, csl_prop, max_search_bound, count, prob, prob_bound, property_var, property_val, mc_step)
	#max_search_bound = max_search_bound + 1
	# prob = graph.model_check(model, model_name, prism, csl_prop)
	# print(prob)

print('=' * 40)
print('=' * 40)
print('Result:')
# print('total # of paths: ' + str(count))
# print('# of seed paths: ' + str(seed_count))
prob = graph.model_check(model, model_name, prism, csl_prop)
print('probability of the counterexample subgraph= ' + str(prob))


