from z3 import *
import importlib
import os, sys
from Graph import Graph, Node, Edge

def sort_first(val): 
	return val[0]

def exclude_path(path): 
	assignments = []
	for d in path.decls(): 
		x = Int(d.name())
		assignments.append(x == path[d])
	return Not(And(assignments))

def exclude_path_scaffold(path_state): 
	assignments = []
	for ps in path_state: 
		for e in ps: 
			x = Int(e[0])
			assignments.append(x == e[1])
	return Not(And(assignments))

def loop_constraints(bound):
	constraints = []
	x1 = Int('s1.{0}'.format(bound))
	x2 = Int('s2.{0}'.format(bound))
	x3 = Int('s3.{0}'.format(bound))
	x4 = Int('s4.{0}'.format(bound))
	x5 = Int('s5.{0}'.format(bound))
	x6 = Int('s6.{0}'.format(bound))


	for i in range(0,bound):
		y1 = Int('s1.{0}'.format(i))
		y2 = Int('s2.{0}'.format(i))
		y3 = Int('s3.{0}'.format(i))
		y4 = Int('s4.{0}'.format(i))
		y5 = Int('s5.{0}'.format(i))
		y6 = Int('s6.{0}'.format(i))

		constraints.append(Not(And((x1 == y1), (x2 == y2), (x3 == y3), (x4 == y4), (x5 == y5), (x6 == y6))))

	return And(constraints)

def scaffold(path, bound, model): 	
	scaffold_paths = []
	index = -1
	for i in path.decls(): 
		index_temp = int(i.name()[i.name().rfind('.')+1:])
		if index_temp > index: 
			index = index_temp

	nodes = []

	for i in range(0, index+1): 
		node_list = []
		for j in path.decls(): 
			if int(j.name()[j.name().rfind('.')+1:])==i: 
				node_list.append([j.name()[1:j.name().find('.')], path[j]])
		node_list.sort(key=sort_first)
		nodes.append(node_list)
	
	scaffold_solver = Solver()
	path_states = []

	#don't find new paths that are already part of the path
	for i in range(0, index):
		s1_0 = Int('s1.{0}'.format(0))
		s2_0 = Int('s2.{0}'.format(0))
		s3_0 = Int('s3.{0}'.format(0))
		s4_0 = Int('s4.{0}'.format(0))
		s5_0 = Int('s5.{0}'.format(0))
		s6_0 = Int('s6.{0}'.format(0))
		state_0 = And(s1_0 == nodes[i][0][1],s2_0 == nodes[i][1][1])
		state_0 = And(state_0, s3_0 == nodes[i][2][1], s4_0 == nodes[i][3][1])
		state_0 = And(state_0, s5_0 == nodes[i][4][1], s6_0 == nodes[i][5][1])

		s1_1 = Int('s1.{0}'.format(1))
		s2_1 = Int('s2.{0}'.format(1))
		s3_1 = Int('s3.{0}'.format(1))
		s4_1 = Int('s4.{0}'.format(1))
		s5_1 = Int('s5.{0}'.format(1))
		s6_1 = Int('s6.{0}'.format(1))
		state_1 = And(s1_1 == nodes[i+1][0][1],s2_1 == nodes[i+1][1][1])
		state_1 = And(state_1, s3_1 == nodes[i+1][2][1], s4_1 == nodes[i+1][3][1])
		state_1 = And(state_1, s5_1 == nodes[i+1][4][1], s6_1 == nodes[i+1][5][1])
		path_states.append(And(state_0, state_1))

	path_states = Not(Or(path_states))
	scaffold_solver.add(path_states)
		

	init_state = []
	
	#any state on the path can be the initial state
	for i in range(0, index+1):
		s1 = Int('s1.{0}'.format(0))
		s2 = Int('s2.{0}'.format(0))
		s3 = Int('s3.{0}'.format(0))
		s4 = Int('s4.{0}'.format(0))
		s5 = Int('s5.{0}'.format(0))
		s6 = Int('s6.{0}'.format(0))
		state = And(s1 == nodes[i][0][1],s2 == nodes[i][1][1])
		state = And(state, s3 == nodes[i][2][1], s4 == nodes[i][3][1])
		state = And(state, s5 == nodes[i][4][1], s6 == nodes[i][5][1])
		init_state.append(state)

	init_state = Or(init_state)
	scaffold_solver.add(init_state)

	for b in range(1, bound+1):
		scaffold_solver.add(model.get_encoding(b))

		#no loops in scaffold paths 
		scaffold_solver.add(loop_constraints(b))
		
		target_state = []
		
		for i in range(0, index+1):
			s1 = Int('s1.{0}'.format(b))
			s2 = Int('s2.{0}'.format(b))
			s3 = Int('s3.{0}'.format(b))
			s4 = Int('s4.{0}'.format(b))
			s5 = Int('s5.{0}'.format(b))
			s6 = Int('s6.{0}'.format(b))
			state = And(s1 == nodes[i][0][1],s2 == nodes[i][1][1])
			state = And(state, s3 == nodes[i][2][1], s4 == nodes[i][3][1])
			state = And(state, s5 == nodes[i][4][1], s6 == nodes[i][5][1])
			target_state.append(state)

		target_state = Or(target_state)
		target_state_property = model.get_property(b)
		target_state = Or(target_state, target_state_property)

		
		while (scaffold_solver.check(target_state)==sat):
			path=scaffold_solver.model()
			scaffold_solver.add(exclude_path(path))
			scaffold_paths.append(path)
			#for d in path.decls(): 
				#print("%s = %s" %(d.name(), path[d]))
			#print('================================')


	scaffold_paths_to_exclude = []
	for path_ in scaffold_paths:
		index_ = -1
		for i in path_.decls(): 
			index_temp = int(i.name()[i.name().rfind('.')+1:])
			if index_temp > index_: 
				index_ = index_temp

		nodes_ = []

		for i in range(0, index_+1): 
			node_list = []
			for j in path_.decls(): 
				if int(j.name()[j.name().rfind('.')+1:])==i: 
					node_list.append([j.name()[1:j.name().find('.')], path_[j]])
			node_list.sort(key=sort_first)
			nodes_.append(node_list)
		
		path_list = []
		for i, node in enumerate(nodes):
			if (node[0][1]==nodes_[0][0][1] and node[1][1]==nodes_[0][1][1] and
				node[2][1]==nodes_[0][2][1] and node[3][1]==nodes_[0][3][1] and
				node[4][1]==nodes_[0][4][1] and node[5][1]==nodes_[0][5][1]):
				break_index = i

		for i in range(0, break_index+1): 
			path_list.append(nodes[i])

		for i in range(1, index_+1): 
			path_list.append(nodes_[i])

		for i, node in enumerate(nodes):
			if (node[0][1]==nodes_[-1][0][1] and node[1][1]==nodes_[-1][1][1] and
				node[2][1]==nodes_[-1][2][1] and node[3][1]==nodes_[-1][3][1] and
				node[4][1]==nodes_[-1][4][1] and node[5][1]==nodes_[-1][5][1]):
				break_index = i
		for i in range(break_index+1, index+1): 
			path_list.append(nodes[i])
		
		scaffold_paths_to_exclude.append([path_list, len(path_list)])




	#print("number of scaff paths: %d" % (len(scaff_paths)))
	return [scaffold_paths, scaffold_paths_to_exclude]


