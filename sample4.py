from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
arr1= np.array(
    [[1,0], [0,1]]
)

arr2= np.array(
    [[1,0], [0,1]]
)

x= euclidean_distances(arr1, arr2).argmin()
print(x)