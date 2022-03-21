#script takes two or three inputs: 
#input1: model file
#input2: bound to check for the model
#input3: 0 or 1. 1 indicates there is a fourth input containing the encoding of solver for bound-1 on the model 
#input4: if input3==1 then it's the file containing encoding of solver for bound-1. If not present, it's assumed the file-name is constraints.smt
#the output will be saved in constraints.smt file

from z3 import *
import importlib
import os, sys
from Graph import Graph, Node, Edge
from scaffold import scaffold, loop_constraints, sort_first, exclude_path, exclude_path_scaffold
from scaffold import states_from_graph, exclude_graph
import timeit
#########################
	
def add_edges_from_path(graph, path): 
	index = -1
	for i in path.decls(): 
		index_temp = int(i.name()[i.name().rfind('.')+1:])
		if index_temp > index: 
			index = index_temp

	node_list = [None] * (index+1)

	for i in path.decls():
		index_temp = int(i.name()[i.name().rfind('.')+1:])
		if node_list[index_temp] == None: 
			node_list[index_temp] = []
		node_list[index_temp].append([i.name()[1:i.name().find('.')], str(path[i])])

	for n in node_list: 
		n.sort(key=sort_first)

	#print (node_list)
	node_list_len = len(node_list)
	for i in range(node_list_len-1): 
		from_node_name = '['
		to_node_name = '['
		
		
		from_cell = node_list[i]
		to_cell = node_list[i+1]

		for j, c in enumerate(from_cell):
			if j == 0: 
				from_node_name = from_node_name + str(c[1])
			else: 
				from_node_name = from_node_name + ',' + str(c[1])
		
		for j, c in enumerate(to_cell):
			if j == 0:
				to_node_name = to_node_name + str(c[1])
			else:
				to_node_name = to_node_name + ',' + str(c[1])

		from_node_name = from_node_name + ']'
		to_node_name = to_node_name + ']'
		from_node = Node.Node(from_node_name)
		to_node = Node.Node(to_node_name)
		temp = to_node_name[:to_node_name.rfind(',')]
		temp = temp[temp.rfind(',')+1:]
		if (temp=='40'):
			to_node.make_terminal()
		edge = Edge.Edge(from_node, to_node)
		graph.add_edges([edge])

	
#importing the python script for model specified in input1 as module
if '/' in sys.argv[1]:
	module_path = sys.argv[1][0:sys.argv[1].rfind('/')+1]
	sys.path.insert(0, os.getcwd()+'/'+module_path)
	sys.path.insert(0, module_path)

	module_name = sys.argv[1][sys.argv[1].rfind('/')+1:len(sys.argv[1])]
	module_name = module_name[0:module_name.rfind('.')]
else:
	module_name = sys.argv[1][0:sys.argv[1].rfind('.')]
model = importlib.import_module(module_name)
#


if len(sys.argv)>4:
	constraints_file = sys.argv[4]
else:
	constraints_file = 'constraints.smt'

graph_file = 'graph.g'

bound_ = int(sys.argv[2])

solver = Solver()
graph = Graph.Graph()

bound = 0
flag = False

while bound<=bound_: 

	if bound==0:
		init_const, init_node, state_vector = model.get_initial_state()
		graph.add_nodes(init_node)
		bound = bound + 1


	if (sys.argv[3]=='1') and (bound!=0): 
		
		solver = Solver()
		#adding initial states
		solver.add(states_from_graph(graph, 0))
		solver.add(exclude_graph(graph, bound))
		print(solver)
		for i in range(1, bound+1):
			solver.add(model.get_encoding(bound))
		count = 0
		print('bound: ' + str(bound))
		if flag:
			if (solver.check(Or(states_from_graph(graph, bound), model.get_property(bound)))==sat):
				path=solver.model()
				add_edges_from_path(graph, path)
				bound=1
				count = count+1
			else:
				bound = bound + 1
		else: 
			if (solver.check(model.get_property(bound))==sat):
				path=solver.model()
				add_edges_from_path(graph, path)
				bound=1
				count = count+1
				flag = True
				print('here')
				print(solver)
			else:
				bound = bound + 1

print('# of paths: ' + str(count))

graph.to_file(graph_file, state_vector)



