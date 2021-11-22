from Graph import Node, Edge
class Graph: 

	def __init__(self):
		self.nodes = []
		self.edges = []

	def add_nodes(self, nodes): 
		for i in nodes: 
			flag = True
			for j in self.nodes:
				if i.equals(j): 
					flag = False
			if flag:
				self.nodes.append(i)

	def add_edges(self, edges): 
		for i in edges: 
			flag = True
			for j in self.edges: 
				if i.equals(j): 
					flag = False
			if flag:
				contains_node1 = False
				contains_node2 = False
				for n in self.nodes: 
					if n.equals(i.get_nodes()[0]): 
						contains_node1=True
					if n.equals(i.get_nodes()[1]):
						contains_node2=True
				if not (contains_node1): 
					node = Node.Node(i.get_nodes()[0].name)
					if i.get_nodes()[0].is_terminal: 
						node.make_terminal()
					self.nodes.append(node)
				if not (contains_node2): 
					node = Node.Node(i.get_nodes()[1].name)
					if i.get_nodes()[1].is_terminal: 
						node.make_terminal()
					self.nodes.append(node) 
				self.edges.append(i)

	def to_file(self, filename, state_vector): 
		with open(filename, mode='w', encoding='ascii') as f: 
			f.truncate()
			f.write(state_vector)
			f.write('\n#')
			terminal_name = []
			for n in self.nodes: 
				if not (n.is_terminal): 
					f.write('\n')
					f.write(n.name)
				else:
					terminal_name.append(n.name)
			f.write('\n#\n')
			for i in terminal_name:
				f.write(i)
				f.write('\n')
			f.write('#')

			for e in self.edges:
				f.write('\n')
				node1 = e.get_nodes()[0]
				node2 = e.get_nodes()[1]
				f.write(node1.name)
				f.write(' ')
				f.write(node2.name)
			f.close()

	def from_file(self, filename): 
		state_vector = ''
		with open(filename, mode='r') as f: 
			state_vector = f.readline().strip('\n')
			while not ('#' in f.readline()): 
				pass
			line = f.readline().strip('\n')
			while not ('#' in line):
				node_name = line
				node = Node.Node(node_name)
				self.nodes.append(node)
				line = f.readline().strip('\n')
			line = f.readline().strip('\n')
			while not ('#' in line):
				node_name = line
				node = Node.Node(node_name)
				node.make_terminal()
				self.nodes.append(node)
				line = f.readline().strip('\n')
			for l in f:
				l = l.strip('\n')
				first_node = Node.Node(l[:l.find(' ')]) 
				second_node = Node.Node(l[l.find(' ')+1:])
				edge = Edge.Edge(first_node, second_node)
				self.edges.append(edge)
			f.close()
		return state_vector






