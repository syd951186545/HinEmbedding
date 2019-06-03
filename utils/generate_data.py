import csv
from random import random

import numpy as np
from scipy import io
from scipy.sparse import csr_matrix


# Generate new Edges and the graph at time T-1
def generate_network(network, num_of_nodes):
    # Network at time t
    network_t = [[0 for y in range(num_of_nodes)] for x in range(num_of_nodes)]

    # New edges(YES & NO) at time t+1
    new_edges = {x: {} for x in range(num_of_nodes)}

    threshhold = 0.8

    # YES links
    count = 0
    for i, row in enumerate(network):
        for j, value in enumerate(row):
            if value == 1:  # if yes edge
                # check if it has more than 1 edge
                neighbours = 0
                # check for i
                for u in network_t[i]:
                    if u == 1:
                        neighbours = neighbours + 1
                    if neighbours > 1:
                        break
                if neighbours <= 1:
                    # Add to the graph at time t
                    network_t[i][j] = 1
                    network_t[j][i] = 1
                    continue

                neighbours = 0
                # check for j
                for u in network_t[j]:
                    if u == 1:
                        neighbours = neighbours + 1
                    if neighbours > 1:
                        break
                if neighbours <= 1:
                    # Add to the graph at time t
                    network_t[i][j] = 1
                    network_t[j][i] = 1
                    continue

                # check for j
                if random() <= threshhold:
                    # Add to the graph at time t
                    network_t[i][j] = 1
                    network_t[j][i] = 1
                else:
                    # Add to the new YES edges
                    new_edges[i][j] = 1
                    new_edges[j][i] = 1
                    count += 1

    print('The number of positive edges in the testing dataset = {}'.format(count))

    # NO links
    while count > 0:
        for i, row in enumerate(network):
            for j, value in enumerate(row):
                # If the edge is not present in the original graph at time t+1
                # and has not been added to the new edges yet
                if value == 0 and (i not in new_edges or j not in new_edges[i]):
                    neighbours = False
                    # check for i
                    for u in network_t[i]:
                        if u == 1:
                            neighbours = True
                        if neighbours:
                            break
                    if not neighbours:
                        continue

                    neighbours = False
                    # check for j
                    for u in network_t[j]:
                        if u == 1:
                            neighbours = True
                        if neighbours:
                            break
                    if not neighbours:
                        continue

                    # Add to the new NO edges
                    if random() >= threshhold:
                        new_edges[i][j] = 0
                        new_edges[j][i] = 0
                        count -= 1
                if count <= 0:
                    break
            if count <= 0:
                break

    # Return the generated network of time T and the new edges(YES & NO)
    # which will be added to network at time T to generate the network at time T+1
    return network_t, new_edges


def load_data_blogcatalog():
    print("dataset blogcatalog")
    file = open("../data/blogCatalog/blogCatalog.edgelist", "r")
    n = 5196
    edges = 0
    network = [[0 for x in range(n)] for x in range(n)]
    while 1:
        l = file.readline()
        if l == '':
            break
        vec = l.split(" ")
        a = int(vec[0])
        b = int(vec[1])
        if a < n and b < n:  # taking all the edges with node values less than 10000
            network[a][b] = 1
            network[b][a] = 1
            edges += 1
    file.close()
    print('Total edges = {}'.format(edges))
    network, new_edges = generate_network(network, n)
    network = csr_matrix(network, dtype=int)
    io.savemat('../data/sample/blogCatalog.mat', {'adjacency_matrix': network})
    np.save('../data/sample/blogCatalog.npy', new_edges)


def load_data_citeseer():
    print("dataset citeseer")
    file = open("../data/citeseer/citeseer.edgelist", "r")
    n = 3312
    edges = 0
    network = [[0 for x in range(n)] for x in range(n)]
    while 1:
        l = file.readline()
        if l == '':
            break
        vec = l.split(" ")
        a = int(vec[0])
        b = int(vec[1])
        if a < n and b < n:  # taking all the edges with node values less than 10000
            network[a][b] = 1
            network[b][a] = 1
            edges += 1
    file.close()
    print('Total edges = {}'.format(edges))
    network, new_edges = generate_network(network, n)
    network = csr_matrix(network, dtype=int)
    io.savemat('../data/sample/citeseer.mat', {'adjacency_matrix': network})
    np.save('../data/sample/citeseer.npy', new_edges)


def load_data_flickr():
    print("dataset flickr")
    file = open("../data/flickr/flickr.edgelist", "r")
    n = 7575
    edges = 0
    network = [[0 for x in range(n)] for x in range(n)]
    while 1:
        l = file.readline()
        if l == '':
            break
        vec = l.split(" ")
        a = int(vec[0])
        b = int(vec[1])
        if a < n and b < n:  # taking all the edges with node values less than 10000
            network[a][b] = 1
            network[b][a] = 1
            edges += 1
    file.close()
    print('Total edges = {}'.format(edges))
    network, new_edges = generate_network(network, n)
    network = csr_matrix(network, dtype=int)
    io.savemat('../data/sample/flickr.mat', {'adjacency_matrix': network})
    np.save('../data/sample/flickr.npy', new_edges)

def load_data_pubmed():
        print("dataset pubmed")
        file = open("../data/pubmed/pubmed.edgelist", "r")
        n = 19717
        edges = 0
        network = [[0 for x in range(n)] for x in range(n)]
        while 1:
            l = file.readline()
            if l == '':
                break
            vec = l.split(" ")
            a = int(vec[0])
            b = int(vec[1])
            if a < n and b < n:  # taking all the edges with node values less than 10000
                network[a][b] = 1
                network[b][a] = 1
                edges += 1
        file.close()
        print('Total edges = {}'.format(edges))
        network, new_edges = generate_network(network, n)
        network = csr_matrix(network, dtype=int)
        io.savemat('../data/sample/pubmed.mat', {'adjacency_matrix': network})
        np.save('../data/sample/pubmed.npy', new_edges)


def main():
    load_data_blogcatalog()
    load_data_citeseer()
    load_data_flickr()
    load_data_pubmed()

if __name__ == '__main__':
    main()
