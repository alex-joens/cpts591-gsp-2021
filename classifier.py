
# classifier.py

import re
import numpy as np
from os import listdir
from utils import get_file_body
from utils import get_words

feature_map = {} # to map features (words) to node indices
classes = listdir("20_newsgroups") # classes (newsgroups) which documents may fall under
class_subgraphs = {}
classification_aggregates = {} # aggregate classification scores indexed by class

feature_file = open("features.csv", "r").read()
features = feature_file.split(",")
for i in range(len(features)):
    feature_map[features[i]] = i
    
for class_name in classes:
    file_str = open("class-subgraphs/{}2.csv".format(class_name), "r").read()
    class_features = file_str.split(",")
    
    class_subgraphs[class_name] = {}
    for feature in class_features:
        class_subgraphs[class_name][feature] = True

for class_name in classes:
    directory = "20_newsgroups/{}".format(class_name)
    files = listdir(directory)
    
    file_classifications = []
    classification_template = {\
        "actual_class": None,\
        "assigned_class": None,\
        "score_actual": None,\
        "score_assigned": None,\
        "score_average": None,\
        "num_words": None,\
        "num_features": None}
    
    print(directory)
    
    for file_name in files:
        classified_as = None
        class_similarity = 0
        total_similarity = 0
        highest_similarity = 0
        num_words = 0
        num_features = 0
        
        file_str = open("{}/{}".format(directory, file_name), "r").read()
        contents_str = get_file_body(file_str)
        words = get_words(contents_str)

        file_subgraph = {}
        for word in words:
            if word not in feature_map:
                continue
                
            if word not in file_subgraph:
                num_features += 1
                file_subgraph[ word ] = True
            
            num_words += 1
        
        for (class_name2, class_subgraph) in class_subgraphs.items():
            class_score = 0
            for feature in file_subgraph:
                if feature in class_subgraph:
                    total_similarity += 1
                    class_score += 1
            
            if(class_name == class_name2):
                class_similarity = class_score
                
            if(class_score > highest_similarity):
                highest_similarity = class_score
                classified_as = class_name2
        
        classification = {\
            "actual_class": class_name,\
            "assigned_class": classified_as,\
            "score_actual": class_similarity,\
            "score_assigned": highest_similarity,\
            "score_average": total_similarity / len(class_subgraphs),\
            "num_words": num_words,\
            "num_features": num_features}
        file_classifications.append(classification)

    num_correct = 0
    num_incorrect = 0
    total_assigned_score = 0
    total_actual_score = 0
    total_average_score = 0
    total_words_correct = 0
    total_words_incorrect = 0
    total_features_correct = 0
    total_features_incorrect = 0
    
    for classification in file_classifications:
        if(classification["actual_class"] == classification["assigned_class"]):
            num_correct += 1
            total_words_correct += classification["num_words"]
            total_features_correct += classification["num_features"]
        else:
            num_incorrect += 1
            total_words_incorrect += classification["num_words"]
            total_features_incorrect += classification["num_features"]
        
        total_assigned_score += classification["score_assigned"]
        total_actual_score += classification["score_actual"]
        total_average_score += classification["score_average"]
    
    num_files = len(file_classifications)
    classification_aggregates[class_name] = {
        "num_correct": num_correct,
        "num_incorrect": num_incorrect,
        "average_assigned_score": total_assigned_score / num_files,
        "average_actual_score": total_actual_score / num_files,
        "average_average_score": total_average_score / num_files,
        "average_words_correct": total_words_correct / num_files,
        "average_words_incorrect": total_words_incorrect / num_files,
        "average_features_correct": total_features_correct / num_files,
        "average_features_incorrect": total_features_incorrect / num_files
    }

for (class_name, aggregate) in classification_aggregates.items():
    file = open("classification-aggregates/{}.txt".format(class_name), "w")
    file_str = ""
    for (label, score) in aggregate.items():
        file_str = file_str + label + ": " + str(score) + "\n"
    
    file.write(file_str)

