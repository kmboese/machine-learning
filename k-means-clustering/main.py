#Solves the problem set from the ECS 170 take-home final, problem 1
from k_means import *
from os import getcwd
from os.path import join, exists
import random
import copy


#I/O Variables
file_dir = getcwd()
filepath = join(file_dir, "k_means_solutions.txt")
divider = "_________________________________________________________\n"

#K-Means variables
k = 2 #number of clusters
cluster_count = 1 #counter for solution formatting
dataset = {"A": (5,36), "B": (73,78), "C": (34,61), "D": (86,33), "E": (67,24), "F": (20,16), \
            "G": (73,14), "H": (5,88), "I": (27,93), "J": (30,21), "K": (51,41), "L": (3,59)}
#Choose B=(73,78) and C=(34,61) as our initial centroids
centroids = {1: dataset["B"], 2: dataset["C"]}
clusters = defaultdict(list)
new_clusters = defaultdict(list)

def main():
    global centroids #Centroids from the previous clustering
    global new_clusters #centroids from the new clustering
    global cluster_count
    #Initial conditions
    print("Initial conditions:")
    print(dataset)
    clusters = cluster(k, centroids, dataset)
    print("Initial centroids: {}".format(centroids))
    printClusterInfo(clusters, new_clusters, centroids)
    writeSolution(filepath, clusters, new_clusters, centroids, init=True)

    #Clustering Phase
    while True:
        print("\nK-Means clustering:")
        #Generate new centroids
        centroids = genCentroids(clusters)
        print("Centroids: {}".format(centroids))
        #Cluster based off of the new centroids
        new_clusters = cluster(k, centroids, dataset)
        #print("Previous Clusters: {}".format(clusters))
        #print("New Clusters: {}".format(new_clusters))
        printClusterInfo(clusters, new_clusters, centroids)
        writeSolution(filepath, clusters, new_clusters, centroids)
        
        #Determine if clustering should continue
        if (new_clusters.values() == clusters.values()):
            print("Clusters did not change. Finishing k-means...")
            return
        else:
            #over-write the old clusters
            clusters = copy.deepcopy(new_clusters)
            new_clusters.clear()
            
#Write cluster information in latex format
def writeSolution(filepath, clusters, new_clusters, centroids, init=False):
    points = []
    #If the first run, create the file and flip the cluster order (Flips N/A and initial cluster)
    if init:
        mode = 'wb+'
        #tmp = copy.deepcopy(new_clusters)
        #new_clusters = copy.deepcopy(clusters)
        #clusters = copy.deepcopy(tmp)
    else:
        mode = 'ab+'
    with open(filepath, mode) as file:
        #Save all point in the same dictionary
        for key in sorted(clusters.keys()):
            points.extend(clusters[key])
        #Sort points
        points = sorted(points)

        #Write centroid info
        writeCentroidInfo(file, centroids)
        #Write cluster header info
        writeClusterHeader(file)

        #Write cluster info
        for point in points:
            dist_from_centroids = distFromCentroids(point[1], centroids, 2)
            centroid_labels = centroids.keys()
            if init:
                label1 = getClusterLabel(point, new_clusters)
                label2 = getClusterLabel(point, clusters)
            else:
                label1 = getClusterLabel(point, clusters)
                label2 = getClusterLabel(point, new_clusters)
            file.write("{} & {} & {} & {} & {} & {} & {} \\\\ \\hline"\
                    .format(point[0], point[1][0], point[1][1], \
                            dist_from_centroids[centroid_labels[0]], \
                            dist_from_centroids[centroid_labels[1]], label1, label2
                    )
            )
            file.write("\n")
        #Write end-formatting for clusters 
        file.write(r"\end{tabular}" + "\n")
        file.write(r"\end{table}" + "\n")
        file.write(r"%End Cluster Info" + "\n")
        file.write("\n")


#Writes centroid info in latex format
def writeCentroidInfo(file, centroids):
    labels = sorted(centroids.keys())
    file.write(r"\clearpage" + "\n")
    file.write(r"%Begin Centroid Points" + "\n")
    file.write(r"\clearpage" + "\n")
    file.write(r"\begin{table}[h!]" + "\n")
    file.write(r"\centering" + "\n")
    file.write(r"\caption{Centroids}" + "\n")
    file.write(r"\begin{tabular}{|c|r|r|}" + "\n")
    file.write(r"\hline" + "\n")
    file.write(r"\begin{tabular}[c]{@{}l@{}}Centroid\\Number\end{tabular} & x  & y   \\ \hline" + \
        "\n")
    file.write("{}\t & {} & {}\t \\\\ \\hline\n".format(labels[0], centroids[labels[0]][0], \
                centroids[labels[0]][1])
    )
    file.write("{}\t & {} & {}\t \\\\ \\hline\n".format(labels[1], centroids[labels[1]][0], \
                centroids[labels[1]][1])
    )
    file.write(r"\end{tabular}" + "\n")
    file.write(r"\end{table}" + "\n")
    file.write(r"%End Centroid Points" + "\n")

#Writes the cluster header info in latex format
def writeClusterHeader(file):
    global cluster_count
    file.write("\n" + r"%Cluster Info" + "\n")
    file.write(r"\begin{table}[h!] " + "\n")
    file.write(r"\centering" + "\n")
    file.write(r"\caption{K-Means Clustering ")
    file.write("{}".format(cluster_count))
    file.write(r"}")
    cluster_count += 1
    file.write(r"\begin{tabular}{|c|c|c|c|c|c|c|c|}" + "\n")
    file.write(r"\hline" + "\n")
    file.write(r"\begin{tabular}[c]{@{}c@{}}Point \\ ID\end{tabular} &" + "\n")
    file.write(r"\multicolumn{1}{c|}{x} & " + "\n")
    file.write(r"\multicolumn{1}{c|}{y} & " + "\n")
    file.write(r"\multicolumn{1}{c|}{\begin{tabular}[c]{@{}c@{}}Dist. to \\ Centroid 1\end{tabular}} &" + "\n")
    file.write(r"\multicolumn{1}{c|}{\begin{tabular}[c]{@{}c@{}}Dist. to \\ Centroid 2\end{tabular}} &" + "\n")
    file.write(r"\multicolumn{1}{c|}{\begin{tabular}[c]{@{}c@{}}Old \\ Group\end{tabular}} & " + "\n")
    file.write(r"\multicolumn{1}{c|}{\begin{tabular}[c]{@{}c@{}}New\\ Group\end{tabular}} \\ \hline" + "\n")
    

#prints info about each cluster
def printClusterInfo(clusters, new_clusters, centroids):
    for key in sorted(clusters.keys()):
        print("Cluster: {}".format(key))
        for point in sorted(clusters[key]):
            dist_from_centroids = distFromCentroids(point[1], centroids, 2)
            print("Point: {} = {}\tC_dists: {}\tOld Group: {}\tNew Group: {}"\
                .format(point[0], point[1], dist_from_centroids, getClusterLabel(point, clusters),\
                    getClusterLabel(point, new_clusters)))




if (__name__ == "__main__"):
    main()