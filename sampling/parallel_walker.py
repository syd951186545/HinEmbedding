import random
import copy
import time
import multiprocessing as mp
import numpy as np
from joblib import Parallel, delayed
import networkx as nx


def parallel_walk(Graph, num_walks, meta_path):
    # meta_path的长度就是游走序列的长度
    start_node_type = meta_path[0]
    walk_seqs = []
    walk_seq=[]
    # 下面随机打乱的意义在于选取第一个出现的某一类节点，就是随机的
    for n_walk in range(num_walks):
        possible_start_node = [node for node in Graph.nodes(data="type") if node[1] == start_node_type]

        if not possible_start_node:
            raise Exception("can not choice start_node")
        else:
            start_node = random.choice(possible_start_node)

        walk_seq = [str(start_node[0]), ]
        current_node = start_node[0]
        for node_type in meta_path[1:]:
            if node_type is "done":
                break
            possible_neighbor_nodes = [node for node in Graph[current_node] if Graph.nodes[node]["type"] == node_type]
            if not possible_neighbor_nodes:
                # 没有邻接点了
                break
            else:
                current_node = random.choice(possible_neighbor_nodes)
                walk_seq.append(str(current_node))

        walk_seqs.append(walk_seq)
    return walk_seqs


if __name__ == '__main__':
    Graphx = nx.read_gpickle("./data/DBLP_labeled.Graph")
    meta_path = ["A", "P", "T", "P", "A", "P", "C"]
    num_walks = 10000
    num_workers = 4

    # num_walks_lists = np.array_split(range(num_walks), num_workers)
    avg_walk = int(num_walks / num_workers)  # 必须能整除
    walkss = [2500, 2500, 2500, 2500]
    if num_workers * avg_walk != num_walks:
        raise Exception("please set num_walks can be be divisible by num_workers")
    a = time.time()
    parallel_walk(Graphx, num_walks, meta_path)
    b = time.time()
    time_normal = b - a

    Parallel(n_jobs=4)(
        delayed(parallel_walk)(Graphx, avg_walk, meta_path) for avg_walk in walkss)
    c = time.time()
    time_processing = c - b

    Parallel(n_jobs=4, backend="multiprocessing")(
        delayed(parallel_walk)(Graphx, avg_walk, meta_path) for avg_walk in walkss)
    d = time.time()
    time_threading = d - c
    print("跑的量越大多进程越快")
    walk_seqs = Parallel(n_jobs=6, backend="multiprocessing")(
        delayed(parallel_walk)(self.Graph, 1, self.current_metapath) for i in range(self.number_walks_Terminated))
    time_mutipool = time.time()-d