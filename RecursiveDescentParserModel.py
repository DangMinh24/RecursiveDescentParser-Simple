import nltk
from nltk.tree import Tree
from nltk.grammar import Nonterminal

# This is a CFG grammar, where:
# Start Symbol : S
# Nonterminal : NP,VP,DT,NN,VB
# Terminal : "I", "a" ,"saw" ,"dog"
grammar=nltk.grammar.CFG.fromstring("""
    S -> NP VP
    NP -> DT NN | NN
    VP -> VB NP
    DT -> "a"
    NN -> "I" | "dog"
    VB -> "saw"
""")


class RDP():
    def __init__(self,grammar):
        self._grammar=grammar

    def parse(self,sentence):
        """This function try to initialize all essential parameters for parser:
        1/ Investigating Tree: A tree that is estimated to find the most appropriate tree
        2/ Remaining list
        3/ Frontier : List of locations of nodes that can be expanded(if Nonterminal) or can be matched/checked(if Terminal)
        """
        start=self._grammar.start().symbol()
        initial_tree=Tree(start,[])
        frontier=[()]
        remaining_list=list(sentence)
        return self._parse(remaining_text=remaining_list,tree=initial_tree,frontier=frontier)

    def _parse(self,remaining_text,tree,frontier):
        """Parsing function need to check all possibility that own investigating tree can have"""

        if len(remaining_text)==0 and len(frontier)==0:
            # Means that there are no nodes need to parsed and no nodes can be expanded or checked
            # => Our tree is completed
            # "Return" the tree
            yield tree
        elif len(frontier)==0:
            # Mean that it still have word need to parsed. However, there are no nodes can be expanded or checked
            # Cannot expanded and checked => This tree is failed
            pass
        elif isinstance(tree[frontier[0]],Tree):
            # Mean that it still have node can be expanded and checked
            # So there will be 2 possibility:
            # - If considered node is a nonterminal => can be expanded
            for result in self._expand(remaining_text,tree,frontier):
                yield result
        else:
            # - If considered node is a terminal => can be checked
            for result in self._match(remaining_text,tree,frontier):
                yield result

    def _expand(self,remaining_text,tree,frontier):
        """This function try to replace a considered node with a  appropriate tree if possible
        Example: my simple production is
        S -> NP VP
        NP -> DT NN

        I assume that my tree is : (S (NP )(VP ))
        I saw that NP can be expanded by DT NN
        => I try to make my tree become : (S (NP (DT )(NN ))(VP ))

        """

        productions=self._grammar.productions()

        for production in productions:
            lhs=production.lhs().symbol()
            if lhs==str(tree[frontier[0]].label()):
                subtree=self._production_to_tree(production)
                if frontier[0]==():
                    newtree=subtree
                else:
                    newtree=tree.copy()
                    newtree[frontier[0]]=subtree
                new_frontier=[frontier[0] +(i,) for i in range(len(production.rhs()))]

                for result in self._parse(remaining_text,newtree,new_frontier+frontier[1:]):
                    yield result

    def _match(self,remaining_text,tree,frontier):

        """This function try to check whether a terminal node is correct"""
        tree_leaves=tree[frontier[0]]
        if len(remaining_text)>0 and tree_leaves==remaining_text[0]:
            new_tree=tree.copy()
            new_tree[frontier[0]]=tree_leaves
            for result in self._parse(remaining_text[1:],new_tree,frontier[1:]):
                yield result


    def _production_to_tree(self,production):
        """This function try to convert a production to a Tree
            A tree has father node is Left Hand Side of the production,
            and children is a Right hand side of the production
            Example: S -> NP VP
            Left hand side :S
            Right hand side :NP, VP

            =>Return tree: (S (NP )(VP))
        """
        children=[]
        for elt in production.rhs():
            if isinstance(elt,Nonterminal):
                # Check if each RHS is a nonterminal
                children.append(Tree(elt,[]))
            else:
                #Check if each RHS is a terminal
                children.append(elt)
        return Tree(production.lhs(),children)


sentence="I saw a dog".split()

parser=RDP(grammar)

final_tree=parser.parse(sentence)

for i in final_tree:
    print(i)