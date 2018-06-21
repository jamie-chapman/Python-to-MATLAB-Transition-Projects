from scipy.spatial import distance
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random


'''
Date: 20/06/2018
Author: Jamie Chapman

K-means clustering 
- Should work with n-dimentional datasets
'''

def main():
    # Generate gaussian clouds
    mu, sigma = 1, 0.5 #mean and std dev

    size = 200;
    x1 = np.random.normal(mu, sigma, size)
    y1 = np.random.normal(mu, sigma, size)
    z1 = np.random.normal(mu, sigma, size)

    x2 = np.random.normal(mu+0.8, sigma, size)
    y2 = np.random.normal(mu+0.8, sigma, size)
    z2 = np.random.normal(mu+0.8, sigma, size)

    #Concat as single point cloud
    points = np.array([np.concatenate([x1, x2], axis=0), np.concatenate([y1, y2], axis=0), np.concatenate([z1, z2], axis=0), np.zeros(size * 2)])

    #Select number of means
    k = 6
    d = len(points)-1 #dimentionality
    means = np.zeros((k,d))

    #Start k-means
    #Pick initial means
    r = random.sample(range(len(points[0])),k) #added step to guarantee unique means
    for i in range(0,k):
        means[i] = points[0:d,r[i]]

    while True:
        #Cluster according to nearest mean
        for i in range(0,len(points[0])): #for each point
            min_dist = float('inf')
            for j in range(0, len(means)): #for each mean
                dist = distance.euclidean(points[0:d, i], means[j]) #distance from point to mean
                if dist < min_dist:
                    points[d,i] = j #assign class label
                    min_dist = dist #make this distance the new minimum
        #Recalculate new means
        old_means = means
        means = np.zeros((k, d))
        count = np.zeros(k) #list of counts for each class
        for i in range(0, len(points[0])): #for each point
            count[int(points[d,i])]+= 1
            means[int(points[d,i])] += points[0:d, i]
        #Set new means
        for i in range(0,k):
            means[i] = np.divide(means[i],count[i])

        #Check for changes in 'clusters'
        if distance.euclidean(np.sum(old_means), np.sum(means)) == 0:
            break

    #Plot 3D output
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    colors = ['r', 'g', 'b', 'y', 'c', 'm']
    for i in range(0, len(points[0])):
        ax.scatter(points[0, i], points[1, i],  points[2, i] , c = colors[int(points[3,i])], marker='.')
    plt.show()

if __name__ == "__main__":
    main()
