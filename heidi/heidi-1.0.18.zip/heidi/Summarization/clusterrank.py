#!/usr/bin/python

import io
import nltk
import itertools
from operator import itemgetter
import networkx as nx
import os
from ..Segmentation import texttiling
from ..Parse import parse
import networkx as nx
import math
import json
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag
import argparse

class ClusterRank():

    def __init__(self):
        print "Cluster Rank"

    def lDistance(self, firstString, secondString):
        if len(firstString) > len(secondString):
            firstString, secondString = secondString, firstString
        distances = range(len(firstString) + 1)
        for index2, char2 in enumerate(secondString):
            newDistances = [index2 + 1]
            for index1, char1 in enumerate(firstString):
                if char1 == char2:
                    newDistances.append(distances[index1])
                else:
                    newDistances.append(1 + min((distances[index1], distances[index1+1], newDistances[-1])))
            distances = newDistances
        return distances[-1]

    def buildGraph(self, nodes):
        gr = nx.Graph() #initialize an undirected graph
        gr.add_nodes_from(nodes)
        nodePairs = list(itertools.combinations(nodes, 2))

        #add edges to the graph (weighted by Levenshtein distance)
        for pair in nodePairs:
            firstString = pair[0]
            secondString = pair[1]
            levDistance = self.lDistance(firstString, secondString)
            gr.add_edge(firstString, secondString, weight=levDistance)

        return gr

    def extractSentences(self, text):
        sentenceTokens = text
        print "Building graph"
        graph = self.buildGraph(sentenceTokens)

        print "Computing page rank"
        calculated_page_rank = nx.pagerank(graph, weight='weight')

        #most important sentences in ascending order of importance
        print "Assigning score to sentences"
        sentences = sorted(calculated_page_rank, key=calculated_page_rank.get, reverse=True)

        #return a 100 word summary
        print "Generating summary"
        summary = ' '.join(sentences)
        summaryWords = summary.split()
        summaryWords = summaryWords[0:201]
        summary = ' '.join(summaryWords)

        print "Operation completed"
        return summary

    def build_graph(self, nodes, threshold, idf):
        
        gr = nx.Graph() 
        gr.add_nodes_from(nodes)
        nodePairs = list(itertools.combinations(nodes, 2))

        for pair in nodePairs:
            node1 = pair[0]
            node2 = pair[1]
            simval = self.idf_modified_cosine(word_tokenize(node1), word_tokenize(node2), idf)
            if simval > threshold:
                gr.add_edge(node1, node2, weight=simval)

        return gr

    def get_keysentences(self, graph):
        calculated_page_rank = nx.pagerank(graph, weight='weight')
        keysentences = sorted(calculated_page_rank, key=calculated_page_rank.get, reverse=False)
        return keysentences

    def tokenize(self, data):
        sent_tokens = sent_tokenize(data)
        word_tokens = [word_tokenize(sent) for sent in sent_tokens]
        return sent_tokens, word_tokens

    def get_words(self, data):
        words = word_tokenize(data)
        return words

    def idf(self, word_tokens, words, N):
        dict = {}
        for word in words:
            for sent in word_tokens:
                if word in sent:
                    if word in dict.keys():
                        dict[word] += 1

                    else:
                        dict[word] = 1
        for word, count in dict.items():
            dict[word] = math.log((N/float(count)))
        return dict

    def idf_modified_cosine(self, x, y, idf):
        try:
            sum = 0
            combine = x + y
            for word in combine:
                tf1, tf2 = x.count(word), y.count(word)
                sum += int(tf1) * int(tf2) * float((idf[word] ** 2))
                total1, total2 = 0, 0
            for word in x:
                tf = x.count(word)
                total1 += int(tf) * float(idf[word])
            for word in y:
                tf = y.count(word)
                total2 += int(tf) * float(idf[word])
            deno = (math.sqrt((total1**2))) * (math.sqrt((total2**2)))
            return float(sum)/deno
        except Exception as e:
            pass

    def get_similarity_matrix(self, word_tokens, idf):
        matrix = []
        for sent1 in word_tokens:
            row = []
            for sent2 in word_tokens:
                sim = self.idf_modified_cosine(sent1, sent2, idf)
                row.append(sim)
            matrix.append(row)
        return matrix


    def summarize(self, data, threshold=0.15, N=10):
        t = texttiling.TextTiling()
        text = t.run(data)
        sent_tokens, word_tokens = self.tokenize(data)
        sent_tokens = text
        words = list(set(self.get_words(data)))
        N = len(sent_tokens)
        idf = self.idf(word_tokens, words, N)
        matrix = self.get_similarity_matrix(word_tokens, idf)
        gr = self.build_graph(sent_tokens, threshold, idf)
        keysentences = self.get_keysentences(gr)
        return keysentences[0:10]

    def summarizeFile(self, pathToFile, threshold=0.15, N=10):
        p = parse.Parse()
        t = texttiling.TextTiling()
        data = p.dataFromFile(pathToFile)
        text = t.run(data)
        sent_tokens, word_tokens = self.tokenize(data)
        sent_tokens = text
        words = list(set(self.get_words(data)))
        N = len(sent_tokens)
        idf = self.idf(word_tokens, words, N)
        matrix = self.get_similarity_matrix(word_tokens, idf)
        gr = self.build_graph(sent_tokens, threshold, idf)
        keysentences = self.get_keysentences(gr)
        return keysentences[0:10]
