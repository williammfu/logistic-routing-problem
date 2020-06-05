d = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]

a = [i for i,j in enumerate(d[0]) if d[0][i] > 1]
print(a)