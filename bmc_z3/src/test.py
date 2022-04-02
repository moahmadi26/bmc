from z3 import *
from scaffold import exclude_graph, states_from_graph
from Graph import Graph, Node, Edge

graph = Graph.Graph()
node1 = Node.Node('[14,32,25,64,12,15]')
node2 = Node.Node('[12,13,14,15,16,17]')
graph.add_nodes([node1, node2])
print(exclude_graph(graph,1))

graph.nodes = []
graph.edges = []

print (states_from_graph(graph, 3))
solver = Solver()
x1 = Int('x0')
solver.add(x1==2)
solver.add(False)
print(solver)
if (solver.check()==sat):
	path = solver.model()
	for d in path.decls(): 
		print('%s = %s' %(d.name(), path[d]))