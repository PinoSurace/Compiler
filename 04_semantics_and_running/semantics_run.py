#!/usr/bin/env python3
#
from semantics_common import SemData ,SymbolData


def run_program(tree, semdata):
  #semdata.old_stacks = []
  #semdata.stack = []
  #semdata = SemData()

  eval_node(tree, semdata)

def eval_node(node, semdata):
  symtbl = semdata.symtbl
  if node.nodetype == 'program':
    # Copy and store current stack
    #semdata.old_stacks.append(semdata.stack.copy())
    for i in node.children_codeitems:
      eval_node(i, semdata)
    # Restore stack
    #semdata.stack = semdata.old_stacks.pop()
    return None
  elif node.nodetype == 'var_definition':
    symbol = SymbolData('variable', node)
    symbol.value = eval_node(node.child_value, semdata)
    semdata.symtbl[eval_node(node.child_var_name, semdata)] = symbol
    return None
  elif node.nodetype == 'func_definition':
    symbol = SymbolData('function', node)
    symbol.params = eval_node(node.child_func_parameters, semdata)
    symbol.body = eval_node(node.child_func_body, semdata)
    semdata.symtbl[eval_node(node.child_var_name), semdata] = symbol

    return None
  elif node.nodetype == 'formals':
    return None
  elif node.nodetype == 'statement_seq':
    for i in node.children_statements:
      eval_node(i, semdata)
    return None
  elif node.nodetype == 'return_statement':
    return None
  elif node.nodetype == 'assignment':
    semdata.symtbl[eval_node(node.child_var, semdata)].value = eval_node(node.child_value, semdata)
    return None
  elif node.nodetype == 'binary_op':

    return semdata.binary_op [node.value] (eval_node(node.child_idx1, semdata) , eval_node(node.child_idx2, semdata))


  elif node.nodetype == 'unary_op':
    return None
  elif node.nodetype == 'literal':
    return node.value

  elif node.nodetype == 'function_call':
    if node.child_func_name.value == 'Print':
      for i in eval_node(node.child_args, semdata):
        print(str(i), end=' ')

    return None
  elif node.nodetype == 'comma_sep_expr':
    list = []
    for i in node.children_expr:
      list.append(eval_node(i, semdata))

    return list

  elif node.nodetype == 'if_statement':
    return None
  elif node.nodetype == 'while_statement':
    return None
  elif node.nodetype == 'do_while_statement':
    return None




  #elif node.nodetype == 'push':
  #  semdata.stack.append(node.child_roman.value)
  #  return None
  #elif node.nodetype == 'pop':
  #  semdata.stack.pop()
  #  return None
  #elif node.nodetype == 'swap':
  #  semdata.stack[-1], semdata.stack[-2] = semdata.stack[-2], semdata.stack[-1]
  #  return None
  #elif node.nodetype == 'complex-swap':
  #  idx1 = node.child_idx1.value
  #  idx2 = node.child_idx2.value
  #  semdata.stack[-idx1], semdata.stack[-idx2] = semdata.stack[-idx2], semdata.stack[-idx1]
  #  return None
  #elif node.nodetype == 'add':
  #  semdata.stack.append(semdata.stack.pop() + semdata.stack.pop())
  #  return None
  #elif node.nodetype == 'sub':
  #  semdata.stack.append(semdata.stack.pop() - semdata.stack.pop())
  #  return None
  #elif node.nodetype == 'print':
  #  print(semdata.stack.pop())
  #  return None