#!/usr/bin/env python3
#

# Generic useful stuff for semantic analysis and interpretation/code generation

from tree_print import get_childvars


# A class for collecting data needed during semantic analysis etc.
# By default contains the symbol table

class SemData:
    def __init__(self):
        self.symtbl = dict()
        self.errors = []  # List for possible semantic errors


# An element in the symbol table, by default containing symbols type
# and reference to its definition in the syntax tree

class SymbolData:
    def __init__(self, symtype, node):
        self.symtype = symtype
        self.node = node


# The function is given the root of the tree
def visit_tree(node, func_dict, semdata=None):
    '''A generic visitor (which uses tree_print.get_childvars)

       Parameters:
       node: root of the (sub)tree to be traversed
       func_dict: a dictionary from nodetype to a pair of functions.
                  When a node is found, its nodetype is used to get the two
                  functions. The first function (before_func) is first called,
                  then all the childrens of the node are visited recursively, then
                  the second function (after_func) is called.
       semdata: optional data that is passed to all functions'''

    before_func, after_func = func_dict.get(node.nodetype, (None, None))

    if before_func:
        err = before_func(node, semdata)
        if not err is None:
            semdata.errors.append(err)

    children = get_childvars(node)

    for name, child in children:
        if child:
            visit_tree(child, func_dict, semdata)

    if after_func:
        after_func(node, semdata)
        if not err is None:
            semdata.errors.append(err)
