import networkx as nx
import pathfinding as pth
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

def draw_map(G):
    """
    Displays the map
    """

    # Adding axis to graph (optional)
    fig, ax = plt.subplots()
    limits = plt.axis('on')
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.xlabel("Latitude")
    plt.ylabel("Longitude")

    # Display nodes per positions
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw_networkx(G, pos, node_size=1, with_labels=False, ax=ax)

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

    node_pos = G.nodes().data('pos')
    for post in posts:
        subgraph.add_node(post, pos=node_pos[post])

    size = len(posts)
    start = time.time()
    for i in range(size):
        for j in range(i+1, size):
            subgraph.add_edge(posts[i], posts[j], weight=pth.a_star(G, posts[i], posts[j]))
    print("Elapsed time: {} seconds".format(time.time() - start))

    with open("../data/snodes.txt", "w") as f:
        nodes = subgraph.nodes().data('pos')
        for node in nodes:
            f.write(str(node[0]) + " " + str(node[1][0]) + " " + str(node[1][1]) + "\n")

    with open("../data/sedges.txt", "w") as f:
        edges = list(subgraph.edges().data('weight'))
        for i in range(len(edges)):
            f.write(
                str(i) + " " + str(edges[i]).replace(",","").replace("(","").replace(")","") + "\n"   
            )
    
    return starting_node, subgraph

def draw_subgraph(subgraph):
    """
    Displays the subgraph
    """
    # Adding axis to graph (optional)
    fig, ax = plt.subplots()
    plt.axis('on')
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.xlabel("Latitude")
    plt.ylabel("Longitude")

    # Displays graph in a circular model
    pos = nx.circular_layout(subgraph)
    nx.draw_networkx(subgraph, pos=pos, with_labels=True, ax=ax)

    # Displays graph
    plt.show()

def create_subgraph_matrix(subgraph, filename="mat.txt"):
    """
    Converts a subgraph
    as a distance matrix
    """

    nodes = subgraph.nodes()
    edges = subgraph.edges().data('weight')
    index = { name : index for index, name in enumerate(nodes) }
    
    # Filling the distance matrix
    m = [[0 for i in range(len(nodes))] for j in range(len(nodes))]
    for i,j,k in edges:
        # Symmetric matrix (i.e. M(i,j) == M(j,i))
        m[index[i]][index[j]] = k
        m[index[j]][index[i]] = k

    with open("../out/" + filename, "w") as f:
        for entry in m:
            for i in entry:
                f.write(str(i) + " ")
            f.write("\n")

def loadMatrix(filename):
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
    
    for arr in m:
        for index, item in enumerate(arr):
            if item == 0.0:
                arr[index] = sys.maxsize 

    return m


if __name__ == "__main__":

    # Oldenburg data
    OL_MAP = read_graph()
    
    # San Francisco data
    # read_graph(SF_NODE, SF_EDGE)

    s = time.time()
    start, subgraph = create_subgraph(OL_MAP)
    create_subgraph_matrix(subgraph, filename="small.txt")
    print(time.time() - s)

    draw_map(OL_MAP)
    draw_subgraph(subgraph)



