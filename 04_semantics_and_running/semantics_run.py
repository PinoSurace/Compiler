#!/usr/bin/env python3
#

def run_program(tree, semdata):
  semdata.old_stacks = []
  semdata.stack = []
  eval_node(tree, semdata)

def eval_node(node, semdata):
  symtbl = semdata.symtbl
  if node.nodetype == 'program':
    # Copy and store current stack
    semdata.old_stacks.append(semdata.stack.copy())
    for i in node.children_codeitems:
      eval_node(i, semdata)
    # Restore stack
    #semdata.stack = semdata.old_stacks.pop()
    return None
  elif node.nodetype == 'var_definition':
    pass
  elif node.nodetype == 'func_definition':
    pass
  elif node.nodetype == 'formals':
    pass
  elif node.nodetype == 'statement_seq':
    pass
  elif node.nodetype == 'return_statement':
    pass
  elif node.nodetype == 'assignment':
    pass
  elif node.nodetype == 'binary_op':
    if node.value == '+':
      pass
    elif node.value == '-':
      pass
    elif node.value == '*':
      pass
    elif node.value == '/':
      pass
    elif node.value == '**':
      pass
    elif node.value == '.':
      pass
    elif node.value == '\'':
      pass
  elif node.nodetype == 'unary_op':
    pass
  elif node.nodetype == 'literal':
    pass
  elif node.nodetype == 'function_call':
    pass
  elif node.nodetype == 'comma_sep_expr':
    pass
  elif node.nodetype == 'if_statement':
    pass
  elif node.nodetype == 'while_statement':
    pass
  elif node.nodetype == 'do_while_statement':
    pass




  elif node.nodetype == 'push':
    semdata.stack.append(node.child_roman.value)
    return None
  elif node.nodetype == 'pop':
    semdata.stack.pop()
    return None
  elif node.nodetype == 'swap':
    semdata.stack[-1], semdata.stack[-2] = semdata.stack[-2], semdata.stack[-1]
    return None
  elif node.nodetype == 'complex-swap':
    idx1 = node.child_idx1.value
    idx2 = node.child_idx2.value
    semdata.stack[-idx1], semdata.stack[-idx2] = semdata.stack[-idx2], semdata.stack[-idx1]
    return None
  elif node.nodetype == 'add':
    semdata.stack.append(semdata.stack.pop() + semdata.stack.pop())
    return None
  elif node.nodetype == 'sub':
    semdata.stack.append(semdata.stack.pop() - semdata.stack.pop())
    return None
  elif node.nodetype == 'print':
    print(semdata.stack.pop())
    return None
