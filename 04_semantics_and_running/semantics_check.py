#!/usr/bin/env python3
#

from semantics_common import visit_tree, SymbolData

# Define semantic check functions


#check if the variable is already in the symboltable and in case give an error,
#otherwise the variable is added to the symboltable
def check_var_definition(node, semdata):
  name = node.child_var_name.value
  if name in semdata.symtbl:
    return "Variable " + str(name) + " is already defined"
  else:
    semdata.symtbl[name] = node


# check that if there is an attibute then it is between those defined for the date types, otherwise gives an error.
# if the variable is not in the symboltable then gives an error.
def check_var_assignment(node, semdata):
  if node.child_var.nodetype == 'binary_op' :
    name = node.child_var.child_idx1.value
    if (name not in semdata.symtbl):
      return "Variable " + str(name) + "should be defined before use"
    attr = node.child_var.child_idx2.value
    if attr not in ['day', 'month', 'year']:
      return "Attribute "+ str(attr) + " is not valid."
  else:
    name = node.child_var.value
    if (name not in semdata.symtbl):
      return "Variable " + str(name) + "should be defined before use"


# checks if the function is already in the symboltable and in case gives and error,
# otherwise the function is added to the symboltable. after that the parameters are checked and if
# they are already defined, an error is given, otherwise they are added to the symboltable as normal variables.
def check_function_definition(node, semdata):
  name = node.child_func_name.value
  if name in semdata.symtbl:
    return "Function " + str(name) + "is already defined"
  else:
    semdata.symtbl[name] = {}

    if (hasattr(node, 'child_func_params')):
      params = []
      for i in node.child_func_params.children_args:
        param = i.value
        if param in semdata.symtbl:
          return "You have already defined a variable with this name "+ param
        semdata.symtbl[param] = ''
        params.append(param)
      semdata.symtbl[name]['params'] = params
      #setattr(semdata.funcs[name], 'params', params)

# checks if the function has been defined before and in case it has not then an error is returned,
# moreover there is a check on the number of arguments passed that should be the same of the
# number of parameters defined in the definition, otherwise an error is given.
def check_function_call(node, semdata):
  built_in = ['Input', 'Print']
  name = node.child_func_name.value
  if name not in built_in:
    if name not in semdata.symtbl.keys():
      return "Function " + str(name) + "should be defined before use"
    elif len(semdata.symtbl[name]['params']) != len (node.child_args.children_expr):
      return "Number of arguments is wrong in the function "+ name


# check if the attribute of the variable is one of those defined, otherwise gives an error.
# checks that sting and integer are not in the same expression, otherwise it gives an error.
def check_binary_op(node, semdata):
  if node.value == "'":
    attr = node.child_idx2.value
    if attr not in ['day', 'month', 'year', 'isLeapYear?', 'isWorkday?']:
      return "Attribute " + str(attr) + " is not valid."
  elif node.child_idx1.nodetype == 'literal' and node.child_idx2.nodetype == 'literal':
    if (isinstance(node.child_idx1.value, int) and isinstance(node.child_idx2.value, str)) or \
            (isinstance(node.child_idx2.value, int) and isinstance(node.child_idx1.value, str)):
      return "Integer and string cannot be used in the same expression: (" +str(node.child_idx1.value) \
              + str(node.value)+ str(node.child_idx2.value)+")"



# checks that each identifier (functions and variables)
# are defined before the use in a more general way, so that
# all the cases are covered.
def check_identifier(node, semdata):
  built_in = ['Input', 'Print']
  if node.value not in semdata.symtbl and node.value not in built_in:
    return "'"+ str(node.value) + "'"+ " should be defined before use."





# Dictionaries that define functions to call when visiting nodes

check_var_func = {'var_definition': (check_var_definition, None),
                  'func_definition': (check_function_definition, None),
                  'assignment': (check_var_assignment, None),
                  'function_call': (check_function_call, None),
                  'binary_op': (check_binary_op, None),
                  'identifier': (check_identifier, None)}



def check_semantics(tree, semdata):
  '''run all semantic checks'''

  semdata.symtbl  = dict()
  visit_tree(tree, check_var_func, semdata)

  #visit_tree(tree, check_literals, semdata)
  #semdata.stack_size = 0 # Initially stack is empty
  #semdata.old_stack_sizes = [] # Initially no old stacks
  #visit_tree(tree, check_stack_size, semdata)
