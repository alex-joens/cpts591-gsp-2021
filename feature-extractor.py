
# feature-extractor.py

import re
from os import listdir

WORD_COUNT_THRESHOLD = 5
word_counts = {}
feature_map = {} # to map features (words) to node indices
classes = {} # classes (newsgroups) which documents may fall under
excluded_files = []

def get_words(file_str):
    matches = re.findall("\w+\s+", contents_str)
    for i in range(len(matches)):
        matches[i] = matches[i].strip()
    return matches

# maps features (words) to node indexes
def create_feature_map(word_counts):
    node_idx = 0
    feature_map = {} 
    for (key, val) in word_counts.items():
        if val >= WORD_COUNT_THRESHOLD:
            feature_map[key] = node_idx
            node_idx += 1
    
    return feature_map

classes = listdir("20_newsgroups")

for class_name in classes:
    directory = "20_newsgroups/{}".format(class_name)
    files = listdir(directory)
    print(directory)
    
    for file_name in files:
        file = open("{}/{}".format(directory, file_name), "r")
        file_str = file.read()
        
        end_header = re.search("Lines:\s*\d+", file_str)
        if end_header is None:
            excluded_files.append("{}/{}".format(directory, file_name))
            continue
        
        end_header = end_header.end()
        contents_str = file_str[end_header:]
        words = get_words(file_str)

        for word in words:
            word = word.upper()
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1

feature_map = create_feature_map(word_counts)

print( len(word_counts) )
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

