
# feature-extractor.py

import re
from os import listdir

WORD_COUNT_THRESHOLD = 5
word_counts = {}
feature_map = {} # to map features (words) to node indices
classes = {} # classes (newsgroups) which documents may fall under

def get_words(file_str):
    matches = re.findall("\s+\w+\s+", contents_str)
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
    
    for file in files:
        file = open("{}/{}".format(directory, file), "r")
        file_str = file.read()
        end_header = re.search("Lines:\s*\d+", file_str).end()
        contents_str = file_str[end_header:]
        words = get_words(file_str)

        for word in words:
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1
                
feature_map = create_feature_map(word_counts)




    



