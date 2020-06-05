from mip import Model, xsum, minimize, BINARY
import graph as gr

# Initiating Graph
gr.readNodes("rnodes.txt")
gr.readEdges("redges.txt")

# Initiating list of Nodes and Edges
mapped_nodes = { i : j for i,j in enumerate(gr.G.nodes()) }
nodes = [i for i in mapped_nodes.keys()]
n = len(nodes)
print(n)
edges = [weight for b, e, weight in gr.G.edges().data('weight')]
distance = gr.loadMatrix("mat.txt")
for arr in distance:
    print(arr)

# Initiating model
m_tsp = Model()
V = set(range(n))
print(V)
m = int(input("Number of salesman: "))
p = int(input("Max nodes: "))

# Adding variables x and u
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

for j in range(1, n):
    m_tsp += xsum(x[i][j] for i in range(n)) == 1

for i in range(1, n):
    m_tsp += xsum(x[i][j] for j in range(n)) == 1

# Subtour elimination
for i in range(1, n):
    for j in range(1, n):
        if i != j:
            m_tsp += u[i] - u[j] + (n-m) * x[i][j] <= (n-m) - 1

# Optimize!!
m_tsp.optimize(max_seconds=60)

if m_tsp.num_solutions:
    print("route with total distance {} found".format(m_tsp.objective_value))
    nc = 0
    
    for i in range(n):
        for j in range(n):
            print(x[i][j].x,end=" ")
        print("\n")
    
    # for i in range(n):
    #     print(y[i].x)
    
    while True:
        nc = [i for i in range(n) if x[nc][i].x >= 0.99][0]
        # print(nc)
        print(mapped_nodes[nc])
        if nc == 0:
            break
    print("\n")

else:
    print("fails")
