"""
trie.py

author: Colin Clement
date: 2016-01-14

Given a lexicon of words, Trie object computes the corresponding trie.
TODO: Create function or class DAWG which merges suffixes in Trie to
get the DAWG of a lexicon.
"""


from collections import defaultdict
#import numpy as np

whitespace = '\t\n\x0b\x0c\r ' 


class Node(object):
    def __init__(self):
        """
        input : int, unique label for node
        """
        self.children = {}
        self.parent = None
        self.parentlabel = None
        self.strset = set([])  # list of complete words
        self.maxdepth = -1  # not yet calculated

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
        node.parent = self
        node.parentlabel = edge
        return node

    def __getitem__(self, c):
        return self.children[c]

    def __str__(self):
        """ Make print(self) useful """
        #pstr = "{label} \033[1;35;49m("  # pretty purple
        pstr = "\033[1;35;49m("  # pretty purple
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
        eow = str(1*bool(self.strset))
        return hash(eow + ''.join(sorted(self.children.keys())))


class DirectedGraph(object):
    """
    Edges have a char associated with them and point between two nodes
    Nodes are labeled by a unique int, contain a set of strings which are
    complete words
    """
    def __init__(self):
        self.top = Node()
        self.edges = defaultdict(set)
        self.maxdepth = -1

    @property
    def E(self):
        """ Number of edges """
        visited = set([self.top])
        c = self.top.children.values()
        E = len(c)
        queue = set(c)
        while queue:
            print(E, queue)
            n = queue.pop()
            visited.update(set([n]))
            c = n.children.values()
            E += len(c)
            queue.update(set(c))
        return E, visited

    @property
    def nodes(self):
        """ Return a list of all nodes """
        def children(node):
            c = node.children
            return [node] + reduce(lambda x, y: x+y, 
                                   [children(c[k]) for k in c], [])
        return set(children(self.top))  # only unique nodes!
    
    @property
    def N(self):
        """ Number of nodes """
        return len(self.nodes)

    @property
    def leaves(self):
        return set([n for n in self.nodes if not n.children])

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
        N = len(w)
        for i, c in enumerate(w):
            if c in loc.children:
                loc = loc[c]
                path += c
            elif c in whitespace:
                loc.strset.add(path)
                loc = self.top  # end of word, go to top
                path = ''
            else:  # Create edge, node
                loc = loc.addchild(c, Node())
                path += c
                if i == N - 1:  # in case last char isnt whitespace
                    loc.strset.add(path)
        #self.update_maxdepth()

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

    #TODO: Consider an iterative instead of recursive implementation
    def _count_maxdepths(self, node, depth = 0):
        if node.maxdepth < depth:  # Cut off search if longer path exists
            node.maxdepth = depth
            p = node.parent
            if p:
                return self._count_maxdepths(p, depth + 1)

    def update_maxdepth(self):
        """
        Calculates the maximum depth to leaves for each node.
        Useful for efficiently trimming Trie into a DAWG
        """
        for l in self.leaves:
            self._count_maxdepths(l)


def trie_to_dawg(G):
        """
        Merges all identical subtrees in graph G to for a Directed
        Acyclic Word Graph (DAWG).
        The order in which nodes are merged is determined by the
        maxdepth to leaves, which leads to an optimally compressed
        structure.
        """
        depthdict = defaultdict(list)
        for n in G.nodes:
            depthdict[n.maxdepth] += [n]
        for d in sorted(depthdict.keys()):
            hashdict = defaultdict(list)
            for n in depthdict[d]:
                hashdict[hash(n)] += [n]
            for h in hashdict:
                nodes = hashdict[h]
                receiver = nodes[0]
                for n in nodes[1:]:  # The parents adopt the receiver
                    n.parent.children[n.parentlabel] = receiver 
                    del n


if __name__ == "__main__":
    lex = "car cars cat cats do dog dogs done ear ears eat eats"
    G = DirectedGraph()
    G.parselex(lex)
    trie_to_dawg(G)

