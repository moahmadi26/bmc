class Edge: 
	def __init__(self, n1, n2): 
		self.n1 = n1
		self.n2 = n2

	def equals(self, edge): 
		if self.n1.equals(edge.n1):
			if self.n2.equals(edge.n2): 
				return True
		return False

	def get_nodes(self): 
		return [self.n1, self.n2]