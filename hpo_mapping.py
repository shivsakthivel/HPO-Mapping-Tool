# Required Libraries
import networkx
import obonet
from collections import defaultdict
import string
import json
import math
from os import listdir
from os.path import isfile, join
import pandas as pd

# Getting the list of files to run the keyword search
onlyfiles = [f for f in listdir() if isfile(f)]
files = []
for f in onlyfiles:
    if 'json' in f:
        files.append(f)

# Import of HPO terms
url = "https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo"
graph = obonet.read_obo(url)
all_nodes = list(graph.nodes.data())

# TF-IDF Set Up
wordCount = defaultdict(int)
punctuation = set(string.punctuation)
for d in all_nodes:
    if 'def' in d[1].keys():
        r = d[1]['def'].split("[")[0]
        r = ''.join([c for c in r.lower() if not c in punctuation])
        for w in r.split():
            wordCount[w] += 1
    if 'comment' in d[1].keys():
        s = ''.join([c for c in d[1]['comment'].lower() if not c in punctuation])
        for w in s.split():
            wordCount[w] += 1
    if 'synonym' in d[1].keys():
        list_syn = d[1]['synonym']
        for item in list_syn:
            t = item.split('"')[1]
            t = ''.join([c for c in t.lower() if not c in punctuation])
            for w in t.split():
                wordCount[w] += 1

counts = [(wordCount[w], w) for w in wordCount]
counts.sort()
counts.reverse()
words = [x[1] for x in counts]

df = defaultdict(int)
for d in all_nodes:
    if 'def' in d[1].keys():
        r = d[1]['def'].split("[")[0]
        r = ''.join([c for c in r.lower() if not c in punctuation])
        for w in set(r.split()):
            df[w] += 1
    if 'comment' in d[1].keys():
        s = ''.join([c for c in d[1]['comment'].lower() if not c in punctuation])
        for w in set(s.split()):
            df[w] += 1
    if 'synonym' in d[1].keys():
        list_syn = d[1]['synonym']
        for item in list_syn:
            t = item.split('"')[1]
            t = ''.join([c for c in t.lower() if not c in punctuation])
            for w in set(t.split()):
                df[w] += 1
all_tf_compare = []
for i in range(len(all_nodes)):
    d = all_nodes[i]
    tf = defaultdict(int)
    if 'def' in d[1].keys():
        r = d[1]['def'].split("[")[0]
        r = ''.join([c for c in r.lower() if not c in punctuation])
        for w in r.split():
            tf[w] = 1
    if 'comment' in d[1].keys():
        s = ''.join([c for c in d[1]['comment'].lower() if not c in punctuation])
        for w in s.split():
            tf[w] = 1
    if 'synonym' in d[1].keys():
        list_syn = d[1]['synonym']
        for item in list_syn:
            t = item.split('"')[1]
            t = ''.join([c for c in t.lower() if not c in punctuation])
            for w in t.split():
                tf[w] = 1
    all_tf_compare.append([tf[w] * math.log2(len(all_nodes) / df[w]) for w in words])

# Empty File
overall = open("hpo_map_1.txt", "a")
overall.write("Phenotype, Most Similar Term, Second Term, Third Term")
overall.close()

# Similarity Function
def Cosine(x1,x2):
    numer = 0
    norm1 = 0
    norm2 = 0
    for a1,a2 in zip(x1,x2):
        numer += a1*a2
        norm1 += a1**2
        norm2 += a2**2
    if norm1*norm2:
        return numer / math.sqrt(norm1*norm2)
    return 0

count = 0                
for f in files:
    read_file = open(f)
    data = json.load(read_file)
    
    count += 1
    print(count)
    
    tf_compare = defaultdict(int)
    r = ''.join([c for c in data['description'].lower() if not c in punctuation])
    for w in r.split():
        tf_compare[w] = 1
    s = ''.join([c for c in data['phenotype_concept'].lower() if not c in punctuation])
    for w in s.split():
        tf_compare[w] = 1
    tfidf = dict(zip(words,[tf_compare[w] * math.log2(len(all_nodes) / df[w]) for w in words]))
    tfidfQuery = [tf_compare[w] * math.log2(len(all_nodes) / df[w]) for w in words]
    
    pheno_concept = data['phenotype_concept']

    similarities = []
    for i in range(len(all_nodes)):
        d = all_nodes[i]
        tfidf2 = all_tf_compare[i]
        similarities.append((Cosine(tfidfQuery, tfidf2), d[1]['name'], d[0]))
    
    similarities.sort(reverse=True)
    term_1 = similarities[0]
    term_2 = similarities[1]
    term_3 = similarities[2]
    
    overall = open("hpo_map_1.txt", "a")
    fields = [pheno_concept, str((term_1[1], term_1[2])), str((term_2[1], term_2[2])), str((term_3[1], term_3[2]))]
    string_to_append = ", ".join(fields)
    overall.write(string_to_append)
    overall.close()
                                                                                                                                    