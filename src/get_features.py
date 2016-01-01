from itertools import chain
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
# Should we emit both by default?  Or consider them totally different inputs...?

# Starting with: https://docs.python.org/2/library/xml.etree.elementtree.html

class BaseFeature:
  """
  Base feature template class, which must have:
  * A structural specifier, in XPath, specifying *where* in the input tree to look
  * List of attributes of the resulting nodes to look at; default None => all
  """
  def __init__(self):
    self.label = None
    self.xpath = '//node'
    self.attrib = []
    self.subsets = None


class Self(BaseFeature):
  """
  The feature comprising the set of nodes making up the mention
  """
  def __init__(self, cid, attrib=['lemma','pos']):
    self.label = 'SELF'
    self.xpath = ".//node[@cid='%s']" % str(cid)
    self.attrib = attrib
    self.subsets = 100  # Take n-grams for *all* n...


#class Siblings(BaseFeature):
#  """
#  Gets the siblings of the nodes making up the mentions
#  """


def gen_feats(f, root):
  """
  Simple un-optimized function which takes in a BaseFeature object and an xml object
  and returns a feature set
  """
  # Optionally take subsets of the node set (e.g. n-grams) 
  res = root.findall(f.xpath)
  if f.subsets is None:
    node_sets = [res]
  else:
    node_sets = chain.from_iterable([[res[s:s+l] for s in range(len(res)-l+1)] for l in range(1, min(f.subsets, len(res)))])

  # Generate the features
  for nodes in node_sets:
    for a in f.attrib:
      yield '%s-%s[%s]' % (f.label, a, '_'.join(map(lambda node : node.get(a), nodes)))
