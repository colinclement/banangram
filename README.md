Alemi's suggestion:
    Just do a depth first search of playable words and locs
    Use a DAWG (directed, acyclic graph)
    And for more options heuristically push the search to 'words' that themselves are subwords of more worda
    
GADDAG is likely a faster data structure, but takes up more space
