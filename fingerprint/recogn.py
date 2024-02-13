import os
import cv2
import numpy as np
from sklearn.cluster import KMeans
import networkx as nx

# Load the image
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'fa2.BMP')
img = cv2.imread(image_path, 0)

# Create SIFT detector
sift = cv2.SIFT_create()

# Detect keypoints and compute descriptors
kp, desc = sift.detectAndCompute(img, None)

# Perform k-means clustering on descriptors
num_clusters = 5  # Adjust as needed
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(desc)

# Get cluster labels for keypoints
cluster_labels = kmeans.labels_

# Create a graph
graph = nx.Graph()

# Add nodes (keypoints) to the graph with their cluster labels as attributes
for i, label in enumerate(cluster_labels):
    graph.add_node(i, cluster=label)

# Add edges between keypoints in the same cluster
for i in range(len(kp)):
    for j in range(i + 1, len(kp)):
        if cluster_labels[i] == cluster_labels[j]:
            # Compute the distance between keypoints (e.g., Euclidean distance)
            distance = np.linalg.norm(np.array(kp[i].pt) - np.array(kp[j].pt))
            graph.add_edge(i, j, weight=distance)

# Compute the Minimum Spanning Tree (MST)
mst = nx.minimum_spanning_tree(graph)

# Calculate the total weight of edges in the MST
total_cost = sum(graph.edges[edge]["weight"] for edge in mst.edges())

print("Minimum cost of MST:", total_cost)
