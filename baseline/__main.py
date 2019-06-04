from __future__ import print_function
import numpy as np
import random
from sklearn.linear_model import LogisticRegression
from .graph import *
from . import node2vec
from .classify import Classifier, read_node_label
from . import line
from . import tadw
# from .gcn import gcnAPI
from . import lle
from . import hope
from . import lap
from . import gf
from . import sdne
from .grarep import GraRep
import time
import ast

def __main(args):
    t1 = time.time()
    g = Graph()
    print("Reading...")

    if args.graph_format == 'adjlist':
        g.read_adjlist(filename=args.input)
    elif args.graph_format == 'edgelist':
        g.read_edgelist(filename=args.input, weighted=args.weighted,
                        directed=args.directed)
    if args.method == 'node2vec':
        model = node2vec.Node2vec(graph=g, path_length=args.walk_length,
                                  num_paths=args.number_walks, dim=args.representation_size,
                                  workers=args.workers, p=args.p, q=args.q, window=args.window_size)
    elif args.method == 'line':
        if args.label_file and not args.no_auto_save:
            model = line.LINE(g, epoch=args.epochs, rep_size=args.representation_size, order=args.order,
                              label_file=args.label_file, clf_ratio=args.clf_ratio)
        else:
            model = line.LINE(g, epoch=args.epochs,
                              rep_size=args.representation_size, order=args.order)
    elif args.method == 'deepWalk':
        model = node2vec.Node2vec(graph=g, path_length=args.walk_length,
                                  num_paths=args.number_walks, dim=args.representation_size,
                                  workers=args.workers, window=args.window_size, dw=True)
    elif args.method == 'tadw':
        # assert args.label_file != ''
        assert args.feature_file != ''
        g.read_node_label(args.label_file)
        g.read_node_features(args.feature_file)
        model = tadw.TADW(
            graph=g, dim=args.representation_size, lamb=args.lamb)
    elif args.method == 'gcn':
        assert args.label_file != ''
        assert args.feature_file != ''
        g.read_node_label(args.label_file)
        g.read_node_features(args.feature_file)
        model = gcnAPI.GCN(graph=g, dropout=args.dropout,
                           weight_decay=args.weight_decay, hidden1=args.hidden,
                           epochs=args.epochs, clf_ratio=args.clf_ratio)
    elif args.method == 'grarep':
        model = GraRep(graph=g, Kstep=args.kstep, dim=args.representation_size)
    elif args.method == 'lle':
        model = lle.LLE(graph=g, d=args.representation_size)
    elif args.method == 'hope':
        model = hope.HOPE(graph=g, d=args.representation_size)
    elif args.method == 'sdne':
        encoder_layer_list = ast.literal_eval(args.encoder_list)
        model = sdne.SDNE(g, encoder_layer_list=encoder_layer_list,
                          alpha=args.alpha, beta=args.beta, nu1=args.nu1, nu2=args.nu2,
                          batch_size=args.bs, epoch=args.epochs, learning_rate=args.lr)
    elif args.method == 'lap':
        model = lap.LaplacianEigenmaps(g, rep_size=args.representation_size)
    elif args.method == 'gf':
        model = gf.GraphFactorization(g, rep_size=args.representation_size,
                                      epoch=args.epochs, learning_rate=args.lr, weight_decay=args.weight_decay)
    t2 = time.time()
    print(t2-t1)
    if args.method != 'gcn':
        print("Saving embeddings...")
        model.save_embeddings(args.output)
    if args.label_file and args.method != 'gcn':
        vectors = model.vectors
        X, Y = read_node_label(args.label_file)
        print("Training classifier using {:.2f}% nodes...".format(
            args.clf_ratio*100))
        clf = Classifier(vectors=vectors, clf=LogisticRegression())
        clf.split_train_evaluate(X, Y, args.clf_ratio)


if __name__ == "__main__":
    random.seed(32)
    np.random.seed(32)
    __main(parse_args())
