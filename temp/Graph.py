#from z3 import Solver
import numpy as np
import math



#var_dict a dictionary assining values to the model's variables
#out_reactions is a set containing all the indices of reactions
#going out of the node in the graph
class node:
	def __init__(self, var_dict): 
		self.var_dict = var_dict
		self.is_initial = False
		self.out_reactions = set()
		self.index = -1
		self.out_edges = []

	def make_initial(self): 
		self.is_initial = True

	def equals(self, node_): 
		if self.var_dict == node_.var_dict: 
			return True
		return False

	def set_index(self, index_): 
		self.index = index_

	def add_out_edge(self, edge_): 
		self.out_edges.append(edge_)


#an edge has two nodes n1:source node, n2: destination node
#an edge has a reaction index
class edge: 
	def __init__(self, n1, n2, reaction): 
		self.n1 = n1
		self.n2 = n2
		self.reaction = reaction

	def equals(self, edge_): 
		if self.n1.equals(edge_.n1):
			if self.n2.equals(edge_.n2): 
				if self.reaction == edge_.reaction:
					return True
		return False

	def get_node_list(self): 
		return [self.n1, self.n2]


class graph: 
	def __init__(self):
		self.node_list = []
		self.edge_list = []

	def add_node(self, node_): 
		flag = True
		for j in self.node_list:
			if node_.equals(j): 
				flag = False
		if flag:
			self.node_list.append(node_) 

	#if the source node of an edge is already present
	def add_edge(self, edge_): 
		flag = True
		for j in self.edge_list: 
			if edge_.equals(j): 
				flag = False
		if flag:
			contains_node1 = False
			contains_node2 = False
			for n in self.node_list: 
				if n.equals(edge_.get_node_list()[0]): 
					contains_node1=True
					edge_.n1 = n
					node1 = n
				if n.equals(edge_.get_node_list()[1]):
					contains_node2=True
					edge_.n2 = n
			
			if not (contains_node1): 
				self.node_list.append(edge_.get_node_list()[0])

			if not (contains_node2): 
				self.node_list.append(edge_.get_node_list()[1]) 
			
			self.edge_list.append(edge_)
			node1 = edge_.get_node_list()[0]
			node1.add_out_edge(edge_)

	def is_empty(self): 
		if len(self.node_list) == 0: 
			return True
		return False

	def add_path(self, path): 
		#find the last index (length) of the path
		index = -1
		for i in path.decls(): 
			index_temp = int(i.name()[i.name().rfind('.')+1:])
			if index_temp > index: 
				index = index_temp

		node_ordered_list = [None] * (index+1)

		for i in path.decls():
			index_temp = int(i.name()[i.name().rfind('.')+1:])
			if node_ordered_list[index_temp] == None: 
				node_ordered_list[index_temp] = []
			node_ordered_list[index_temp].append([i.name()[:i.name().find('.')], int(str(path[i]))])

		for i in range(index): 
		
			var_dict_from = {}
			for e in node_ordered_list[i]: 
				if e[0] != 'selected_reaction':
					var_dict_from[e[0]]=e[1]
				else: 
					selected_reaction = e[1]
			
			var_dict_to = {}
			for e in node_ordered_list[i+1]: 
				if e[0] != 'selected_reaction':
					var_dict_to[e[0]]=e[1]

			from_node = node(var_dict_from)
			to_node = node(var_dict_to)
			edge_ = edge(from_node, to_node, selected_reaction)
			self.add_edge(edge_)


	def to_file(self, file_name_prefix, model): 
		species_vector = model.species_vector()
		initial_state_index = -1
		sink_state_index = -2

		#the states file (.sta)
		states_file_name = file_name_prefix + '.sta'
		with open(states_file_name, mode='w', encoding='ascii') as f:
			f.truncate()
			state_vector_line = '('
			for e in species_vector: 
				state_vector_line = state_vector_line + e + ','
			state_vector_line_list = list(state_vector_line)
			state_vector_line_list[-1] = ')'
			state_vector_line = ''.join(state_vector_line_list)
			f.write(state_vector_line)
			f.write('\n')

			for i, n in enumerate(self.node_list): 
				if n.is_initial:
					initial_state_index = i
				n.set_index(i)
				line = str(i) + ':('
				for s in species_vector: 
					line = line + str(n.var_dict[s]) + ','
				line_list = list(line)
				line_list[-1] = ')'
				line = ''.join(line_list)
				f.write(line)
				f.write('\n')
			sink_line = str(self.node_list[-1].index + 1) + ':('
			for e in species_vector:
				sink_line = sink_line + '-1,'
			sink_line_list = list(sink_line)
			sink_line_list[-1] = ')'
			sink_line = ''.join(sink_line_list)
			f.write(sink_line)
			f.close()

		#the labels file (.lab)
		labels_file_name = file_name_prefix + '.lab'
		with open(labels_file_name, mode='w', encoding='ascii') as f:
			f.truncate()
			sink_state_index = self.node_list[-1].index + 1
			lab_line = '0="init" 1="deadlock" 2="sink"'
			f.write(lab_line)
			f.write('\n')
			f.write(str(initial_state_index) + ': 0')
			f.write('\n')
			f.write(str(sink_state_index) + ': 2')
			f.close()

		#the transitions file (.tra)
		rate = float()
		trans_list  = [[]] * len(self.node_list)
			
		for i, n in enumerate(self.node_list):
			#get the state-vector for node n
			var_values = [None] * len(species_vector)
			for j, s in enumerate(species_vector):
				var_values[j] = n.var_dict[s]

			current_rate = 0
			total_rate = 0

			trans_list_temp = []
			for e in n.out_edges:
				comb = 1
				for it, r in enumerate(model.reactions_vector()[e.reaction][0]):
					for c in range(r): 
						comb = comb * var_values[it]

				rate = model.reaction_rates()[e.reaction-1]
				rate = rate * comb
				trans_list_temp.append([n.index, e.get_node_list()[1].index, rate])
				current_rate = current_rate + rate

			for j, r in enumerate(model.reactions_vector().values()):
				comb = 1
				rate = model.reaction_rates()[j]
				for it, v in enumerate(r[0]):
					for c in range(v): 
						comb = comb * var_values[it]
				rate = rate * comb
				total_rate = total_rate + rate

			remaining_rate = total_rate - current_rate
			if remaining_rate > 0:
				trans_list_temp.append([n.index, sink_state_index, remaining_rate])
			trans_list[i] = trans_list_temp

		trans_file_name = file_name_prefix + '.tra'
		with open(trans_file_name, mode='w', encoding='ascii') as f:
			f.truncate()
			num_transitions = 0
			for n in trans_list: 
				for e in n: 
					num_transitions = num_transitions + 1
			
			first_line = str(len(self.node_list)+1) + ' ' + str(num_transitions)
			f.write(first_line)
			f.write('\n')
			for n in trans_list: 
				for e in n:
					line = str(int(e[0])) + ' ' + str(int(e[1])) + ' ' + str(e[2])
					f.write(line)
					f.write('\n')
			f.close()

