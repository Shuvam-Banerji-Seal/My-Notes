# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 11:40:32 2024

@author: HP
"""

import numpy as np

def k_means_clustering(data, k, max_iterations=100):
    # Step 1: Initialize centroids randomly from the data points.
    centroids = data[np.random.choice(data.shape[0], k, replace=False)]
    print(centroids)
    for iteration in range(max_iterations):
        # Step 2: Assign points to the nearest centroid.
        distances = np.sqrt(((data - centroids[:, np.newaxis])**2).sum(axis=2))
        closest_centroids = np.argmin(distances, axis=0)
        
        new_centroids = np.array([data[closest_centroids==i].mean(axis=0) for i in range(k)])
        
        # Check for convergence (if centroids do not change).
        if np.all(centroids == new_centroids):
            break
        
        centroids = new_centroids
    
    return closest_centroids, centroids

# Example usage:

x = [4, 5, 10, 4, 3, 11, 14 , 6, 10, 12]
y = [21, 19, 24, 17, 16, 25, 24, 22, 21, 21]  

data1 = list(zip(x, y))
print(data1)  
    
data = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])

print(data.shape)
clusters, centroids = k_means_clustering(data, 2)
print("Cluster assignments:", clusters)
print("Centroids:", centroids)
