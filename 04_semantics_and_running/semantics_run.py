#!/usr/bin/env python3
#

#python main.py --treetype dot -f 04_test\01_prova.popl
from semantics_common import SemData ,SymbolData
import datetime, calendar

def run_program(tree, semdata):

  #initialize the symtable and evaluation subnodes
  semdata.symtbl = dict()
  eval_node(tree, semdata)


#function that asks the input to the user and cast it depending on ita nature (int, data or string)
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



#functiong that goes through the tree nodes and execute the relative operations

def eval_node(node, semdata):
  symtbl = semdata.symtbl


  if node.nodetype == 'program':
    for i in node.children_codeitems:
      eval_node(i, semdata)
    return None

  #variable is added to the symbol table
  elif node.nodetype == 'var_definition':
    symbol = SymbolData('variable', node)
    symbol.value = eval_node(node.child_value, semdata)
    symtbl[eval_node(node.child_var_name, semdata)] = symbol
    return None

  #function information are added to the symbol table
  elif node.nodetype == 'func_definition':
    symbol = SymbolData('function', node)
    if(hasattr(node, 'child_func_params') ):
      symbol.params = node.child_func_params
    symbol.body = node.child_func_body
    semdata.symtbl[eval_node(node.child_func_name, semdata)] = symbol
    return None

  #return a list with the parameters of the function
  elif node.nodetype == 'formals':
    list = []
    for i in node.children_args:
      list.append(eval_node(i, semdata))
    return list

  #if the return value is != None then it means it is the return value of a function
  elif node.nodetype == 'statement_seq':
    for i in node.children_statements:
      out = eval_node(i, semdata)
      if out != None:
        return out
    return None

  #return the value of the subnode
  elif node.nodetype == 'return_statement':
    return eval_node(node.child_value, semdata)

  #if the variable has an attribute then it is a date variable so the respective attribute is
  #updated in the symboltable, otherwise just the variable value is updated in the symbol table
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

  #in case of "'" "+" and "-" operators some checks regarding the types of the involved subnodes are done
  # because in case of date types the behavior is different, in fact some opations with date are needed,
  # otherwise the normal operations are executed.
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

  #if the identifier is already in the symtable then its value is returned, otherwise just the name is returned
  elif node.nodetype == 'identifier':
    if node.value in symtbl:

      return symtbl[node.value].value
    else:
      return node.value

  #during function call is checked if it is one of the build in functions and in case they are executed.
  #Otherwise the function body of the function is executed after it is got from the symboltable.
  #in case of parameters, the arguments value are assigned to the variables name in the symbol table and
  # they are considered as normal variables.
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

  #return the list of arguments passed to the function
  elif node.nodetype == 'comma_sep_expr':
    list = []
    for i in node.children_expr:
      list.append(eval_node(i, semdata))
    return list

  #if the condition is true then the 'then' branch is executed otherwise
  #if there is an else branch it will be executed.
  elif node.nodetype == 'if_statement':
    if(eval_node(node.child_condition, semdata)):
      eval_node(node.child_then, semdata)
    elif(hasattr(node, 'child_else')):
      eval_node(node.child_else, semdata)
    return None

  # the loop body is executed while the condition is true
  elif node.nodetype == 'while_statement':
    while (eval_node(node.child_condition, semdata)):
      eval_node(node.child_loop_body, semdata)
    return None

  # the loop body is executed once and then it is executed
  # while the condition is true
  elif node.nodetype == 'do_while_statement':
    eval_node(node.child_loop_body, semdata)
    while (eval_node(node.child_condition, semdata)):
      eval_node(node.child_loop_body, semdata)
    return None

