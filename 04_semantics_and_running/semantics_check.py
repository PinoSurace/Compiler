#!/usr/bin/env python3
#

from semantics_common import visit_tree, SymbolData

# Define semantic check functions

# Stupid check, make sure all numbers are < 10
def check_literal_size(node, semdata):
  if node.value >= 10:
    return "Literal "+str(node.value)+" too large!"


# Check that the stack size remains acceptable within operations

def increment_stack_size(node, semdata):
  '''One more push done to stack'''
  semdata.stack_size = semdata.stack_size + 1

def decrement_stack_size(node, semdata):
  '''One more drop done to stack'''
  semdata.stack_size = semdata.stack_size - 1

def check_stack_print(node, semdata):
  '''Check that stack is not empty, remove one'''
  if semdata.stack_size == 0:
    return "Nothing in stack!"
  decrement_stack_size(node, semdata)

def check_stack_swap(node, semdata):
  '''Check that at least two items are in stack'''
  if semdata.stack_size < 2:
    return "Too few items in stack for swap!"

def check_stack_complex_swap(node, semdata):
  '''Check that enough items are in stack'''
  if semdata.stack_size < node.child_idx1.value or semdata.stack_size < node.child_idx2.value:
    return "Too few items in stack for complex swap!"

def check_stack_add_sub(node, semdata):
  '''Check that at least two items are in stack, remove one'''
  if semdata.stack_size < 2:
    return "Too few items in stack for add/sub!"
  decrement_stack_size(node, semdata)

def check_stack_program_before(node, semdata):
  '''Store old stack size when embedded program starts'''
  semdata.old_stack_sizes.append(semdata.stack_size)

def check_stack_program_after(node, semdata):
  '''Restore old stack size when embedded program ends'''
  semdata.stack_size = semdata.old_stack_sizes.pop()


# Dictionaries that define functions to call when visiting nodes

check_literals = {'literal': (check_literal_size, None)}

check_stack_size = {'push': (increment_stack_size, None),
                    'pop': (decrement_stack_size, None),
                    'print': (check_stack_print, None),
                    'swap': (check_stack_swap, None),
                    'complex-swap': (check_stack_complex_swap, None),
                    'add': (check_stack_add_sub, None),
                    'sub': (check_stack_add_sub, None),
                    'program': (check_stack_program_before, check_stack_program_after)}

def check_semantics(tree, semdata):
  '''run all semantic checks'''
  visit_tree(tree, check_literals, semdata)
  semdata.stack_size = 0 # Initially stack is empty
  semdata.old_stack_sizes = [] # Initially no old stacks
  visit_tree(tree, check_stack_size, semdata)
