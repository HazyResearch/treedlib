
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
  Base class which emits an XPath pattern
  """
  def __init__(self):
    self.xpath = '//node'


class Self(BaseFeature):
  """
  The feature comprising the set of nodes making up the mention
  """
  def __init__(self, cid=1):
    self.xpath = '//node[@cid=%s]' % cid


class Siblings(BaseFeature):
  """
  Gets the siblings of the nodes making up the mentions
  """

