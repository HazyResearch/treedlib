from itertools import chain
import re

# NodeSet objects are functions f : P(T) -> P(T)
# ---------------
# They are applied compositionally and lazily, by constructing an xpath query
# We use these to get the *subtree* or set of nodes that our indicicator features will
# operate over

class NodeSet:
  """Given an input tree T, a NodeSet object is a function f : P(T) -> P(T)"""
  def __init__(self):
    self.label = 'NODE_SET'
    self.xpath = '//node'

  def __repr__(self):
    return '<%s, xpath="%s">' % (self.label, self.xpath)


def Mention(NodeSet):
  """Gets candidate mention nodes"""
  def __init__(self, ns, cid):
    self.label = 'MENTION'
    self.xpath = "//node[@cid='%s']" % str(cid)


def Keyword(NodeSet):
  """Gets keyword nodes"""
  def __init__(self, keyword, ns=None):
    self.label = 'KEYWORD' + '-IN-%s' % ns.label if ns else ''
    self.xpath = ns.xpath if ns else '//node'
    self.xpath += "[@word='%s']" % keyword


def Left(NodeSet):
  """Gets preceding siblings"""
  def __init__(self, ns):
    self.label = 'LEFT-OF-%s' % ns.label
    self.xpath = ns.xpath + '/preceding-sibling::node'


def Right(NodeSet):
  """Gets following siblings"""
  def __init__(self, ns):
    self.label = 'RIGHT-OF-%s' % ns.label
    self.xpath = ns.xpath + '/following-sibling::node'


def Parents(NodeSet):
  """Gets parents of the node set"""
  def __init__(self, ns):
    self.label = 'PARENTS-OF-%s' $ ns.label
    self.xpath = ns.xpath + '/ancestor::node'


class Between(NodeSet):
  """
  Gets the nodes between two node sets
  Note: this requires some ugly xpath... could change this to non-xpath method
  """
  def __init__(self, ns1, ns2):
    self.label = 'BETWEEN-%s-and-%s' % (ns1.label, ns2.label)
    self.xpath = "{0}/ancestor-or-self::node[count(. | {1}/ancestor-or-self::node) = count({1}/ancestor-or-self::node)][1]/descendant-or-self::node[ .{0} | .{1}]".format(ns1.xpath, ns2.xpath)


# Indicator objects are functions f : P(T) -> {0,1}^F
# ---------------
# Indicator objects take a NodeSet, an attibute or attributes, and apply some indicator
# function to the specified attributes of the NodeSet

class Indicator:
  """Given an input node set, an Indicator object is a function g : P(T) -> {0,1}^F"""
  def __init__(self, ns, attrib):
    self.ns = ns
    self.attrib = attrib

  def apply(self, root):
    for feat in self._get_features(root.xpath(self.ns.xpath + '/@' + self.attrib)):
      yield '%s:%s[%s]' % (self.attrib.upper(), self.ns.label, feat)

  def _get_features(self, res):
    """
    Given a result set of attribute values, return a set of strings representing the features
    This should be the default method to replace for Indicator objects
    """
    return ['_'.join(res)]

  def __repr__(self):
    return '<%s:%s:%s, xpath="%s">' % (self.__name__, self.attrib, self.ns.label, self.ns.xpath)


class NGrams(Indicator):
  """Return indicator features over the ngrams of a result set"""
  def __init__(self, ns, attrib, ng):
    self.ns = ns
    self.attrib = attrib
    if (type(ng) == int and ng > 0) or (type(ng) in [list, tuple] and ng[0] > 0):
      self.ng = ng
    else:
      raise ValueError("Improper ngram range: %s" % ng)

  def _get_features(self, res):
    r = range(min(len(res), ng)) if type(ng) == int else range(ng[0]-1, min(len(res), ng[1]))
    return chain.from_iterable(['_'.join(res[s:s+l+1]) for s in range(len(res)-l)] for l in r)
    

class Regexp(Indicator):
  """
  Return indicator features defined by regular expressions applied to the 
  concatenation of the result set strings
  """
  def __init__(self, ns, attrib, rgx, rgx_label):
    self.ns = ns
    self.attrib = attrib
    self.rgx = rgx
    self.rgx_label = rgx_label

  # TODO: Sort by word order...
  def _get_features(self, res):
    return 'RGX:%s=%s' % (self.rgx_label, re.search(self.rgx, self.sep.join(res)) is not None)



# TODO: Handle subsets where...?

# TODO: Handle combinations, unions, intersections / conjunctions, sets, etc...?

