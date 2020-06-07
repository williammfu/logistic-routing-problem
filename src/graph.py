import networkx as nx
from src import pathfinding as pth
import matplotlib.pyplot as plt
import time, sys

# Oldenburg
OL_NODE = "../data/OL.cnode.txt"
OL_EDGE = "../data/OL.cedge.txt"

# San Francisco
SF_NODE = "../data/SF.cnode.txt"
SF_EDGE = "../data/SF.cedge.txt"

def read_graph(node_file=OL_NODE, edge_file=OL_EDGE):
    """
    Initiates a graph from
    the given datasets
    """
    # Initiallize array
    G = nx.Graph()

    # Reads the nodes dataset
    parsed = []
    with open(node_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            parsed.append(line.strip().split(" "))
    
    for parse in parsed:
        G.add_node(int(parse[0]), pos=(float(parse[1]), float(parse[2])))

    # Reads the edges dataset
    parsed = []
    with open(edge_file, "r") as f:
        
        for line in f:
            parsed.append(line.strip().split(" "))
    
    for parse in parsed:
        G.add_edge(int(parse[1]), int(parse[2]), weight=float(parse[3]))

    return G

def draw_map(G, subgraph, edgeslist, nodeslist, lb, zoom=True, save=False):
    """
    Displays the map
    """
    # Colors
    COLOR = ['lightskyblue','darkseagreen','r','c','m','k','pink','orange']


    # Display nodes per positions
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, node_color="lightgray", edge_color="lightgray", with_labels=False, node_size=6)
    nx.draw_networkx_labels(G, pos, labels=lb, font_size=6, font_family='monospace')
    for i in range(len(nodeslist)):
        nx.draw_networkx_nodes(G, pos, nodelist=nodeslist[i][:1], node_color='yellow', edgescolor='gold', node_size=70, with_labels=True)
        nx.draw_networkx_nodes(G, pos, nodelist=nodeslist[i][1:len(nodeslist[i])-1], node_color=COLOR[i%8], node_size=70, with_labels=True)
        nx.draw_networkx_edges(G, pos=pos, edge_color=COLOR[i%8], edgelist=edgeslist[i])

    if zoom:
        x_data = [ x[1][0] for x in subgraph.nodes().data('pos') ]
        y_data = [ x[1][1] for x in subgraph.nodes().data('pos') ]
        min_X = min(x_data)
        max_x = max(x_data)
        min_y = min(y_data)
        max_y = max(y_data)
        plt.xlim(min_X - 25, max_x + 25)
        plt.ylim(min_y - 25, max_y + 25)

    if save:
        fname = input("Masukan nama file: ")
        plt.savefig('../out/img/'+ fname + '.png')
    else:
        plt.show()

def create_subgraph(G):
    """
    Generates a subgraph with the given nodes
    from the map G
    """
    # Generate a new graph
    subgraph = nx.Graph()
    
    # Read wanted nodes
    posts = []
    with open("../data/post.txt","r") as f:
        for line in f:
            posts.append(int(line))

    starting_node = posts[0] # First line denotes the starting point
    posts.sort()

    # Adding nodes
    node_pos = G.nodes().data('pos')
    for post in posts:
        subgraph.add_node(post, pos=node_pos[post])

    size = len(posts)

    # Building a complete graph
    print("Memulai pathfinding. . .")
    start = time.time()
    for i in range(size):
        for j in range(i+1, size):
            subgraph.add_edge(posts[i], posts[j], weight=pth.a_star(G, posts[i], posts[j]))
    print("Waktu pathfinding: {:.3f} detik".format(time.time() - start))

    # Writes subgraph to a txt file
    with open("../out/SUBnodes.txt", "w") as f:
        nodes = subgraph.nodes().data('pos')
        for node in nodes:
            f.write(str(node[0]) + " " + str(node[1][0]) + " " + str(node[1][1]) + "\n")

    with open("../out/SUBedges.txt", "w") as f:
        edges = list(subgraph.edges().data('weight'))
        for i in range(len(edges)):
            f.write(
                str(i) + " " + str(edges[i]).replace(",","").replace("(","").replace(")","") + "\n"   
            )
    
    return starting_node, subgraph

def draw_subgraph(subgraph, edgeslist):
    """
    Displays the subgraph
    """
    # Displays graph in a circular model
    pos = nx.get_node_attributes(subgraph, 'pos')
    nx.draw_networkx_nodes(subgraph, pos=pos, with_labels=True, node_size=10)
    nx.draw_networkx_edges(subgraph, pos=pos, edge_color='r', edgelist=edgeslist)

    # Displays graph
    plt.show()

def create_subgraph_matrix(start, subgraph, filename="OL"):
    """
    Converts a subgraph
    as a distance matrix
    """

    nodes = list(subgraph.nodes())
    st = nodes.index(start)
    if st != 0: # Starting node is always index 0
        nodes[0], nodes[st] = nodes[st], nodes[0] # Swap

    edges = subgraph.edges().data('weight')
    index = { name : index for index, name in enumerate(nodes) }
    
    # Filling the distance matrix
    m = [[sys.maxsize for i in range(len(nodes))] for j in range(len(nodes))]
    for i,j,k in edges:
        # Symmetric matrix (i.e. M(i,j) == M(j,i))
        m[index[i]][index[j]] = k
        m[index[j]][index[i]] = k

    with open("../out/" + filename + "nodes.txt", "w") as f:
        for key, entry in enumerate(index):
            f.write(str(key) + " " + str(entry) + "\n")
        
    with open("../out/" + filename + "mat.txt", "w") as f:
        for entry in m:
            for i in entry:
                f.write(str(i) + " ")
            f.write("\n")

def load_matrix(filename):
    """
    Loads matrix from a given filename
    """
    m = []
    with open(filename, "r") as f:
        lines = [x.strip() for x in f.readlines()]
        for line in lines:
            m.append(
                list(map(float, line.split()))
            )

    return m

def generate_tours_data(tours):
    '''
    Generate data for the
    tours visualization
    '''
    edgeslist = []
    nodeslist = []
    labels = {}

    for tour in tours:
        temp_edge = []
        temp_node = []

        temp_node.append(tour[0])
        labels[tour[0]] = str(tour[0])
        for i in range(len(tour)-1):
            edge = tour[i], tour[i+1]
            temp_edge.append(edge)
            labels[tour[i+1]] = str(tour[i+1])
            temp_node.append(tour[i+1])
        
        edgeslist.append(temp_edge)
        nodeslist.append(temp_node)
    
    return edgeslist, nodeslist, labels

def print_tours(subgraph, tours):
    ''' Displays tours '''

    print("\n=== TOUR ===========")
    for tour in tours:

        tour_weight = 0
        print("{}".format(tour[0]),end="")
        
        for i in range(1,len(tour)):
            print("-> {}".format(tour[i]),end=" ")
            tour_weight += subgraph.edges[tour[i-1], tour[i]]['weight']
        
        print("\nBobot tur = {}".format(tour_weight))

if __name__ == "__main__":

    # Oldenburg data
    OL_MAP = read_graph()
    
    # San Francisco data
    # SF_MAP = read_graph(SF_NODE, SF_EDGE)

    start, subgraph = create_subgraph(OL_MAP)
    create_subgraph_matrix(start, subgraph)

    # print(OL_MAP.edges[0,1])
    # draw_map(OL_MAP)
    # draw_subgraph(subgraph)



