"""
graph.py

author: Colin Clement
date: 2016-01-14

Given a lexicon of words, DirectedGraph object computes the corresponding trie.
trie_to_dawg then dramatically trims this graph by merging subtrees, thus
combining word nodes with matching suffixes.
"""


from collections import defaultdict
from datetime import datetime


class Node(object):
    def __init__(self):
        """
        input : int, unique label for node
        """
        self.children = {}
        self.parent = None
        self.parentedge = None
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
        node.parentedge = edge
        return node

    def __getitem__(self, c):
        return self.children[c]

    def __str__(self):
        """ Make print(self) useful """
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
        edges, that is the next possible characters in the graph and whether
        this node corresponds to a word. This will improve the speed
        of comparing two subtrees when building a DAWG
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
            n = queue.pop()
            visited.update(set([n]))
            c = n.children.values()
            E += len(c)
            queue.update(set(c))
        return E

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
        delimits words. Also computes maxdepth to leaves for each node,
        a useful way to order the graph reduction below.
        input:
            w : str, lexicon to add to graph
        """
        assert type(w) == str, "w must be str"
        for word in w.split():
            N = len(word)
            loc = self.top
            loc.maxdepth = max(loc.maxdepth, N)
            for i, c in enumerate(word):
                if c in loc.children:
                    loc = loc[c]
                else:
                    loc = loc.addchild(c, Node())
                loc.maxdepth = max(loc.maxdepth, N - 1 - i)
            loc.strset.add(word)

    def downto(self, word):
        """ Return node corresponding to word or None """
        def down(self, node, word):
            """ Traverse tree to find the node at which word lives """
            nextnode = node[word[0]]
            if not nextnode:  # word not in lexicon
                return None
            if len(word) > 1:
                return down(nextnode, word[1:])
            else:
                return nextnode
        return down(self.top, word)


def trie_to_dawg(G):
        """
        Merges all identical subtrees in graph G to for a Directed
        Acyclic Word Graph (DAWG).
        The order in which nodes are merged is determined by the
        maxdepth to leaves, which leads to an optimally compressed
        structure.
        """
        depthdict = defaultdict(list)
        [depthdict[n.maxdepth].append(n) for n in G.nodes]
        for d in sorted(depthdict.keys()):
            hashdict = defaultdict(list)
            [hashdict[hash(n)].append(n) for n in depthdict[d]]
            for h in hashdict:
                nodes = hashdict[h]
                one = nodes[0]
                for n in nodes[1:]:  # The parents adopt the one child
                    n.parent.children[n.parentedge] = one
                    del n
                    # receiver.strset.update(n.strset)  # space expensive


if __name__ == "__main__":
    lex = "car cars cat cats do dog dogs done ear ears eat eats"
    # G = DirectedGraph()
    # G.parselex(lex)
    # trie_to_dawg(G)
    with open('../data/sowpods.txt', 'r') as infile:
        w = infile.read()

    G = DirectedGraph()

    start = datetime.now()
    G.parselex(w[:100000])
    print("Parsing took {}".format(datetime.now()-start))

    print("Nodes = {}, edges = {}".format(G.N, G.E))

    start = datetime.now()
    trie_to_dawg(G)
    print("Trimming to DAWG took {}".format(datetime.now()-start))

    print("Nodes = {}, edges = {}".format(G.N, G.E))
