"""
trie.py

author: Colin Clement
date: 2016-01-14

Given a lexicon of words, Trie object computes the corresponding trie.
TODO: Create function or class DAWG which merges suffixes in Trie to
get the DAWG of a lexicon.

"""


import string
from collections import defaultdict


class Node(object):
    def __init__(self, label):
        assert type(label) is int, 'label must be int'
        self.label = label
        self.children = {}
        self.parents = {}
        self.strset = set([])  # list of complete words

    def addchild(self, edge, node):
        assert type(node) is Node, 'node must be a Node'
        assert type(edge) is str, 'edge must be a char'
        self.children[edge] = node
        node.parents[edge] = node
        return node

    def __repr__(self):
        """ Make print(self) useful """
        pstr = "{label} \033[1;35;49m("  # pretty purple
        if self.strset:
            pstr += reduce(lambda s, r: s + ', ' + r, self.strset) 
        pstr += ")\033[0m: "
        pstr += reduce(lambda s, r: s + ' ' + r, self.children)
        return pstr.format(**self.__dict__)


class Trie(object):
    """
    Edges have a char associated with them and point between two nodes
    Nodes are labeled by a unique int, contain a set of strings which are
    complete words
    """
    def __init__(self):
        self.nodes = [Node(0)]  # First node is empty string
        self.edges = defaultdict(set)

    @property
    def N(self):
        """ Number of nodes """
        return len(self.nodes)

    @property
    def E(self):
        """ Number of edges """
        return sum([len(self.edges[c]) for c in self.edges])
    
    def parselex(self, w):
        """ Parse string w, adding lexicon to trie """
        assert type(w) == str, "w must be str"
        loc = self.nodes[0]
        path = ''
        for c in w:
            if c in loc.children: 
                loc = loc.children[c]
                path += c
            elif c in string.whitespace:
                loc.strset.add(path)
                loc = self.nodes[0]  # end of word, go to top
                path = ''
            else:  # Create edge, node
                loc = loc.addchild(c, Node(self.N+1))
                self.nodes.append(loc)
                self.edges[c].add((loc.parents[c], loc))
                path += c
