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
        """
        input : int, unique label for node
        """
        assert type(label) is int, 'label must be int'
        self.label = label
        self.children = defaultdict(set)
        self.parents = defaultdict(set)
        self.strset = set([])  # list of complete words

    def addchild(self, edge, node):
        """
        input:
            edge : str, single character
            node : Node object to connect by edge
        returns:
            childnode : Node object
        """
        assert type(node) is Node, 'node must be a Node'
        assert type(edge) is str, 'edge must be a char'
        self.children[edge] = node
        node.parents[edge] = self
        return node

    def __getitem__(self, c):
        return self.children[c]

    def __str__(self):
        """ Make print(self) useful """
        pstr = "{label} \033[1;35;49m("  # pretty purple
        if self.strset:
            pstr += ('{}, '*len(self.strset)).format(*self.strset)[:-2]
        pstr += ")\033[0m: "
        pstr += ('{} '*len(self.children)).format(*self.children)
        return pstr.format(**self.__dict__)

    def __repr__(self):
        """ I like default printing in ipython """
        return self.__str__()

    def __hash__(self):
        """
        Returns an integer which is uniquely determined by the children
        edges, that is the next possible characters in the graph. This
        will improve the speed of comparing two nodes when building a DAWG
        """
        return hash(''.join(sorted(self.children.keys())))


class Graph(object):
    """
    Edges have a char associated with them and point between two nodes
    Nodes are labeled by a unique int, contain a set of strings which are
    complete words
    """
    def __init__(self):
        self.nodes = [Node(0)]  # First node is empty string
        self.edges = defaultdict(set)

    @property
    def top(self):
        return self.nodes[0]

    @property
    def N(self):
        """ Number of nodes """
        return len(self.nodes)

    @property
    def E(self):
        """ Number of edges """
        return sum([len(self.edges[c]) for c in self.edges])

    def parselex(self, w):
        """
        Parse string w, adding its lexicon to trie. Any whitespace
        delimits words
        input:
            w : str, lexicon to add to graph
        """
        assert type(w) == str, "w must be str"
        loc = self.top
        path = ''
        for c in w:
            if c in loc.children:
                loc = loc[c]
                path += c
            elif c in string.whitespace:
                loc.strset.add(path)
                loc = self.top  # end of word, go to top
                path = ''
            else:  # Create edge, node
                loc = loc.addchild(c, Node(self.N+1))
                self.nodes.append(loc)
                self.edges[c].add((loc.parents[c], loc))
                path += c

    def _down(self, node, word):
        """ Traverse tree to find the node at which word lives """
        nextnode = node[word[0]]
        if not nextnode:  # word not in lexicon
            return None
        if len(word) > 1:
            return self._down(nextnode, word[1:])
        else:
            return nextnode

    def downto(self, word):
        """ Return node corresponding to word or None """
        return self._down(self.top, word)


if __name__ == "__main__":
    lex = "car cars cat cats do dog dogs done ear ears eat eats"
    G = Graph()
    G.parselex(lex)

