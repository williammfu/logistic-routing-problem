"""
Pathfinding module
to generate a complete subgraph
using A* algorithm
"""
import networkx as nx
import heapq

heuristics = []
livenodes = [] # Priority Queue

class Node:

    def __init__(self, node, path, distance, parent=None):
        self.parent = parent
        self.node = node
        self.path = path
        self.path.append(node)
        self.distance = distance
        self.cost = self.distance + heuristics[node]
    
    def __lt__(self, value):
        return self.cost < value.cost

    def __str__(self):
        return str(self.path) + "," + str(self.cost)

def get_X(node):
    return node[1][0]

def get_Y(node):
    return node[1][1]

def calculate_euc_dist(node1, node2):
    return ((get_X(node1) - get_X(node2))**2 + (get_Y(node1) - get_Y(node2))**2)**0.5

def fill_heuristics(G, goal):
    nodes = list(G.nodes.data('pos'))
    goal_node = nodes[goal]
    for node in nodes:
        heuristics.append(calculate_euc_dist(node, goal_node))

def a_star(G, start, goal):

    awaken = 1
    livenodes.clear()
    heuristics.clear()
    fill_heuristics(G, goal)
    # livenodes.append(Node(start, [], 0))
    heapq.heappush(livenodes, Node(start, [], 0))
    current_node = Node(start, [], 0) # Dummy element

    while current_node.node != goal:

        # current_node = livenodes.pop(livenodes.index(min(livenodes)))
        current_node = heapq.heappop(livenodes)
        current_distance = current_node.distance
        node = current_node.node

        incidences = G.edges(node)

        for incidence in incidences:
            next_node = incidence[1]

            if next_node not in current_node.path:
                distance = G.get_edge_data(incidence[0], incidence[1])['weight']
                to_add = Node(next_node, list.copy(current_node.path), current_distance + distance, parent=current_node)
                # livenodes.append(to_add)
                heapq.heappush(livenodes, to_add)
                awaken += 1


    print(current_node.path)
    print("Nodes:", awaken)
    return current_node.distance