import numpy as np
import pickle
import networkx as nx
import csv
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

from utils.save_load import save_csv_from_numpy

#HIN Construction
def construct_hin():

    hin_movielens = nx.Graph()

    # load user-movie array (user, movie , rating)
    f = open("../Data/user_movie_rating_list.csv")
    line = f.readline()
    while line:
        content = line.split("\t")
        hin_movielens.add_edge('U_' + content[0], 'M_' + content[1], weight=content[2])
        line = f.readline()
    f.close()

    # load movie-aspect array (movie, aspect, 1)
    f = open("../Data/movie_genres_list.csv")
    line = f.readline()
    while line:
        content = line.split("\t")
        hin_movielens.add_edge('M_' + content[0], 'A_' + content[1], weight=1)
        line = f.readline()
    f.close()

    # load user-user embedding similarity matrix
    f1 = open('E://PyCharmProjs//HIN//Data//user_embedding.pickle', 'rb')
    user_embed = pickle.load(f1)
    f1.close()
    sim_user = cosine_similarity(user_embed)
    m = sim_user.shape[0]
    for i in range(m):
        sim_user[i, i] = 0
    scaler = MinMaxScaler()
    scaler.fit(sim_user)
    sim_user = scaler.transform(sim_user)
    TH_USER = np.percentile(sim_user, 99.6)
    #print(TH_USER)

    # load user-user pearson similarity matrix
    f1 = open('E://PyCharmProjs//HIN//Data//user_similarity_pearson.pickle', 'rb')
    sim_user_pearson = pickle.load(f1)
    for i in range(m):
        sim_user_pearson[i, i] = 0
    TH_USER_pearson = np.percentile(sim_user_pearson, 99.6)
    #print(TH_USER_pearson)

    # user-user
    index = 0
    user_set = set()
    for i in range(sim_user.shape[0]):
        for j in range(i, sim_user.shape[1]):
            if sim_user[i, j] >= TH_USER:
                index = index + 1
                user_set.add(str(i) + "-" + str(j))
    #print("sim_user:", index)

    # user-user_pearson
    index = 0
    user_pearson_set = set()
    for i in range(sim_user_pearson.shape[0]):
        for j in range(i, sim_user_pearson.shape[1]):
            if sim_user_pearson[i, j] >= TH_USER_pearson:
                index = index + 1
                user_pearson_set.add(str(i) + "-" + str(j))
    #print("sim_user_pearson:",index)

    #common_user = list(user_set.intersection(user_pearson_set))
    common_user = list(user_set.union(user_pearson_set))

    #print(len(common_user))
    user_user_list = list()
    for idx in range (len(common_user)):
        user_str = common_user[idx]
        user_pairs = user_str.split("-")
        u_i = user_pairs[0]
        u_j = user_pairs[1]
        weight = (sim_user[int(u_i), int(u_j)] + sim_user_pearson[int(u_i), int(u_j)])/2
        user_user_list.append([int(u_i) + 1, int(u_j) + 1, weight])
        hin_movielens.add_edge('U_' + str(int(u_i)+1), 'U_' + str(int(u_j)+1), weight=weight)

    save_csv_from_numpy("E://PyCharmProjs//HIN//Data//user_user_list.csv", user_user_list)

    # load movie-movie embedding similarity matrix
    f2 = open('E://PyCharmProjs//HIN//Data//movie_embedding.pickle', 'rb')
    movie_embedd = pickle.load(f2)
    f2.close()
    sim_movie = cosine_similarity(movie_embedd)
    m = sim_movie.shape[0]
    for i in range(m):
        sim_movie[i, i] = 0
    scaler = MinMaxScaler()
    scaler.fit(sim_movie)
    sim_movie = scaler.transform(sim_movie)
    TH_ITEM = np.percentile(sim_movie, 99.35)
    #print(TH_ITEM)

    # load movie-movie pearson similarity matrix
    f2 = open('E://PyCharmProjs//HIN//Data//movie_similarity_pearson.pickle', 'rb')
    sim_movie_pearson = pickle.load(f2)
    f2.close()
    for i in range(m):
        sim_movie_pearson[i, i] = 0
    TH_ITEM_Pearson = np.percentile(sim_movie_pearson, 99.3)
    #print(TH_ITEM_Pearson)

    # movie-movie
    movie_set = set()
    for i in range(sim_movie.shape[0]):
        for j in range(i, sim_movie.shape[1]):
            if sim_movie[i, j] >= TH_ITEM:
                movie_set.add(str(i) + "-" + str(j))
    #print("sim_movie:", index)

    # movie-movie_pearson
    movie_pearson_set = set()
    for i in range(sim_movie_pearson.shape[0]):
        for j in range(i, sim_movie_pearson.shape[1]):
            if sim_movie_pearson[i, j] >= TH_ITEM_Pearson:
                movie_pearson_set.add(str(i) + "-" + str(j))
    #print("sim_user_pearson:",index)

    # common_movie = list(movie_set.intersection(movie_pearson_set))
    common_movie = list(movie_set.union(movie_pearson_set))

    movie_movie_list = list()
    #print(len(common_movie))
    for idx in range(len(common_movie)):
        movie_str = common_movie[idx]
        movie_pairs = movie_str.split("-")
        m_i = movie_pairs[0]
        m_j = movie_pairs[1]
        weight = (sim_movie[int(m_i), int(m_j)] + sim_movie_pearson[int(m_i), int(m_j)]) / 2
        movie_movie_list.append([int(m_i)+1, int(m_j)+1, weight])
        hin_movielens.add_edge('M_' + str(int(m_i) + 1), 'M_' + str(int(m_j) + 1), weight=weight)

    save_csv_from_numpy("E://PyCharmProjs//HIN//Data//movie_movie_list.csv", movie_movie_list)

    # save the whole hin
    nx.write_gpickle(hin_movielens, "E://PyCharmProjs//HIN//Data//hin_movielens.gpickle")





