#!/usr/bin/env python3
#

#python main.py --treetype dot -f 04_test\01_prova.popl
from semantics_common import SemData ,SymbolData
import datetime, calendar

def run_program(tree, semdata):
  #semdata.old_stacks = []
  #semdata.stack = []
  semdata.symtbl = dict()

  eval_node(tree, semdata)

def build_in_input():
  input_value = input()
  try:
    value = int(input_value)
    print(type(value))
    return value
  except ValueError:
    try:
      value = datetime.datetime.strptime(input_value, '%Y-%m-%d')

      return value
    except ValueError:
      print(type(input_value))
      return input_value





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
    if(hasattr(node, 'child_func_params') ):
      symbol.params = node.child_func_params
    symbol.body = node.child_func_body
    semdata.symtbl[eval_node(node.child_func_name, semdata)] = symbol
    return None

  elif node.nodetype == 'formals':
    list = []
    for i in node.children_args:
      list.append(eval_node(i, semdata))
    return list

  elif node.nodetype == 'statement_seq':
    for i in node.children_statements:
      out = eval_node(i, semdata)
      if out != None:
        return out
    return None


  elif node.nodetype == 'return_statement':
    return eval_node(node.child_value, semdata)

  elif node.nodetype == 'assignment':
    res = eval_node(node.child_value, semdata)
    if (node.child_var.nodetype == 'binary_op'):
      var = node.child_var.child_idx1.value
      attr = node.child_var.child_idx2.value
      if attr == 'day':
        symtbl[var].value = datetime.date(symtbl[var].value.year, symtbl[var].value.month, res)
      elif attr == 'month':
        symtbl[var].value = datetime.date(symtbl[var].value.year, res, symtbl[var].value.day)
      else:
        symtbl[var].value = datetime.date(res, symtbl[var].value.month, symtbl[var].value.day)

    else:
      symtbl[node.child_var.value].value = res
    return None

  elif node.nodetype == 'binary_op':
    node1 = node.child_idx1
    node2 = node.child_idx2

    if(node.value == "'"):
      var = eval_node(node1, semdata)
      attr = node.child_idx2.value
      if attr == 'day':
        return var.day
      elif attr ==  'month':
        return var.month
      elif attr ==  'year':
        return var.year
      elif attr == 'isLeapYear?':
        return calendar.isleap(var.year)
      elif attr == 'isWorkday?':
        return calendar.weekday(var.year, var.month, var.day) in range(0,5)

    elif node.value == '+':
      if isinstance(eval_node(node1, semdata), datetime.date) :
        return eval_node(node1, semdata) + datetime.timedelta(days=eval_node(node2, semdata))
      #elif isinstance(eval_node(node2, semdata), datetime.date) :
      #  return eval_node(node2, semdata) + datetime.timedelta(days=eval_node(node1, semdata))
      else:
        return semdata.binary_op[node.value](eval_node(node1, semdata), eval_node(node2, semdata))
    elif node.value == '-':
      if isinstance(eval_node(node1, semdata), datetime.date):
        return (eval_node(node1, semdata) - eval_node(node2, semdata)).days
      else:
        return semdata.binary_op[node.value](eval_node(node1, semdata), eval_node(node2, semdata))
    else:
      return semdata.binary_op[node.value](eval_node(node1, semdata), eval_node(node2, semdata))




  elif node.nodetype == 'unary_op':
    return -node.child_atom.value


  elif node.nodetype == 'literal':

    return node.value

  elif node.nodetype == 'identifier':
    if node.value in symtbl:

      return symtbl[node.value].value
    else:
      return node.value

  elif node.nodetype == 'function_call':
    if node.child_func_name.value == 'Input':
      return build_in_input()
    elif node.child_func_name.value == 'Print':
      if (hasattr(node, 'child_args')):
        for i in node.child_args.children_expr:
          print(str(eval_node(i, semdata)))
      else:
        print()
        #if i.nodetype == 'identifier':
        #  name = i.value
        #  print(str(symtbl[name].value))
        #else:
        #  print(str(eval_node(i , semdata)))
    else:
      func = symtbl[node.child_func_name.value]
      if (hasattr(node, 'child_args')):
        params = eval_node(func.params, semdata)
        args = eval_node(node.child_args, semdata)
        for i in range(0, len(params)):
          symbol = SymbolData('variable', node)
          symbol.value = args[i]
          symtbl[params[i]] = symbol
      out = eval_node(func.body, semdata)
      return out
    return None


  elif node.nodetype == 'comma_sep_expr':
    list = []
    for i in node.children_expr:
      list.append(eval_node(i, semdata))
    return list

  elif node.nodetype == 'if_statement':
    if(eval_node(node.child_condition, semdata)):
      eval_node(node.child_then, semdata)
    elif(hasattr(node, 'child_else')):
      eval_node(node.child_else, semdata)
    return None

  elif node.nodetype == 'while_statement':
    while (eval_node(node.child_condition, semdata)):
      eval_node(node.child_loop_body, semdata)
    return None

  elif node.nodetype == 'do_while_statement':
    eval_node(node.child_loop_body, semdata)
    while (eval_node(node.child_condition, semdata)):
      eval_node(node.child_loop_body, semdata)
    return None

