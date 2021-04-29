
# utils.py

import re

def get_words(contents_str):
    matches = re.findall("\w+\s+", contents_str)
    for i in range(len(matches)):
        matches[i] = matches[i].strip().upper()
    return matches
    
def get_file_body(file_str):
    end_header = re.search("Lines:\s*\d+", file_str)
    if end_header is None:
        return ""
    
    end_header = end_header.end()
    return file_str[end_header:]