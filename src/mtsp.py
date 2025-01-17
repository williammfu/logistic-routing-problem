"""
Multiple Travelling Salesman Problem (m-TSP) module
to generate a solution for the m-TSP problem

Based on the proposed MIP solution of TSP
by Dantzig, et.al 
"""
from mip import Model, xsum, minimize, BINARY, OptimizationStatus
from src import graph as gr

def load_graph(node_file, mat_file):
    ''' Loads graph representation with adj matrix '''
    parsed = []
    with open(node_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            parsed.append(line.strip().split(" "))

    matrix = gr.load_matrix(mat_file)

    return { int(i) : int(j) for i,j in parsed }, matrix

def generate_tours(num_of_salesman, matrix, mapped_nodes):
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
                tour.append(mapped_nodes[0])
                break
            p = q
            q = [j for j,k in enumerate(matrix[p]) if matrix[p][j] > 0.0][0]
            
        i += 1
        tours.append(tour)

    return tours

def mip_solve(mapped_nodes, load_matrix, m, p):
    '''
    Creates a optimization model
    from the given graph G
    '''
    # Number of nodes in map G
    n = len(mapped_nodes.keys())

    # Matrix of distances
    distance = load_matrix

    # Initiating model
    m_tsp = Model()

    # Adding variables x and u
    # x represents the edges chosen in the tour
    # x(i,j) == 1 when the edge c(i,j) is included in the tour, otherwise 0
    x = [[ m_tsp.add_var(var_type=BINARY) for i in range(n) ] for j in range(n) ]

    # u is a continuous variable represents the constraint for the 
    # given tour (no subtours are allowed!!)
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
    # Based on the constraint formulated by Miller, et al. (1960)
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                m_tsp += u[i] - u[j] +  p * x[i][j] <= p - 1

    # Optimzing. . .
    st = m_tsp.optimize(max_seconds=30)

    # Assumed solution is always generated
    # There is a chance that the solution generated is not confirmed
    # to be globally optimum

    if m_tsp.num_solutions:

        if st == OptimizationStatus.FEASIBLE:
            print("Feasible", end=" ")
        elif st == OptimizationStatus.OPTIMAL:
            print("Optimum", end=" ")

        print("tour(s) with total distance {} found".format(m_tsp.objective_value))
        nc = 0
        
        result = []
        for i in range(n):
            row = [a.x for a in x[i]]
            result.append(row)
        
        tours = generate_tours(m, result, mapped_nodes)
        return tours

    else:
        print("Failed. Tour(s) not found.")
