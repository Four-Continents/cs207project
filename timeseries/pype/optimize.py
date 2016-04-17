from .fgir import *
from .error import *

# Optimization pass interfaces

class Optimization(object):
  def visit(self, obj): pass

class FlowgraphOptimization(Optimization):
  '''Called on each flowgraph in a FGIR.

  May modify the flowgraph by adding or removing nodes (return a new Flowgraph).
  If you modify nodes, make sure inputs, outputs, and variables are all updated.
  May NOT add or remove flowgraphs.'''
  pass

class NodeOptimization(Optimization):
  '''Called on each node in a FGIR.

  May modify the node (return a new Node object, and it will be assigned).
  May NOT remove or add nodes (use a component pass).'''
  pass

class TopologicalNodeOptimization(NodeOptimization): pass

# Optimization pass implementations

class PrintIR(TopologicalNodeOptimization):
  'A simple "optimization" pass which can be used to debug topological sorting'
  def visit(self, node):
    print(str(node))

class AssignmentEllision(FlowgraphOptimization):
  '''Eliminates all assignment nodes.

  Assignment nodes are useful for the programmer to reuse the output of an
  expression multiple times, and the lowering transformation generates explicit
  flowgraph nodes for these expressions. However, they are not necessary for
  execution, as they simply forward their value. This removes them and connects
  their pre- and post-dependencies.'''

  def visit(self, flowgraph):
    for (nodeid, node) in flowgraph.nodes.items():
      if node.type == FGNodeType.assignment:
        # There can only be one input for an assignment expression
        # Retrieve the nodeid for the input and output node
        before = flowgraph.pre(nodeid)[0]
        after = flowgraph.post(nodeid)

        # For each output node of the assignment node, bypass the assignment node
        for a_nid in after:
          for i, n in enumerate(flowgraph.nodes[a_nid].inputs):
            if n == nodeid:
              flowgraph.nodes[a_nid].inputs[i] = before

        # Update the variable mapping table
        for (m_str, m_nid) in flowgraph.variables:
          if m_nid == nodeid:
            flowgraph.variables[m_str] = before
    return flowgraph


class DeadCodeElimination(FlowgraphOptimization):
  '''Eliminates unreachable expression statements.

  Statements which never affect any output are effectively useless, and we call
  these "dead code" blocks. This optimization removes any expressions which can
  be shown not to affect the output.
  NOTE: input statements *cannot* safely be removed, since doing so would change
  the call signature of the component. For example, it might seem that the input
  x could be removed:
    { component1 (input x y) (output y) }
  but imagine this component1 was in a file alongside this one:
    { component2 (input a b) (:= c (component a b)) (output c) }
  By removing x from component1, it could no longer accept two arguments. So in
  this instance, component1 will end up unmodified after DCE.'''

  def visit(self, flowgraph):
    req = {}

    # Start with each of the output nodes
    for nodeid in flowgraph.outputs:
      # Now DFS and mark each component as required
      stack = [nodeid]
      while stack:
        curNode = stack.pop()

        if curNode in req:
          continue
        else:
          req[curNode] = True

        for parent in flowgraph.nodes[nodeid].inputs:
          stack.append(parent)

    # For each node that was not marked as required, make sure it is not an input
    # node, and then delete it. Also delete variable references to deleted nodes.

    for nodeid in list(flowgraph.nodes.keys()):
      node = flowgraph.nodes[nodeid]
      if nodeid in req or node.type == FGNodeType.input:
          continue

      # Delete the node
      del flowgraph.nodes[nodeid]

    # Go through the graph and fix references to deleted nodes
    # Fix the input and output lists for each node
    for (nodeid, node) in flowgraph.nodes.items():
      updateInp, updateOut = [], []
      for i, n in enumerate(flowgraph.nodes[nodeid].inputs):
        if n in flowgraph.nodes:
            updateInp.append(n)

      flowgraph.nodes[nodeid].inputs = updateInp

      for i, n in enumerate(flowgraph.nodes[nodeid].outputs):
        if n in flowgraph.nodes:
            updateOut.append(n)

      flowgraph.nodes[nodeid].outputs = updateOut

    # Fix the variable mappings
    for var_str in list(flowgraph.variables.keys()):
      nodeid = flowgraph.variables[var_str]
      if nodeid not in flowgraph.nodes:
        del flowgraph.variables[var_str]

    return flowgraph