def exclude_graph(graph, bound): 
	assignments = []
	nodes = []
	for node in graph.nodes: 
		node_name = node.name
		s1 = node_name[1:node_name.find(',')]
		node_name = node_name[node_name.find(',')+1:]
		s2 = node_name[:node_name.find(',')]
		node_name = node_name[node_name.find(',')+1:]
		s3 = node_name[:node_name.find(',')]
		node_name = node_name[node_name.find(',')+1:]
		s4 = node_name[:node_name.find(',')]
		node_name = node_name[node_name.find(',')+1:]
		s5 = node_name[:node_name.find(',')]
		node_name = node_name[node_name.find(',')+1:]
		s6 = node_name[:node_name.find(',')]
		node_name = node_name[node_name.find(',')+1:node_name.find(']')]
		nodes.append([s1,s2,s3,s4,s5,s6])
	
	
	exclude_states = []
	for b in range (0, bound+1): 
		s1 = Int('s1.{0}'.format(b))
		s2 = Int('s2.{0}'.format(b))
		s3 = Int('s3.{0}'.format(b))
		s4 = Int('s4.{0}'.format(b))
		s5 = Int('s5.{0}'.format(b))
		s6 = Int('s6.{0}'.format(b))
		graph_states = []
		for e in nodes: 
			state = And(s1==e[0], s2==e[1], s3==e[2], s4==e[3], s5==e[4], s6==e[5])
			graph_states.append(state)
		exclude_states.append(graph_states)

	for es in exclude_states: 
		es = Not(Or(es))
		assignments.append(es)
	assignments = Or(assignments)
	return assignments


def states_from_graph(graph, state_bound):
	nodes = []
	for node in graph.nodes: 
		node_name = node.name
		s1 = node_name[1:node_name.find(',')]
		node_name = node_name[node_name.find(',')+1:]
		s2 = node_name[:node_name.find(',')]
		node_name = node_name[node_name.find(',')+1:]
		s3 = node_name[:node_name.find(',')]
		node_name = node_name[node_name.find(',')+1:]
		s4 = node_name[:node_name.find(',')]
		node_name = node_name[node_name.find(',')+1:]
		s5 = node_name[:node_name.find(',')]
		node_name = node_name[node_name.find(',')+1:]
		s6 = node_name[:node_name.find(',')]
		node_name = node_name[node_name.find(',')+1:node_name.find(']')]
		nodes.append([s1,s2,s3,s4,s5,s6])

	s1 = Int('s1.{0}'.format(state_bound))
	s2 = Int('s2.{0}'.format(state_bound))
	s3 = Int('s3.{0}'.format(state_bound))
	s4 = Int('s4.{0}'.format(state_bound))
	s5 = Int('s5.{0}'.format(state_bound))
	s6 = Int('s6.{0}'.format(state_bound))

	graph_states = []
	for e in nodes: 
		state = And(s1==e[0], s2==e[1], s3==e[2], s4==e[3], s5==e[4], s6==e[5])
		graph_states.append(state)
	return (Or(graph_states))




