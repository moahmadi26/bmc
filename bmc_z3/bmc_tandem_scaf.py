#script takes three or four inputs: 
#input1: model file
#input2: bound to check for the model
#input3: 0 or 1. 1 indicates there is a fourth input containing the encoding of solver for bound-1 on the model 
#input4: if input3==1 then it's the file containing encoding of solver for bound-1. If not present, it's assumed the file-name is constraints.smt
#the output will be saved in constraints.smt file

from z3 import *
import importlib
import os, sys
from Graph import Graph, Node, Edge
from time import time
#########################

def exclude_path(path): 
	assignments = []
	for d in path.decls(): 
		x = Int(d.name())
		assignments.append(x  == path[d])
	return Not(And(assignments))

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
				node_list.append([j.name()[:j.name().find('.')], path[j]])
		node_list.sort(key=sort_first)
		nodes.append(node_list)
	
	
	count = 0
	for i in range(0, index): 
		print(i)
		scaff_solver = Solver()
		for j in range(0, i+1):
			sc_j = Int('sc.{0}'.format(j))
			ph_j = Int('ph.{0}'.format(j))
			sm_j = Int('sm.{0}'.format(j))
			state = And(sc_j == nodes[j][0][1],ph_j == nodes[j][1][1], sm_j == nodes[j][2][1])
			scaff_solver.add(state)
		flag = False
		for j in range(i+1, i+bound): 
			scaff_solver.add(model.get_encoding(j)) 
			flag = True
		if flag: 
			scaff_solver.add(model.get_encoding(i+bound))
		for j in range(i+bound, index+bound):
			sc_j = Int('sc.{0}'.format(j))
			ph_j = Int('ph.{0}'.format(j))
			sm_j = Int('sm.{0}'.format(j))
			state = And(sc_j == nodes[j-bound+1][0][1], ph_j == nodes[j-bound+1][1][1], sm_j == nodes[j-bound+1][2][1])
			scaff_solver.add(state)

		# smt2 = scaff_solver.sexpr()
		# with open('file.smt', mode='w', encoding='ascii') as f:
		# 	f.truncate()
		# 	f.write(smt2)
		# 	f.close()
		while (scaff_solver.check()==sat):
			path=scaff_solver.model()
			scaff_solver.add(exclude_path(path))
			scaff_paths.append(path)
		# 	count = count + 1
		# 	print(count)
		# for path in scaff_paths: 
		# 	print ('+' * 50)
		# 	index = -1
		# 	for i in path.decls(): 
		# 		index_temp = int(i.name()[i.name().rfind('.')+1:])
		# 		if index_temp > index: 
		# 			index = index_temp

		# 	nodes = []
		# 	for i in range(0, index+1): 
		# 		node_list = []
		# 		for j in path.decls(): 
		# 			if int(j.name()[j.name().rfind('.')+1:])==i: 
		# 				node_list.append([j.name()[:j.name().find('.')], path[j]])
		# 		node_list.sort(key=sort_first)
		# 		nodes.append(node_list)

		# 	for node in nodes:
		# 		print(node)

	
	print("number of scaff paths: %d" % (len(scaff_paths)))
	return scaff_paths

				
	

def sort_first(val): 
	if val[0]=='sc':
		return 0
	elif val[0]=='ph':
		return 1
	else:
		return 2

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
		node_list[index_temp].append([i.name()[:i.name().find('.')], str(path[i])])

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
		temp = to_node_name[1:to_node_name.find(',')]
		if (temp=='127'):
			to_node.make_terminal()
		edge = Edge.Edge(from_node, to_node)
		graph.add_edges([edge])

	# index = -1
	# for i in path.decls(): 
	# 	index_temp = int(i.name()[i.name().rfind('.')+1:])
	# 	if index_temp > index: 
	# 		index = index_temp

	

	# for i in range(0, index): 
	# 	from_node_name = '['
	# 	from_node_list = []
	# 	to_node_name = '['
	# 	to_node_list = []
	# 	for j in path.decls(): 
	# 		if int(j.name()[j.name().rfind('.')+1:])==i: 
	# 			from_node_list.append([j.name()[:j.name().find('.')], str(path[j])])
	# 		if int(j.name()[j.name().rfind('.')+1:])==i+1: 
	# 			to_node_list.append([j.name()[:j.name().find('.')], str(path[j])])

	# 	from_node_list.sort(key=sort_first)
	# 	to_node_list.sort(key=sort_first)

	# 	flag = False
	# 	for l in from_node_list: 
	# 		if flag == False: 
	# 			from_node_name = from_node_name + str(l[1])
	# 			flag = True
	# 		else: 
	# 			from_node_name = from_node_name + ',' + str(l[1])
	# 	from_node_name = from_node_name + ']'
	# 	flag = False
	# 	for l in to_node_list: 
	# 		if flag == False: 
	# 			to_node_name = to_node_name + str(l[1])
	# 			flag = True
	# 		else: 
	# 			to_node_name = to_node_name + ',' + str(l[1])
	# 	to_node_name = to_node_name + ']'
	# 	from_node = Node.Node(from_node_name)
	# 	to_node = Node.Node(to_node_name)
	# 	temp = to_node_name[1:to_node_name.find(',')]

	# 	if (temp=='127'):
	# 		to_node.make_terminal()
	# 	edge = Edge.Edge(from_node, to_node)
	# 	graph.add_edges([edge])

