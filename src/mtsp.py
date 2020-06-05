"""
Multiple Travelling Salesman Problem (m-TSP) module
to generate a solution for the m-TSP problem

Based on the proposed MIP solution of TSP
by Dantzig, et.al 
"""
from mip import Model, xsum, minimize, BINARY, OptimizationStatus
import graph as gr

# Initiating Graph
G = gr.read_graph("../data/snodes.txt", "../data/sedges.txt")

# Initiating list of Nodes and Edges
mapped_nodes = { i : j for i,j in enumerate(gr.G.nodes()) }
n = len(mapped_nodes.keys()) # Number of nodes in map G
edges = [weight for b, e, weight in gr.G.edges().data('weight')]

def generate_tours(num_of_salesman, matrix):
    '''
    Returns a list of tour from the solution
    matrix after optimization
    '''
    
    # Initiating variables
    tours = []
    a = [i for i,j in enumerate(matrix[0]) if matrix[0][i] > 0.0]
    i = 0
    
    # Initializing loop
    # The amount of tour equals the number of salesman assigned
    while i < num_of_salesman:
            
        p = 0
        q = a[i]
        tour = []

        while True:
            
            tour.append(mapped_nodes[p])
            if q == 0: # Back to node 0 = tour created!!
                tour.append(0)
                break
            p = q
            q = [j for j,k in enumerate(matrix[p]) if matrix[p][j] > 0.0][0]
            
        i += 1
        tours.append(tour)

    return tours

def mip_solve(G):
    '''
    Creates a optimization model
    from the given graph G
    '''

    # Matrix of distances
    distance = gr.loadMatrix("../out/small.txt")

    # Initiating model
    m_tsp = Model()
    m = int(input("Number of salesman: "))
    p = int(input("Max nodes: "))

    # Adding variables x and u
    # x represents the edges chosen in the tour
    # x(i,j) == 1 when the edge c(i,j) is included in the tour, otherwise 0
    # u is a continuous variable represents the constraint for the 
    # given tour (no subtours are allowed!!)
    x = [[ m_tsp.add_var(var_type=BINARY) for i in range(n) ] for j in range(n) ]
    u = [ m_tsp.add_var() for i in range(n) ]

    # Adding objective
    m_tsp.objective = minimize(
                        xsum( distance[i][j] * x[i][j]  for i in range(n) for j in range(n))
                    )

    # Adding constraints
    # Ensures that exactly m salesman departs
    # from the first node
    m_tsp += xsum(x[0][j] for j in range(1,n)) == m
    m_tsp += xsum(x[j][0] for j in range(1,n)) == m

    # Ensures that each node only travelled by one salesman ONLY
    # Note: For nodes other than the starting node
    for j in range(1, n):
        m_tsp += xsum(x[i][j] for i in range(n)) == 1

    for i in range(1, n):
        m_tsp += xsum(x[i][j] for j in range(n)) == 1

    # Subtour elimination
    # Based on the constraint formulated by Gavish, 1976
    # as the correction for the constraint
    # suggested by Svestka & Huckfeldt, 1973
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                m_tsp += u[i] - u[j] + (n-m) * x[i][j] <= (n-m) - 1

    st = m_tsp.optimize(max_seconds=30)
    if m_tsp.num_solutions:

        if st == OptimizationStatus.FEASIBLE:
            print("Feasible sol only")
        elif st == OptimizationStatus.OPTIMAL:
            print("Optimum!")

        print("route with total distance {} found".format(m_tsp.objective_value))
        nc = 0
        
        met = []
        for i in range(n):
            row = [a.x for a in x[i]]
            for j in range(n):
                print(x[i][j].x,end=" ")
            met.append(row)
            print("\n")
        
        tours = generate_tours(m, met)

    else:
        print("fails")
