"""
Main program to simulate
logistic routing problem
"""
import sys
import networkx as nx
sys.path.append('../')
from src import graph, mtsp, clustering, hungarian

OUTPUT = "../out/"

def input_logistics():
    ''' Masukan m '''
    while True:
        m = int(input("Masukan banyaknya kendaraan logistik: "))
        if m > 0:
            return m

def choose_method():
    ''' Pilihan metode penyelesaian mTSP '''
    print("Aproksimasi penyelesaian m-TSP: ")
    print("[1] Reduced Cost Matrix")
    print("[2] Pemodelan MIP")

    while True:
        m = int(input("Pilihan anda: "))
        if m == 1 or m == 2:
            return m

MAP = None
SAVE_GRAPH = False # if true, graph will be saved in ../out/img

if len(sys.argv) == 1:
    MAP = graph.read_graph(graph.OL_NODE, graph.OL_EDGE)
elif len(sys.argv) == 2:
    if sys.argv[1].lower() == 'ol':
        MAP = graph.read_graph(graph.OL_NODE, graph.OL_EDGE)
    elif sys.argv[1].lower() == 'sf':
        MAP = graph.read_graph(graph.SF_NODE, graph.SF_EDGE)
    else:
        print("Invalid filename")
        sys.exit()
else:
    print("Invalid arguments")
    sys.exit()

START, PLACES = graph.create_subgraph(MAP)

# Input menu
log = input_logistics()
opt = choose_method()
tours = [] # Results go here !

if opt == 1: # With Clustering

    CL = clustering.cluster(PLACES, START, log)
    clustering.cluster_to_matrix(PLACES, START, CL)

    n = len(CL)

    # Solving each tours
    for i in range(n):
        MAPPED, MATR = mtsp.load_graph( OUTPUT + "CLnodes" + str(i) + ".txt", 
                                        OUTPUT + "CLmat" + str(i) + ".txt" )
        tour = hungarian.search(MAPPED, MATR)
        tours.append(tour)

else: # Without clustering

    graph.create_subgraph_matrix(START, PLACES, filename=sys.argv[1].upper())
    MAPPED, MATR = mtsp.load_graph( OUTPUT + sys.argv[1].upper() + "nodes.txt",
                                    OUTPUT + sys.argv[1].upper() + "mat.txt" )
    
    # Max num of nodes = (len(MATR)//log) - 1
    tours = mtsp.mip_solve(MAPPED, MATR, log, (len(MATR)//log) - 1)


# Output
print("Simpan? (y/n)")
ans = input(">> ")

SAVE_GRAPH = ans.lower() == 'y'
graph.print_tours(PLACES, tours)
ed, nd, lb = graph.generate_tours_data(tours)

graph.draw_map(MAP, PLACES, ed, nd, lb, save=SAVE_GRAPH)