def loop_constraints(bound):
	constraints = []
	sc = Int('sc.{0}'.format(bound))
	ph = Int('ph.{0}'.format(bound))
	sm = Int('sm.{0}'.format(bound))


	for i in range(0,bound):
		sc_temp = Int('sc.{0}'.format(i))
		ph_temp = Int('ph.{0}'.format(i))
		sm_temp = Int('sm.{0}'.format(i))
		constraints.append(Not(And((sc == sc_temp), (ph == ph_temp), (sm == sm_temp))))

	return And(constraints)

def add_loops_to_graph(model, graph, loop_size):
	loop_solver = Solver()
	paths = []
	#print(loop_solver.sexpr())
	for i in range(2,loop_size): 
		for n in graph.nodes:
			loop_solver.push()
			if not (n.marked):
				s2_1 = Int('s2.{0}'.format(0))
				loop_solver.add(s2_1 == n.get_int())
				for j in range(1,i+1): 
					loop_solver.add(model.get_encoding(j))
				x_temp = Int('s2.{0}'.format(i))
				loop_solver.add(s2_1 == x_temp)
				n.mark()
				while (loop_solver.check()==sat):
					path=loop_solver.model()
					paths.append(path)
					loop_solver.add(exclude_path(path))
					#print(loop_solver.sexpr())
			loop_solver.pop()

	for path in paths:
		add_edges_from_path(graph, path)



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
	constraints_file = '/Users/mo/usf/projects/probmc/ProbMC/SMT_BMC/src/constraints.smt'
	constraints_file = 'constraints.smt'

graph_file = '/Users/mo/usf/projects/probmc/ProbMC/SMT_BMC/src/graph.g'
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
	time1 = time()
	state_vector = graph.from_file(graph_file)
	time2 = time()
	solver.from_file(constraints_file)
	time3 = time()
	solver.add(model.get_encoding(bound))
	time4 = time()
	#solver.add(loop_constraints(bound))
	time5 = time()
	#solver.push()
	#solver.add(model.get_property(bound))
	count = 0
	flag = False
	time6 = time()
	time7 = time()
	time8 = time()
	time9 = time()
	time10 = time()
	time11 = time()
	print('bound: ' + str(bound))
	if bound > 126:
		time6 = time()
		while (solver.check(model.get_property(bound))==sat):
			time7 = time()
			path=solver.model()
			time8 = time()
			add_edges_from_path(graph, path)
			time9 = time()
			#solver.pop()
			solver.add(exclude_path(path))
			print('='*40)
			scaff_paths = scaffold(path,4,model)
			print('here')
			temp_count=0
			for path_ in scaff_paths:
				add_edges_from_path(graph, path_)
				temp_count = temp_count + 1
				print(temp_count)
				solver.add(exclude_path(path_))
				print(temp_count)
			print('number of scaff pahts = %d' % (len(scaff_paths)))
			#solver.push()
			time10 = time()
			#solver.add(model.get_property(bound))
			count = count+1
			flag = True
		time11 = time()
	time12 = time()
	#solver.pop()
	print('# of paths: ' + str(count))
	print(f'time to read from graph: {(time2 - time1)/(time12-time1)}')
	print(f'time to read solver status: {(time3 - time2)/(time12-time1)}')
	print(f'time to add encoding: {(time4 - time3)/(time12-time1)}')
	print(f'time to add loop constraints: {(time5 - time4)/(time12-time1)}')
	print(f'time to solve: {(time7 - time6)/(time12-time1)}')
	print(f'time to get the path: {(time8 - time7)/(time12-time1)}')
	print(f'time to add edges: {(time9 - time8)/(time12-time1)}')
	print(f'time to add exclude path: {(time10 - time9)/(time12-time1)}')
	print(f'time in while loop: {(time11 - time6)/(time12-time1)}')
	# if flag or bound>25:
	# 	add_loops_to_graph(model, graph, 3)
	smt2 = solver.sexpr()
	with open(constraints_file, mode='w', encoding='ascii') as f:
		f.truncate()
		f.write(smt2)
		f.close()
	graph.to_file(graph_file, state_vector)



