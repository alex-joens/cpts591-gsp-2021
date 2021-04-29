
# feature-extractor.py

import re
from os import listdir
from utils import get_file_contents
from utils import get_words

FILE_COUNT_THRESHOLD = 20
FILE_COUNT_MAX_PROPORTION = 0.5
file_counts = {} # number of files a feature (word) occurs in
feature_map = {} # to map features (words) to node indices
classes = {} # classes (newsgroups) which documents may fall under
excluded_files = []
num_files = 0

# maps features (words) to node indexes
def create_feature_map(file_counts, num_files):
    max_file_count = FILE_COUNT_MAX_PROPORTION * num_files
    node_idx = 0
    feature_map = {} 
    for (key, val) in file_counts.items():
        if val >= FILE_COUNT_THRESHOLD and val <= max_file_count:
            feature_map[key] = node_idx
            node_idx += 1
    
    return feature_map

classes = listdir("20_newsgroups")

for class_name in classes:
    directory = "20_newsgroups/{}".format(class_name)
    files = listdir(directory)
    print(directory)
    
    for file_name in files:
        file_str = open("{}/{}".format(directory, file_name), "r").read()
        contents_str = utils.get_file_body(file_str)
        words = get_words(contents_str)

        word_occurrences = {}
        for word in words:
            if word not in word_occurrences:
                word_occurrences[word] = True
                
        for word in word_occurrences:
            if word not in file_counts:
                file_counts[word] = 1
            else:
                file_counts[word] += 1
        num_files += 1

feature_map = create_feature_map(file_counts, num_files)

print( len(file_counts) )
print( len(feature_map) )

features_str = ""
excluded_files_str = ""
for (feature, _) in feature_map.items():
    features_str = features_str + feature + ","
for val in excluded_files:
    excluded_files_str = excluded_files_str + val + "\n"
    
features_str = features_str[0:len(features_str) - 1]

features_file = open("features.csv", "w")
excluded_files_file = open("excluded_files.txt", "w")
features_file.write(features_str)
excluded_files_file.write(excluded_files_str)

