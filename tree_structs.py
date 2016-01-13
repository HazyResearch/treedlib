from IPython.core.display import display_html, HTML, display_javascript, Javascript
import json
import os
import re
import lxml.etree as et

class Tree:
  def __init__(self, raw):
    """Calls subroutines to parse input"""
    self.raw = raw
    self.js = self._make_js()
    self.root = self._make_xml()

  def to_xml_str(self):
    return et.tostring(self.root)

  def render_tree(self):
    """
    Renders d3 visualization of the d3 tree, for IPython notebook display
    Depends on html/js files in vis/ directory, which is assumed to be in same dir...
    """
    # HTML
    display_html(HTML(data=open('vis/tree-chart.html').read()))

    # JS
    JS_LIBS = ["http://d3js.org/d3.v3.min.js"]
    js = "var root = " + json.dumps(self.js) + "\n"
    js += open('vis/tree-chart.js').read()
    display_javascript(Javascript(data=js, lib=JS_LIBS))


class DepTree(Tree):
  """
  Initializes via a SentenceInput object, which is the output of the CoreNLP preprocessing
  pipeline.  Crucially, a SentenceInput object should contain the words of the sentence,
  and the dependency parse in CoNLL format (two arrays, dep_parents and dep_labels)
  """

  def _make_attrib(self, i):
    """
    Generate a dictionary of node attributes from a SentenceInput object's attribute arrays
    """
    if i < 0: 
      return {}
    return dict([(singular(k), v[i]) for k,v in filter(lambda x : type(x[1]) == list, self.raw._asdict().iteritems()) if v[i] is not None])

  def _make_js(self, root=0, prune_root=True):
    node = {
      'id' : root,
      'attrib' : self._make_attrib(root-1),
      'children' : []
    }
    for i,d in enumerate(self.raw.dep_parents):
      if d == root:
        node['children'].append(self._make_js(i+1))

    # If prune_root = True, remove leaf node children of the root node
    # In general these seem to be unimportant words (root parent is parser default?)
    # Also collapse root node if applicable after pruning
    if root == 0 and prune_root:
      node['children'] = filter(lambda c : len(c['children']) > 0, node['children'])
      if len(node['children']) == 1:
        node = node['children'][0]
    return node

  def _make_xml(self, node=None):
    """
    Convert to XML representation, starting from js
    """
    node = self.js if node is None else node

    # attribs need to be str format for serialization
    attrib = list(node['attrib'].iteritems()) + [('id', node['id'])]
    root = et.Element('node', attrib=dict(map(lambda x : (x[0], str(x[1])), attrib)))

    # Recursively append children
    for c in node['children']:
      root.append(self._make_xml(c))
    return root


def singular(s):
  """Get singular form of word s (crudely)"""
  return re.sub(r'e?s$', '', s, flags=re.I)


class TableTree(Tree):
  """Initializes via HTML table as text string input"""

  def _make_xml(self, node=None):
    """
    Take the XML and convert each word in leaf nodes into its own node
    Note: Ideally this text would be run through CoreNLP?
    """
    node = et.fromstring(re.sub(r'>\s+<', '><', self.raw.strip())) if node is None else node

    # Split text into Token nodes
    # NOTE: very basic token splitting here... (to run through CoreNLP?)
    if node.text is not None:
      print node.text
      for tok in re.split(r'\s+', node.text):
        node.append(et.Element('token', attrib={'word':tok}))
    
    # Recursively append children
    for c in node:
      node.append(self._make_xml(c))
    return node

  def _make_js(self, node=None):
    return None
