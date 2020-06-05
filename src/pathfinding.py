"""
Pathfinding module
to generate a complete subgraph
using A* algorithm
"""
import networkx as nx
import heapq

heuristics = [] # Represents the h(n) value for each node
                # relative to its goal
livenodes = [] # Priority queue containing the live nodes
               # to be expanded

# Represents individual node
# of a search tree for the pathfinding algorithm
class Node:

    def __init__(self, node, path, distance, parent=None):
        ''' Creates a Node object '''
        self.parent = parent
        self.node = node # Corresponding node in the MAP
        self.path = path # List containing visited nodes
        self.path.append(node)
        self.distance = distance # Represents g(n) --> distance from 
                                 # current node to the starting node
        self.cost = self.distance + heuristics[node] 
    
    # Operator overloading '<'
    def __lt__(self, value):
        return self.cost < value.cost


def get_X(node):
    ''' Returns the x position of a node'''
    return node[1][0]

def get_Y(node):
    '''Returns the y position of a node'''
    return node[1][1]

def calculate_euc_dist(node1, node2):
    ''' Returns the euclidean distance between two nodes '''
    return ((get_X(node1) - get_X(node2))**2 + (get_Y(node1) - get_Y(node2))**2)**0.5

def fill_heuristics(G, goal):
    ''' 
    Preprocessing before the A* algorithm, 
    fills out the list with the heuristic value
    for each node in the map G 
    '''
    nodes = list(G.nodes.data('pos'))
    goal_node = nodes[goal]
    for node in nodes:
        heuristics.append(calculate_euc_dist(node, goal_node))

def a_star(G, start, goal):
    ''' Initiating the A* algorithm '''
    
    ## Preprocessing ##
    
    awaken = 1 # Initiating variable

    # Clears heuristics and prio-queue
    livenodes.clear() 
    heuristics.clear()

    # Initiating heuristics and priority queue
    fill_heuristics(G, goal)
    heapq.heappush(livenodes, Node(start, [], 0))
    current_node = Node(start, [], 0) # Dummy element

    # Initialize loop
    while current_node.node != goal:

        # Picks out the live node
        # with the LEAST cost to expand
        current_node = heapq.heappop(livenodes)
        current_distance = current_node.distance

        # List out every edges incident
        # to the current node
        incidences = G.edges(current_node.node)

        for incidence in incidences:
            next_node = incidence[1]

            # Ensures that every node appended to the path
            # has not been explored
            if next_node not in current_node.path:
                distance = G.get_edge_data(incidence[0], incidence[1])['weight']
                to_add = Node(next_node, list.copy(current_node.path), current_distance + distance, parent=current_node)
                heapq.heappush(livenodes, to_add)
                awaken += 1


    print(current_node.path)
    print("Nodes:", awaken)
    return current_node.distance