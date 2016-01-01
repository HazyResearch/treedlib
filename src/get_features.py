
# //node[@cand=true]

# get attribute of single node...
# POS tag of
# NER tag of
# lemma of

# siblings
# parent
# etc...

# path between


# BaseFeature objects specify *structure*
# as for attributes...

# * Should support flat & structured sentences

# Starting with: https://docs.python.org/2/library/xml.etree.elementtree.html

class BaseFeature:
  """
  Base feature template class, which must have:
  * A structural specifier, in XPath, specifying *where* in the input tree to look
  * List of attributes of the resulting nodes to look at; default None => all
  """
  def __init__(self):
    self.xpath = '//node'
    self.attrib = []

class Self(BaseFeature):
  """
  The feature comprising the set of nodes making up the mention
  """
  def __init__(self, cid, attrib=['lemma','pos']):
    self.label = 'SELF'
    self.xpath = ".//node[@cid='%s']" % str(cid)
    self.attrib = attrib

#class Siblings(BaseFeature):
#  """
#  Gets the siblings of the nodes making up the mentions
#  """

def gen_feats(f, root):
  """
  Simple un-optimized function which takes in a BaseFeature object and an xml object
  and returns a feature set
  """
  nodes = root.findall(f.xpath)

  # TODO: Should be option to take subsets of the node set (e.g. for n-grams)
  for a in f.attrib:
    yield '%s-%s[%s]' % (f.label, a, '_'.join(map(lambda node : node.get(a), nodes)))


  

