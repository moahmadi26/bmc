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
import timeit
#########################
def exclude_path(path): 
	assignments = []
	for d in path.decls(): 
		x = Int(d.name())
		assignments.append(x == path[d])
	return Not(And(assignments))

def sort_first(val): 
	return val[0]

def scaffold(path, bound, model): 	
	scaff_paths = []
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
	
	count = 0
	for i in range(0, index): 
		scaff_solver = Solver()
		for j in range(0, i+1):
			s1_j = Int('s1.{0}'.format(j))
			s2_j = Int('s2.{0}'.format(j))
			s3_j = Int('s3.{0}'.format(j))
			s4_j = Int('s4.{0}'.format(j))
			s5_j = Int('s5.{0}'.format(j))
			s6_j = Int('s6.{0}'.format(j))
			state = And(s1_j == nodes[j][0][1],s2_j == nodes[j][1][1], s3_j == nodes[j][2][1], s4_j == nodes[j][3][1], s5_j == nodes[j][4][1], s6_j == nodes[j][5][1])
			scaff_solver.add(state)
		flag = False
		for j in range(i+1, i+bound): 
			scaff_solver.add(model.get_encoding(j)) 
			flag = True
		if flag: 
			scaff_solver.add(model.get_encoding(i+bound))
		for j in range(i+bound, index+bound):
			s1_j = Int('s1.{0}'.format(j))
			s2_j = Int('s2.{0}'.format(j))
			s3_j = Int('s3.{0}'.format(j))
			s4_j = Int('s4.{0}'.format(j))
			s5_j = Int('s5.{0}'.format(j))
			s6_j = Int('s6.{0}'.format(j))
			state = And(s1_j == nodes[j-bound+1][0][1],s2_j == nodes[j-bound+1][1][1], s3_j == nodes[j-bound+1][2][1], s4_j == nodes[j-bound+1][3][1], s5_j == nodes[j-bound+1][4][1], s6_j == nodes[j-bound+1][5][1])
			scaff_solver.add(state)

		
		while (scaff_solver.check()==sat):
			path=scaff_solver.model()
			scaff_solver.add(exclude_path(path))
			scaff_paths.append(path)

	
	#print("number of scaff paths: %d" % (len(scaff_paths)))
	return scaff_paths

				
	
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

# def add_loops_to_graph(model, graph, loop_size):
# 	loop_solver = Solver()
# 	paths = []
# 	#print(loop_solver.sexpr())
# 	for i in range(2,loop_size): 
# 		for n in graph.nodes:
# 			loop_solver.push()
# 			if not (n.marked):
# 				s2_1 = Int('s2.{0}'.format(0))
# 				loop_solver.add(s2_1 == n.get_int())
# 				for j in range(1,i+1): 
# 					loop_solver.add(model.get_encoding(j))
# 				x_temp = Int('s2.{0}'.format(i))
# 				loop_solver.add(s2_1 == x_temp)
# 				n.mark()
# 				while (loop_solver.check()==sat):
# 					path=loop_solver.model()
# 					paths.append(path)
# 					loop_solver.add(exclude_path(path))
# 					#print(loop_solver.sexpr())
# 			loop_solver.pop()

# 	for path in paths:
# 		add_edges_from_path(graph, path)



#########################


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

bound = int(sys.argv[2])
solver = Solver()
graph = Graph.Graph()



if bound==0:
	init_const, init_node, state_vector = model.get_initial_state()
	graph.add_nodes(init_node)
	solver.add(init_const)
	smt2 = solver.sexpr()
	with open(constraints_file, mode='w', encoding='ascii') as f:
		f.truncate()
		f.write(smt2)
		f.close()
	graph.to_file(graph_file, state_vector)



if (sys.argv[3]=='1') and (bound!=0): 
	state_vector = graph.from_file(graph_file)
	solver.from_file(constraints_file)
	solver.add(model.get_encoding(bound))
	solver.add(loop_constraints(bound))
	count = 0
	flag = False
	print('bound: ' + str(bound))
	num_scaff_paths = 0
	p_bound = Real('p.{0}'.format(bound))
	prob_bound = 8E-25
	while (solver.check(And(model.get_property(bound)), p_bound>prob_bound)==sat):
		path=solver.model()
		add_edges_from_path(graph, path)
		solver.add(exclude_path(path))
		#scaff_paths = scaffold(path,3,model)
		scaff_paths = []
		for path_ in scaff_paths:
			add_edges_from_path(graph, path_)
			num_scaff_paths = num_scaff_paths + 1
			#solver.add(exclude_path(path_))
		
		count = count+1
		flag = True
		if bound==19:
			smt2 = solver.sexpr()
			with open('test.smt', mode='w', encoding='ascii') as f:
				f.truncate()
				f.write(smt2)
				f.close()

	print('# of paths: ' + str(count))
	print('# of scaff pahts = %d' % (num_scaff_paths))
	# if flag or bound>25:
	# 	add_loops_to_graph(model, graph, 3)
	smt2 = solver.sexpr()
	with open(constraints_file, mode='w', encoding='ascii') as f:
		f.truncate()
		f.write(smt2)
		f.close()
	graph.to_file(graph_file, state_vector)



