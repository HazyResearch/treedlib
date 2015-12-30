from IPython.core.display import display_html, HTML, display_javascript, Javascript
import json
import os

APP_HOME = os.environ['TREEDLIB_HOME']

class DepTree:
  def __init__(self, sentence_input, root):
    """
    Initializes via a SentenceInput object, which is the output of the CoreNLP preprocessing
    pipeline.  Crucially, a SentenceInput object should contain the words of the sentence,
    and the dependency parse in CoNLL format (two arrays, dep_parents and dep_labels)
    """
    self.s = sentence_input
    self.tree = self._make_dep_tree(root)

  def _make_dep_tree(self, root):
    node = {'id' : root, 'text' : self.s.words[root-1], 'children' : []}
    for i,d in enumerate(self.s.dep_parents):
      if d == root:
        node['children'].append(self._make_dep_tree(i+1))
    return node

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
