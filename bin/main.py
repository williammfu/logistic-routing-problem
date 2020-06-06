"""
Main program to simulate
logistic routing problem
"""
import sys
import networkx as nx
sys.path.append('../')
from src import graph, mtsp, clustering

OUTPUT = "../out/"
def input_logistics():
    ''' Masukan m '''
    while True:
        m = int(input("Masukan banyaknya kendaraan logistik: "))
        if m > 0:
            return m

def choose_method():
    ''' Pilihan metode penyelesaian mTSP '''
    print("Pilih method penyelesaian m-TSP: ")
    print("[1] Dengan Clustering")
    print("[2] Tanpa Clustering")

    while True:
        m = int(input("Pilihan anda: "))
        if m == 1 or m == 2:
            return m

MAP = graph.read_graph()
START, PLACES = graph.create_subgraph(MAP)

log = input_logistics()
opt = choose_method()

if opt == 1:

    CL = clustering.cluster(PLACES, START, log)
    clustering.cluster_to_matrix(PLACES, START, CL)

    n = len(CL)
    tours = []
    for i in range(n):
        MAPPED, MATR = mtsp.load_graph( OUTPUT + "CLnodes" + str(i) + ".txt", 
                                        OUTPUT + "CLmat" + str(i) + ".txt" )
        tour = mtsp.mip_solve(MAPPED, MATR, 1, len(MATR))
        tours.append(tour)
    
    print(tours)

else:

    graph.create_subgraph_matrix(START, PLACES)
    MAPPED, MATR = mtsp.load_graph( OUTPUT + "OLnodes.txt",
                                    OUTPUT + "OLmat.txt" )
    tours = mtsp.mip_solve(MAPPED, MATR, log, (len(MATR)//log) - 1)
    print(tours) 
