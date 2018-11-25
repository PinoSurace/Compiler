#!/usr/bin/env python3
#

#python main.py --treetype dot -f 04_test\01_prova.popl
from semantics_common import SemData ,SymbolData
import datetime

def run_program(tree, semdata):
  #semdata.old_stacks = []
  #semdata.stack = []
  #semdata = SemData()

  eval_node(tree, semdata)

def eval_node(node, semdata):
  symtbl = semdata.symtbl

  if node.nodetype == 'program':
    for i in node.children_codeitems:
      eval_node(i, semdata)
    return None

  elif node.nodetype == 'var_definition':
    symbol = SymbolData('variable', node)
    symbol.value = eval_node(node.child_value, semdata)
    symtbl[eval_node(node.child_var_name, semdata)] = symbol
    return None

  elif node.nodetype == 'func_definition':
    symbol = SymbolData('function', node)
    symbol.params = node.child_func_parameters
    symbol.body = node.child_func_body
    semdata.symtbl[eval_node(node.child_var_name, semdata)] = symbol

    return None
  elif node.nodetype == 'formals':
    list = []
    for i in node.children_args:
      list.append(eval_node(i, semdata))

    return list

  elif node.nodetype == 'statement_seq':
    for i in node.children_statements:
      eval_node(i, semdata)
    return None

  elif node.nodetype == 'return_statement':
    return eval_node(node.child_value, semdata)

  elif node.nodetype == 'assignment':
    symtbl[node.child_var.value].value = eval_node(node.child_value, semdata)

    return None

  elif node.nodetype == 'binary_op':
    return semdata.binary_op [node.value] (eval_node(node.child_idx1, semdata) , eval_node(node.child_idx2, semdata))


  elif node.nodetype == 'unary_op':
    return -node.child_atom.value
    return None

  elif node.nodetype == 'literal':
    return node.value

  elif node.nodetype == 'identifier':
    if node.value in symtbl:
      return symtbl[node.value].value
    return node.value

  elif node.nodetype == 'function_call':
    if node.child_func_name.value == 'Input':
      input_value = input()
      try:
        value = int(input_value)
        print(type(value))
        return value
      except ValueError:
        try:
          value = datetime.datetime.strptime( input_value, '%Y-%m-%d')
          print(type(value))
          return value
        except ValueError:
          print(type(input_value))
          return input_value



    elif node.child_func_name.value == 'Print':

      for i in node.child_args.children_expr:
        if i.nodetype == 'identifier':
          name = i.value
          print(str(symtbl[name].value))
        else:
          print(eval_node(i , semdata))
    else:
      func = symtbl[node.child_func_name.value]
      params = func.params
      body


    return None
  elif node.nodetype == 'comma_sep_expr':
    list = []
    for i in node.children_expr:
      list.append(eval_node(i, semdata))

    return list

  elif node.nodetype == 'if_statement':
    if(eval_node(node.child_condition, semdata)):
      eval_node(node.child_then, semdata)
    elif(node.child_else != None):
      eval_node(node.child_else, semdata)
    return None

  elif node.nodetype == 'while_statement':
    while (eval_node(node.child_condition, semdata)):
      eval_node(node.child_loop_body, semdata)
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