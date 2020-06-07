from sys import maxsize
import heapq
import time

INF = maxsize
livenodes = [] # Priority queue to hold live nodes

MAT = [
    [INF, 14, 17, 2, 8],
    [12, INF, 19, 2, 7],
    [10, 3, INF, 4, 2],
    [5, 3, 12, INF, 9],
    [11, 7, 7, 12, INF]
]

mapped = {0:1,1:2,2:3,3:4,4:5}
class Node:

    def __init__(self, cost, mat, path, node):
        self.cost = cost
        self.mat = mat
        self.path = path
        self.node = node
        self.path.append(node)
    
    # Operator overloading '<'
    def __lt__(self, value):
        return self.cost < value.cost

def set_to_inf(input_matrix, i, j):
    
    mat = [row[:] for row in input_matrix]
    n = len(input_matrix)
    row = [INF for i in range(n)]
    mat[i] = row
    for k in range(n):
        mat[k][j] = INF
    mat[j][0] = INF
    return mat
    

def reduce_matrix(input_matrix):

    matrix = [row[:] for row in input_matrix]

    # Reduce column
    total_cost = 0
    for i in range(len(matrix)):
        if 0 not in matrix[i] and not all( k == INF for k in matrix[i] ):
            cost = min(matrix[i])
            temp = [ INF if matrix[i][j] == INF 
                    else matrix[i][j]-cost 
                    for j in range(len(matrix[i])) ]
            matrix[i] = temp
            total_cost += cost
    
    # Reduce row
    for i in range(len(matrix)):
        row = [ col[i] for col in matrix ]
        if 0 not in row and not all( k == INF for k in row ):
            cost = min(row)
            row = [ INF if row[j] == INF 
                    else row[j] - cost for j in range(len(row)) ]
            for j in range(len(row)):
                matrix[j][i] = row[j]
            total_cost += cost
    
    return matrix, total_cost

def search(mapped_nodes, matrix):

    # Root node
    reduced, cost = reduce_matrix(matrix)
    tour = set(range(len(matrix)))
    exp = Node(cost, reduced, [], 0)

    start = time.time()
    while set(exp.path) != tour:

        unvisited = tour - set(exp.path)

        for i in unvisited:
            edge = exp.mat[exp.node][i]
            temp_mat = set_to_inf(exp.mat, exp.node, i)
            reduced, cost = reduce_matrix(temp_mat)
            heapq.heappush(livenodes, Node(exp.cost+cost+edge, reduced, list.copy(exp.path), i))

        exp = heapq.heappop(livenodes)

    print("Tur ditemukan dengan waktu: {:.3f} detik".format(time.time()-start))
    final_tour = exp.path[:]
    final_tour.append(0)

    return [ mapped_nodes[node] for node in final_tour ]
