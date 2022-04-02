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
#########################
def exclude_path(path): 
	assignments = []
	for d in path.decls(): 
		x = Int(d.name())
		assignments.append(x  == path[d])
	return Not(And(assignments))

def sort_first(val): 
	if val[0]== 'R':
		return 0
	elif val[0]=='L':
		return 1
	elif val[0]=='RL':
		return 2
	elif val[0]=='G':
		return 3
	elif val[0]=='G_a':
		return 4
	elif val[0]=='G_bg':
		return 5
	elif val[0]=='G_d':
		return 6
	else:
		print (val[0])
		return -1

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
		node_list[index_temp].append([i.name()[0:i.name().find('.')], str(path[i])])

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
		if (temp=='50'):
			to_node.make_terminal()
		edge = Edge.Edge(from_node, to_node)
		graph.add_edges([edge])

def loop_constraints(bound):
	constraints = []
	
	R_ = Int('R.{0}'.format(bound))
	L_ = Int('L.{0}'.format(bound))
	RL_ = Int('RL.{0}'.format(bound))
	G_ = Int('G.{0}'.format(bound))
	G_a_ = Int('G_a.{0}'.format(bound))
	G_bg_ = Int('G_bg.{0}'.format(bound))
	G_d_ = Int('G_d.{0}'.format(bound))
	

	for i in range(0,bound):
		R = Int('R.{0}'.format(i))
		L = Int('L.{0}'.format(i))
		RL = Int('RL.{0}'.format(i))
		G = Int('G.{0}'.format(i))
		G_a = Int('G_a.{0}'.format(i))
		G_bg = Int('G_bg.{0}'.format(i))
		G_d = Int('G_d.{0}'.format(i))

		constraints.append(Not(And((R_ == R), (L_ == L), (RL_ == RL), (G_ == G), (G_a_ == G_a), (G_bg_ == G_bg), (G_d_ == G_d))))

	return And(constraints)


#########################


#importing the python script for model specified in input1 as module
if '/' in sys.argv[1]:
	module_path = sys.argv[1][0:sys.argv[1].rfind('/')+1]
	sys.path.insert(0, os.getcwd()+'/'+module_path)
	sys.path.insert(0, module_path)

	module_name = sys.argv[1][sys.argv[1].rfind('/')+1:len(sys.argv[1])]
	module_name = module_name[0:module_name.rfind('.')]
else:
	module_name = sys.argv[1][0:module_name.rfind('.')]
model = importlib.import_module(module_name)
#


if len(sys.argv)>4:
	constraints_file = sys.argv[4]
else:
	constraints_file = 'constraints.smt'

graph_file = 'graph.g'

bound = int(sys.argv[2])
solver = Solver()
graph = Graph.Graph()



if bound==0:
	init_const, init_node, state_vector = model.get_initial_state()
	graph.add_nodes(init_node)
	solver.add(init_const)

	
	for i in range (1,100):
		solver.add(model.get_encoding(i))

	smt2 = solver.sexpr()
	with open(constraints_file, mode='w', encoding='ascii') as f:
		f.truncate()
		f.write(smt2)
		f.close()
	graph.to_file(graph_file, state_vector)



elif (sys.argv[3]=='1') and (bound!=0): 
	if bound<100: 
		print('bound: ' + str(bound))
		exit()
	state_vector = graph.from_file(graph_file)
	solver.from_file(constraints_file)
	solver.add(model.get_encoding(bound))
	solver.add(loop_constraints(bound))
	count = 0
	flag = False
	print('bound: ' + str(bound))
	while (solver.check(model.get_property(bound))==sat):
		path=solver.model()
		add_edges_from_path(graph, path)
		solver.add(exclude_path(path))
		count = count+1
		print(count)
		flag = True
		graph.to_file(graph_file, state_vector)
		if count==10:
			break

	print('# of paths: ' + str(count))
	smt2 = solver.sexpr()
	with open(constraints_file, mode='w', encoding='ascii') as f:
		f.truncate()
		f.write(smt2)
		f.close()
	graph.to_file(graph_file, state_vector)



