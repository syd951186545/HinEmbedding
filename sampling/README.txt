walker适用于同质网络游走主要参数为graph（同baseline中的graph.py中的graph类），随机游走参数dw=True，
广度优先游走p=1，q=0
深度优先游走p=0，q=1
使用方式例如：
import walker
walker_example = walker.Walker(graph, p=p, q=q, workers=4)
sentences_example = walker_example.simulate_walks(num_walks=num_paths, walk_length=path_length)
----------------------------------------------------------------------------
parallel_walker适用于异质网络游走，主要参数为graph（networkx的Graph类，节点包含"type"属性为必要）
参数num_walks, meta_path分别为游走路径条数和指定的路径类型
使用方法例如：# 多进程的并行游走在处理大量游走条数需求时快很多倍

from joblib import Parallel, delayed

walkss=[100,100,100,....] # 指定每一个并行worker游走的条数
for i in range(20):
    meta_path = meta_path.extend(["A","P","A"])
Parallel(n_jobs=4, backend="multiprocessing")(
        delayed(parallel_walk)(Graphx, avg_walk, meta_path) for avg_walk in walkss)