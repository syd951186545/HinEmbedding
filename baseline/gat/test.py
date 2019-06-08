from gat_api import *
import networkx as nx
from  graph import *


path = 'E:/Codes/Code/Python Codes/pyGAT/data/citeseer'
g = Graph()
g.read_edgelist(path+'/citeseer.edgelist')
g.read_node_features(path + '/citeseer.feature')
g.read_node_label(path + '/citeseer.label')

GAT_api(g,False,100,0.005,5e-4,hidden = 8,nb_heads = 8,drop_out = 0.6,
                alpha = 0.2 ,patience = 100)


