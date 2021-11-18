from nltk.cluster.util import cosine_distance
import numpy as np
from hazm import *
import networkx as nx
import re
from normalizer import normalize

class Summarizer:
    
    def __init__(self, *arg, **kwarg):
        pass

    def load_stopwords(self):
        with open("persian") as file:
            txt = file.readlines()
        
        stopwords = [i.replace("\n", "") for i in txt]

        return stopwords
    
    def read_clean(self, data):
        """Read, clean and split the given file"""
        article = sent_tokenize(data)
        sentences_tok = [word_tokenize(normalize(s)) for s in article]  
        return sentences_tok
    
    
    def sentence_similarity(self, sent1, sent2):
        stopwords = self.load_stopwords()

        all_words = list(set(sent1+sent2))
        # Building zero valued vectors with length : len(all_words)
        vector1 = [0]*len(all_words)
        vector2 = [0]*len(all_words)
        # Building vector for first(sent1) and second(sent2) sentence
        for w in sent1:
            if w in stopwords:
                continue
            vector1[all_words.index(w)] += 1

        for w in sent2:
            if w in stopwords:
                continue
            vector2[all_words.index(w)] += 1
        return 1 - cosine_distance(vector1, vector2)
    
    
    def build_similarity_matrix(self, sentences):
        """Building similarity_matrix based on cosine_distance of two sentenece"""
        similarity_matrix = np.zeros((len(sentences), len(sentences))) # Create an empty similarity matrix
        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2:
                    continue
                similarity_matrix[idx1][idx2] = self.sentence_similarity(sentences[idx1], sentences[idx2])
        return similarity_matrix
    
    def generate_summary(self, path, top_n=2):
        summarize_text = []
        # read, clean and split text file
        sentences = self.read_clean(path)
        # Generate similarity matrix across the sentences
        sentence_similarity_matrix = self.build_similarity_matrix(sentences)
        # biuld a graph for numpy array
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
        # rank nodes(sentences) in graph based on structure of the incoming links
        scores = nx.pagerank(sentence_similarity_graph)
        # Sort the rank and pick top sentences
        ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
        # print("Indexes of top ranked_sentence order are: ", ranked_sentence)
        
        for i in range(top_n):
            if len(sentences) <= top_n:
                summarize_text = ["متن انتخابی کوتاه است"]
            else:
                summarize_text.append(" ".join(ranked_sentence[i][1]))

        return ". ".join(summarize_text)