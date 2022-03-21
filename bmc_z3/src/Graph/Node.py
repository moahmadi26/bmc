class Node:

	def __init__(self, name): 
		self.name = name
		self.is_terminal = False
		self.marked = False

	def make_terminal(self): 
		self.is_terminal = True

	def equals(self, node): 
		if self.name == node.name: 
			return True
		return False

	def mark(self):
		self.marked = True

	def get_int(self): 
		return self.name[1:len(self.name)-1]
