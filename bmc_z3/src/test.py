from scaffold import exclude_graph
from Graph import Graph, Node, Edge

graph = Graph.Graph()
node1 = Node.Node('[14,32,25,64,12,15]')
node2 = Node.Node('[12,13,14,15,16,17]')
graph.add_nodes([node1, node2])

exclude_graph(graph,1)