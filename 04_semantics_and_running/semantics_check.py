#!/usr/bin/env python3
#

from semantics_common import visit_tree, SymbolData

# Define semantic check functions


#
def check_var_definition(node, semdata):
  name = node.child_var_name.value
  if name in semdata.vars:
    return "Variable " + str(name) + "is already defined"
  else:
    semdata.vars.append(name)

def check_var_assignment(node, semdata):
  if node.child_var.nodetype == 'binary_op' :
    name = node.child_var.child_idx1.value
    attr = node.child_var.child_idx2.value
    if attr not in ['day', 'month', 'year']:
      return "Attribute "+ str(attr) + " is not valid."
  else:
    name = node.child_var.value

  if (name not in semdata.vars):
    return "Variable " + str(name) + "should be defined before use"

def check_function_definition(node, semdata):
  name = node.child_func_name.value
  if name in semdata.funcs:
    return "Function " + str(name) + "is already defined"
  else:
    semdata.funcs[name] = {}


    if (hasattr(node, 'child_func_params')):
      params = []
      for i in node.child_func_params.children_args:
        param = i.value
        if param in semdata.vars:
          return "You have already defined a variable with this name "+ param
        params.append(param)
      semdata.funcs[name]['params'] = params
      #setattr(semdata.funcs[name], 'params', params)

def check_function_call(node, semdata):
  build_in = ['Input', 'Print']
  name = node.child_func_name.value
  if name not in build_in:
    if name not in semdata.funcs.keys():
      return "Function " + str(name) + "should be defined before use"
    elif len(semdata.funcs[name]['params']) != len (node.child_args.children_expr):
      return "Number of arguments is wrong in the function "+ name

def check_binary_op(node, semdata):
  if node.value == "'":
    attr = node.child_idx2.value
    if attr not in ['day', 'month', 'year', 'isLeapYear?', 'isWorkday?']:
      return "Attribute " + str(attr) + " is not valid."










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

check_var_func = {'var_definition': (check_var_definition, None),
                  'func_definition': (check_function_definition, None),
                  'assignment': (check_var_assignment, None),
                  'function_call': (check_function_call, None),
                  'binary_op': (check_binary_op, None)}

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
  semdata.vars = []
  semdata.funcs = {}
  visit_tree(tree, check_var_func, semdata)

  #visit_tree(tree, check_literals, semdata)
  #semdata.stack_size = 0 # Initially stack is empty
  #semdata.old_stack_sizes = [] # Initially no old stacks
  #visit_tree(tree, check_stack_size, semdata)
