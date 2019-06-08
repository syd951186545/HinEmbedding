from __future__ import division
from __future__ import print_function

import os
import glob
import time
import random
import  networkx as nx
from itertools import chain
import numpy as np
import scipy.sparse as sp
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable

from utils import  accuracy,encode_onehot
from models import GAT, SpGAT
random_seed = 72
class GAT_api(object):
    def __init__(self,graph,sparse = False,epochs = 200,learning_rate = 0.005,
                 weight_decay = 5e-4,hidden = 8,nb_heads = 8,drop_out = 0.6,
                alpha = 0.2 ,patience = 100,train = 1500,val = 2000,test = 3100):
        self.graph = graph
        self.sparse  = sparse
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.hidden = hidden
        self.nb_heads  = nb_heads
        self.drop_out = drop_out
        self.alpha = alpha
        self.patience = patience
        self.train = train
        self.val = val
        self.test = test

        idx_train,idx_val , idx_test = self.load_data()

        random.seed(random_seed)
        np.random.seed(random_seed)
        torch.manual_seed(random_seed)

        if self.sparse:
            model = SpGAT(nfeat=self.features.shape[1],
                          nhid=self.hidden,
                          nclass=int(self.labels.max()) + 1,
                          dropout=self.drop_out,
                          nheads=self.nb_heads,
                          alpha=self.alpha)
        else:
            model = GAT(nfeat=self.features.shape[1],
                        nhid=self.hidden,
                        nclass=int(self.labels.max()) + 1,
                        dropout=self.drop_out,
                        nheads=self.nb_heads,
                        alpha=self.alpha)

        optimizer = optim.Adam(model.parameters(),
                               lr=self.learning_rate,
                               weight_decay=self.weight_decay)

        #利用GPU
        # device = torch.device("cuda:0")
        # torch.cuda.empty_cache()
        # model.to(device)
        # self.features = self.features.to(device)
        # self.adj = self.adj.to(device)
        # self.labels = self.labels.to(device)
        # idx_train = idx_train.to(device)
        # idx_val = idx_val.to(device)
        # idx_test = idx_test.to(device)

        features, adj, labels = Variable(self.features), Variable(self.adj), Variable(self.labels)

        t_total = time.time()
        loss_values = []
        bad_counter = 0
        best = self.epochs + 1
        best_epoch = 0
        for epoch in range(self.epochs):

            t = time.time()
            model.train()
            optimizer.zero_grad()
            output = model(features, adj)
            loss_train = F.nll_loss(output[idx_train], labels[idx_train])
            acc_train = accuracy(output[idx_train], labels[idx_train])
            loss_train.backward()
            optimizer.step()

            model.eval()
            output = model(features, adj)

            loss_val = F.nll_loss(output[idx_val], labels[idx_val])
            acc_val = accuracy(output[idx_val], labels[idx_val])

            print('Epoch: {:04d}'.format(epoch + 1),
                  'loss_train: {:.4f}'.format(loss_train.data),
                  'acc_train: {:.4f}'.format(acc_train.data),
                  'loss_val: {:.4f}'.format(loss_val.data),
                  'acc_val: {:.4f}'.format(acc_val.data),
                  'time: {:.4f}s'.format(time.time() - t))
            loss_values.append(loss_val.data)
            torch.save(model.state_dict(), '{}.pkl'.format(epoch))
            if loss_values[-1] < best:
                best = loss_values[-1]
                best_epoch = epoch
                bad_counter = 0
            else:
                bad_counter += 1

            if bad_counter == self.patience:
                break

            files = glob.glob('*.pkl')
            for file in files:
                epoch_nb = int(file.split('.')[0])
                if epoch_nb < best_epoch:
                    os.remove(file)

        print("Optimization Finished!")
        print("Total time elapsed: {:.4f}s".format(time.time() - t_total))
        print('Loading {}th epoch'.format(best_epoch))
        model.load_state_dict(torch.load('{}.pkl'.format(best_epoch)))

        model.eval()
        output = model(features, adj)
        loss_test = F.nll_loss(output[idx_test], labels[idx_test])
        acc_test = accuracy(output[idx_test], labels[idx_test])
        print("Test set results:",
              "loss= {:.4f}".format(loss_test.data),
              "accuracy= {:.4f}".format(acc_test.data))

    def load_data(self):
        g = self.graph.G
        look_back = self.graph.look_back_list
        adj = nx.to_scipy_sparse_matrix(g)
        # adj = adj + adj.T.multiply(adj.T > adj) - adj.multiply(adj.T > adj)
        adj = self.normalize_adj(adj + sp.eye(adj.shape[0]))
        self.adj = torch.FloatTensor(np.array(adj.todense()))


        labels = []
        for node in g.nodes():
            labels.append((g.nodes[node]['label']))
        #合并多列表
        labels = list(chain(*labels))
        labels = encode_onehot(labels)
        self.labels = torch.LongTensor(np.where(labels)[1])

        features = np.vstack([g.nodes[look_back[i]]['feature']
                                   for i in range(g.number_of_nodes())])
        features = self.normalize_features(features)
        self.features = torch.FloatTensor(np.array(features))

        idx_train = torch.LongTensor(range(self.train))
        idx_val = torch.LongTensor(range(self.train,self.val))
        idx_test = torch.LongTensor(range(self.val,self.test))

        return idx_train,idx_val,idx_test

    def normalize_adj(self,mx):
        """Row-normalize sparse matrix"""
        rowsum = np.array(mx.sum(1))
        r_inv_sqrt = np.power(rowsum, -0.5).flatten()
        r_inv_sqrt[np.isinf(r_inv_sqrt)] = 0.
        r_mat_inv_sqrt = sp.diags(r_inv_sqrt)
        return mx.dot(r_mat_inv_sqrt).transpose().dot(r_mat_inv_sqrt)

    def normalize_features(self,mx):
        """Row-normalize sparse matrix"""
        rowsum = np.array(mx.sum(1))
        r_inv = np.power(rowsum, -1).flatten()
        r_inv[np.isinf(r_inv)] = 0.
        r_mat_inv = sp.diags(r_inv)
        mx = r_mat_inv.dot(mx)
        return mx