from IPython.core.display import display_html, HTML, display_javascript, Javascript
import json
import os
import re
import lxml.etree as et

APP_HOME = os.environ['TREEDLIB_HOME']

class DepTree:
  def __init__(self, sentence_input, prune_root=True):
    """
    Initializes via a SentenceInput object, which is the output of the CoreNLP preprocessing
    pipeline.  Crucially, a SentenceInput object should contain the words of the sentence,
    and the dependency parse in CoNLL format (two arrays, dep_parents and dep_labels)
    """
    self.s = sentence_input
    self.tree = self._make_dep_tree(prune_root=prune_root)

  def _make_attrib(self, i):
    """
    Generate a dictionary of node attributes from a SentenceInput object's attribute arrays
    """
    if i < 0: 
      return {}
    return dict([(singular(k), v[i]) for k,v in filter(lambda x : type(x[1]) == list, self.s._asdict().iteritems()) if v[i] is not None])

  def _make_dep_tree(self, root=0, prune_root=False):
    node = {
      'id' : root,
      'attrib' : self._make_attrib(root-1),
      'children' : []
    }
    for i,d in enumerate(self.s.dep_parents):
      if d == root:
        node['children'].append(self._make_dep_tree(i+1))

    # If prune_root = True, remove leaf node children of the root node
    # In general these seem to be unimportant words (root parent is parser default?)
    # Also collapse root node if applicable after pruning
    if root == 0 and prune_root:
      node['children'] = filter(lambda c : len(c['children']) > 0, node['children'])
      if len(node['children']) == 1:
        node = node['children'][0]
    return node

  def to_xml(self, node=None):
    """
    Convert to XML representation, starting from self.tree
    """
    node = self.tree if node is None else node

    # attribs need to be str format for serialization
    attrib = list(node['attrib'].iteritems()) + [('id', node['id'])]
    root = et.Element('node', attrib=dict(map(lambda x : (x[0], str(x[1])), attrib)))

    # Recursively append children
    for c in node['children']:
      root.append(self.to_xml(c))
    return root

  def to_xml_str(self):
    return et.tostring(self.to_xml())

  def render_tree(self):
    """
    Renders d3 visualization of the d3 tree, for IPython notebook display
    Depends on html/js files in vis/ directory, which is assumed to be in same dir...
    """

    # HTML
    display_html(HTML(data=open('%s/src/vis/tree-chart.html' % APP_HOME).read()))

    # JS
    JS_LIBS = ["http://d3js.org/d3.v3.min.js"]
    js = "var root = " + json.dumps(self.tree) + "\n"
    js += open('%s/src/vis/tree-chart.js' % APP_HOME).read()
    display_javascript(Javascript(data=js, lib=JS_LIBS))


def singular(s):
  """Get singular form of word s (crudely)"""
  return re.sub(r'e?s$', '', s, flags=re.I)
