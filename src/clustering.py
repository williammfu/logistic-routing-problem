'''
Clustering module to implement
k-means algorithm
'''
import random, networkx, sys
MAX_ITER = 15
OUTPUT_PATH = "../out/CL"

def init_centroids(nodes, num_of_cluster):
    """
    Assign random nodes
    as centroids
    """
    i = 0
    chosen = []  # List to ensure that the same node
                 # is not chosen as the centroid
    centroids = [] # List of (x,y) coordinates which acts as
                   # the centroid for n clusters

    while i < num_of_cluster:
        j = random.randint(0, len(nodes)-1)
        if j not in chosen:
            centroids.append(nodes[j][1])
            i += 1

    return centroids

def calc_euc_dist(p1, p2):
    ''' Calculates the Euclidean distance between the two nodes '''
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def cluster(places, start, num_of_cluster):
    """
    Clusters a bunch of nodes
    to certain number of clusters
    """
    
    # Initiating local variables
    nodes = list(places.nodes().data('pos'))
    idx = [index for index,tup in enumerate(nodes) if tup[0] == start][0]
    starting_node = nodes.pop(idx)
    centroids = init_centroids(nodes, num_of_cluster)
    clusters = [[] for i in range(num_of_cluster)]

    # Clustering
    i = 0
    changed = False
    while i < MAX_ITER and not changed:
        
        before = centroids.copy()

        for node in nodes:
            temp = [calc_euc_dist(node[1], centroids[i]) for i in range(num_of_cluster)]
            index = temp.index(min(temp))
            for cluster in clusters:
                if node in cluster:
                    cluster.pop(cluster.index(node))
            clusters[index].append(node)
        
        for i in range(len(clusters)):
            if len(clusters[i]) == 0:
                continue
            avg_x = sum( pos[0] for node, pos in clusters[i] ) / len(clusters[i])
            avg_y = sum( pos[1] for node, pos in clusters[i] ) / len(clusters[i])
            centroids[i] = (avg_x, avg_y)

        changed = (before == centroids)
        i += 1
    
    for i in range(len(clusters)):
        clusters[i].insert(0, starting_node)

    return clusters

def cluster_to_matrix(places, start, clusters):
    ''' Converts clusters into adjacency matrix '''
    
    # List of edges' weight --> for adjacency matrix
    edges = places.edges().data('weight')

    for i in range(len(clusters)):

        mapped = { tup[0] : j for j, tup in enumerate(clusters[i]) }
        print(mapped)

        with open(OUTPUT_PATH + "nodes" + str(i) + ".txt", "w") as f:
            for m,n in enumerate(mapped):
                f.write(str(m) + " " + str(n) + "\n")
        
        # Initializing matrix
        n = len(clusters[i])
        m = [[sys.maxsize for i in range(n)] for j in range(n)]
        for x,y,z in edges:
            # Symmetric matrix (i.e. M(i,j) == M(j,i))
            if x in mapped.keys() and y in mapped.keys():
                m[mapped[x]][mapped[y]] = z
                m[mapped[y]][mapped[x]] = z

        with open(OUTPUT_PATH + "mat" + str(i) + ".txt", "w") as f:
            for entry in m:
                for k in entry:
                    f.write(str(k) + " ")
                f.write("\n")

          
