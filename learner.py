
# learner.py

import re
import numpy as np
from os import listdir
from utils import get_file_contents
from utils import get_words

LABELED_SET_SIZE = 15
feature_map = {} # to map features (words) to node indices
classes = {} # classes (newsgroups) which documents may fall under (mapped to ids)
complete_adjacency_matrix = None # adjacency matrix for the full collection of documents

feature_file = open("features.csv", "r").read()
features = feature_file.split(",")
for i in range(len(features)):
    feature_map[features[i]] = i

classes_list = listdir("20_newsgroups")
for i in range(len(classes_list)):
    classes[classes_list[i]] = i

# add files to the adjacency matrix
n = len(feature_map)
adjacency_matrix = np.zeros(n * n)
adjacency_matrix = adjacency_matrix.reshape(n,n)
for (class_name, class_id) in classes.items():
    directory = "20_newsgroups/{}".format(class_name)
    files = listdir(directory)
    
    print(directory)
    
    for file_name in files:
        word_occurrences = {}
        file_str = open("{}/{}".format(directory, file_name), "r").read()
        contents_str = get_file_body(file_str)
        words = get_words(contents_str)
        
        for word in words:
            if word not in feature_map:
                continue
            if word not in word_occurrences:
                word_occurrences[word] = True
        
        words_array = []
        for word in word_occurrences:
            idx1 = feature_map[word]
            for word2 in words_array:
                idx2 = feature_map[word2]
                adjacency_matrix[idx1][idx2] += 1
                adjacency_matrix[idx2][idx1] += 1
                adjacency_matrix[idx1][idx1] += 1
                adjacency_matrix[idx2][idx2] += 1
            
            words_array.append(word)

# create initial class subgraphs from a "labeled" subset
# then use the initial class subgraphs as basis to learn a class subgraph with information from all documents
total_degree = 0
for i in range( len(feature_map) ):
    total_degree += adjacency_matrix[i][i]

for (class_name, class_id) in classes.items():
    directory = "20_newsgroups/{}".format(class_name)
    files = listdir(directory)
    initial_class_subgraph = {}
    final_class_subgraph = {}
    # for final_class_subgraph2, a node in the initial subgraph is not necessarily in the final
    final_class_subgraph2 = {} 
    
    print(directory)
    
    for i in range(LABELED_SET_SIZE):
        file_name = files[i]
        word_occurrences = {}
        file_str = open("{}/{}".format(directory, file_name), "r").read()
        contents_str = get_file_contents(file_str)
        words = get_words(contents_str)
        
        for word in words:
            if word not in feature_map:
                continue
            initial_class_subgraph[word] = True
    
    # get the sum of degrees for features within the class subgraph,
    # and the proportion of edges to nodes within the subgraph
    class_total_degree = 0
    proportion = None # >:<
    for feature in initial_class_subgraph:
        node_id = feature_map[feature]
        class_total_degree += adjacency_matrix[node_id][node_id]
    proportion = class_total_degree / total_degree
    
    # for each node, get the total edge weight to nodes within the class subgraph
    class_in_degrees = np.zeros(len(feature_map))
    class_in_degrees2 = np.zeros(len(feature_map))
    for (feature, id) in feature_map.items():
        class_in_degree = 0
        class_in_degree2 = 0
        
        for feature2 in initial_class_subgraph:
            node_id2 = feature_map[feature2]
            class_in_degree += adjacency_matrix[id][node_id2]
            
            # for class_in_degree2, if the node is in the initial subgraph already, add the average edge weight
            # times the likelihood it would be connected to the class subgraph
            if node_id2 == id:
                class_in_degree2 += (adjacency_matrix[id][id] / len(feature_map) * proportion) // 1
            else:
                class_in_degree2 += adjacency_matrix[id][node_id2]
            
        class_in_degrees[id] = class_in_degree
        class_in_degrees2[id] = class_in_degree2
    
    node_degrees = np.zeros(len(feature_map))
    for i in range(len(feature_map)):
        node_degrees[i] = adjacency_matrix[i][i]
    
    for (feature, id) in feature_map.items():
        if((class_in_degrees[id] / node_degrees[id]) > proportion):
            final_class_subgraph[feature] = True
        if((class_in_degrees2[id] / node_degrees[id]) > proportion):
            final_class_subgraph2[feature] = True
            
    print(class_name)
    print(len(initial_class_subgraph))
    print(len(final_class_subgraph))
    print(len(final_class_subgraph2))
    print("proportion: {}".format(proportion))
    print()
    
    # export
    subgraph_str = ""
    subgraph2_str = ""
    for feature in final_class_subgraph:
        subgraph_str = subgraph_str + feature + ","
    for feature in final_class_subgraph2:
        subgraph2_str = subgraph2_str + feature + ","
        
    subgraph_str = subgraph_str[0:len(subgraph_str) - 1]
    subgraph2_str = subgraph2_str[0:len(subgraph2_str) - 1]
    
    subgraph_file = open("{}.csv".format(class_name), "w")
    subgraph_file2 = open("{}2.csv".format(class_name), "w")
    subgraph_file.write(subgraph_str)
    subgraph_file2.write(subgraph2_str)
    
