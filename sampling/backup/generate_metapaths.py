import numpy as np
import pickle
import networkx as nx
from stellargraph.data import UniformRandomMetaPathWalk
from stellargraph import StellarGraph


def construct_hin_pandas():
    n_users = 6040
    n_movie = 3952
    n_genres = 18

    # generate node list
    user_node_ids = list(range(1, n_users+1))
    user_node_ids = ["u" + str(user_node_id) for user_node_id in user_node_ids]

    movie_node_ids = list(range(1, n_movie+1))
    movie_node_ids = ["m" + str(movie_id) for movie_id in movie_node_ids]

    apsect_node_ids = list(range(1, n_genres+1))
    apsect_node_ids = ["a" + str(aspect_id) for aspect_id in apsect_node_ids]


    # generate edge list
    user_movie_edge = list()
    with open("E://PyCharmProjs//HIN//Data//user_movie_rating_list.csv", 'r') as f:
        for line in f.readlines():
            curLine = line.strip().split("\t")
            user_movie_edge.append([int(curLine[0]), int(curLine[1]), float(curLine[2])])

    user_user_edge = list()
    with open("E://PyCharmProjs//HIN//Data//user_user_list.csv", 'r') as f:
        for line in f.readlines():
            curLine = line.strip().split("\t")
            user_user_edge.append([int(curLine[0]), int(curLine[1]), float(curLine[2])])

    movie_movie_edge = list()
    with open("E://PyCharmProjs//HIN//Data//movie_movie_list.csv", 'r') as f:
        for line in f.readlines():
            curLine = line.strip().split("\t")
            movie_movie_edge.append([int(curLine[0]), int(curLine[1]), float(curLine[2])])

    movie_aspect_edge = list()
    with open("E://PyCharmProjs//HIN//Data//movie_genres_list.csv", 'r') as f:
        for line in f.readlines():
            curLine = line.strip().split("\t")
            movie_aspect_edge.append([int(curLine[0]), int(curLine[1]), float(curLine[2])])


    u_m_edges = [("u" + str(from_node), "m" + str(to_node)) for from_node, to_node, weight in user_movie_edge]
    u_u_edges = [("u" + str(from_node), "u" + str(to_node)) for from_node, to_node, weight in user_user_edge]
    m_m_edges = [("m" + str(from_node), "m" + str(to_node)) for from_node, to_node, weight in movie_movie_edge]
    m_a_edges = [("m" + str(from_node), "a" + str(to_node)) for from_node, to_node, weight in movie_aspect_edge]

    g_nx = nx.Graph()  # create the graph

    # add user and group nodes with labels 'Person' and 'Group' respectively.
    g_nx.add_nodes_from(user_node_ids, label="user")
    g_nx.add_nodes_from(movie_node_ids, label="movie")
    g_nx.add_nodes_from(apsect_node_ids, label="aspect")


    # add the user-user edges with label 'friend'
    g_nx.add_edges_from(u_m_edges, label="rating")
    g_nx.add_edges_from(u_u_edges, label="friend")
    g_nx.add_edges_from(m_m_edges, label="same")
    g_nx.add_edges_from(m_a_edges, weight = 1, label="include")

    print(g_nx.number_of_nodes())
    print(g_nx.number_of_edges())
    return g_nx


g_nx = construct_hin_pandas()

# Create the random walker
rw = UniformRandomMetaPathWalk(StellarGraph(g_nx))

# specify the metapath schemas as a list of lists of node types.
metapaths = [
    ["user", "user", "movie"],
    #["user", "movie", "aspect", "movie"],
]

walks = rw.run(nodes=list(g_nx.nodes()), # root nodes
               length=3,  # maximum length of a random walk
               n=50,        # number of random walks per root node
               metapaths=metapaths  # the metapaths
              )

for i in range(1000):
    print(walks[i])

print("Number of random walks: {}".format(len(walks)))



