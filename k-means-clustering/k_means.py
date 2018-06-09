#Program that performs k-means clustering on a set of tuples
from math import sqrt
from collections import defaultdict
import random

centroid_count = 3

#Returns the distance between two 2-value tuples
def distance(p1, p2):
    return(sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2))

#Randomly chooses k points from a dictionary dataset to initialize a k-means clustering operation
def initCentroids(k, dataset):
    centroids = {} #list of centroids to return
    points = [] #list of data points
    #Read all the keys into the points list
    points = dataset.keys()
    #Choose k random points
    for i in range(k):
        tmp = points[random.randint(0,len(points)-1)]
        #don't select duplicate points
        if tmp not in centroids:
            centroids[tmp] = dataset[tmp]
    return centroids

#Choose new centroids based off of the mean of the points within the existing clusters
def genCentroids(clusters):
    global centroid_count
    new_centroids = {}
    for key in clusters.keys():
        x_sum = 0
        y_sum = 0
        for point in clusters[key]:
            x_sum += point[1][0]
            y_sum += point[1][1]
        x_centroid = x_sum / len(clusters[key])
        y_centroid = y_sum / len(clusters[key])
        new_centroids[centroid_count] = x_centroid, y_centroid
        centroid_count += 1
    return new_centroids 

#Assign a point to a cluster
#Returns: the label of the centroid to which the given point should cluster
def groupPoint(p, centroids):
    dist = float('inf')
    centroid_label = ""
    '''
    #don't group centroids with themselves
    if (p in centroids.values()):
        return
    '''
    for key in centroids.keys():
        if (distance(p, centroids[key]) < dist):
            dist = distance(p, centroids[key])
            centroid_label = key
    return centroid_label, centroids[centroid_label]


#Cluster points around the k clusters based off the distance from the point to each centroid value
#Returns: A list of k clusters of datapoints
def cluster(k, centroids, dataset):
    clusters = defaultdict(list) #a list of point clusters
    #print("\tDEBUG: number of centroids == {}".format(len(centroids)))
    assert len(centroids) == k
    for key in dataset.keys():
        point = dataset[key]
        centroid_group = groupPoint(point, centroids)
        if centroid_group is not None:
            #Add the point to a cluster based on the centroid label
            P = (key, point)
            clusters[centroid_group[0]].append(P)
    return clusters

#Returns the distance of a point from all centroids to a specified amount of decimal points
def distFromCentroids(point, centroids, decimals):
    distances = {}
    for centroid_label in centroids.keys():
        distances[centroid_label] = round(distance(point, centroids[centroid_label]), decimals)
    return distances

#Returns the cluster label for a point
def getClusterLabel(p, clusters):
    for label in clusters.keys():
        for point in clusters[label]:
            if p[0] == point[0]:
                return ("C" + str(label))
    return ("N/A")

