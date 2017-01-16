The rules are simple:
    Randomly collect N letter tiles
    Use all N letters to make a Scrabble-like grid of words.
    If no solution exists, grab more tiles
The Question: for N randomly grabbed letters, how likely is it that a solution exist?
Sub-questions: 
    1) As N increases, how does likelihood of solution change? Where does the change occur?
    2) How does the behavior depend on the distribution of letters grabbable?

Alemi's suggestion:
    Just do a depth first search of playable words and locs
    Use a DAWG (directed, acyclic graph)
    And for more options heuristically push the search to 'words' that themselves are subwords of more worda
    
GADDAG is likely a faster data structure, but takes up more space, also built to solve board constraints not present in Bangrams.


## Sources:
  * Appel and Jacobsen (1986) "The World's Fastest Scrabble Program"
  * http://stevehanov.ca/blog/index.php?id=115
