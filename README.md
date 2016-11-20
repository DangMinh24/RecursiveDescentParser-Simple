# RecursiveDescentParser-Simple

Parsing function use 3 parameter to determine parsing process:

1/ Remain list: To see how many words left need to parsing (also show how many words have been parsed)

2/ Investigating Tree: A tree that we consider to see whether it is a right one

3/ Frontier : list of locations in "Investigating tree" that can be expanded( if Node symbol still be a Nonterminal ), or
can be matched( if Node symbol is a Terminal )



Considered Node will be a first node that can be expanded or checked. Means considered node is a node whose location is a first
element in frontier. Or considered_node=Investigating_Tree[Frontier[0]]

Parsing will check a considered node with all possibility:

1/ When Investigating tree is completed

2/ When Investigating tree isn't finished:

    a/ If consider node is a terminal -> Check whether it is correct

    b/ If consider node is a nonterminal -> Expand the node


This code is similar to nltk.RecursiveDescentParser (without trace). However, my goal to understand the code rather than
a magical tool box

