from templates import *
import lxml.etree as et

BASIC_ATTRIBS = ['word', 'lemma', 'pos', 'ner']
BASIC_ATTRIBS_REL = ['word', 'lemma', 'pos', 'ner', 'dep_label']


def apply_templates(temps, root, cids):
  """Applies a set of templates to root, relative to candidates cids"""
  # Ensure that root is parsed
  if type(root) == str:
    root = et.fromstring(root)

  # Apply the templates
  for temp in temps:
    for feat in temp.apply(root, cids, 'word_idx'):
      yield feat
  

def get_relation_features(root, e1_idxs, e2_idxs, keywords=[]):
  """
  Get relation features given an XMLTree root and the word indexes of the two entities
  """
  temps = []
  btwn = Between(Mention(0), Mention(1))

  # The full path between
  for a in BASIC_ATTRIBS_REL:
    temps.append(Indicator(btwn, a))

  # The tri-grams between
  for a in BASIC_ATTRIBS_REL:
    temps.append(Ngrams(btwn, a, (2,3)))

  # The VBs between
  temps.append(Ngrams(Filter(btwn, 'pos', 'VB'), 'lemma', [1,3]))

  # The window features for each of the mentions
  for m in [0,1]:
    for a in BASIC_ATTRIBS:
      temps.append(RightNgrams(RightSiblings(Mention(m)), a))
      temps.append(LeftNgrams(LeftSiblings(Mention(m)), a))
      #temps += [r, l, Combinations(r, l)]
  
  return apply_templates(temps, root, [e1_idxs, e2_idxs])


def get_generic_mention_features(root, cid, keywords):
  """
  Get the generic mention features as listed in the DDLib documentation
  http://deepdive.stanford.edu/doc/basics/gen_feats.html
  """
  temps = []

  # The basic attribs of the mention candidate span
  temps += [Indicator(Mention(), a) for a in BASIC_ATTRIBS]

  # Whether the mention candidate starts with a capital letter
  temps.append(Regexp(Mention(), 'word', r'^[A-Z].*$', 'STARTS_W_CAPITAL'))

  # The window features
  for a in BASIC_ATTRIBS:
    r = RightNgrams(RightSiblings(Mention()), a)
    l = LeftNgrams(LeftSiblings(Mention()), a)
    temps += [r, l, Combinations(r, l)]

  # Keyword in mention, in sentence; dep path labels + edges between kw and mention
  for kw in keywords:
    temps.append(Indicator(Keyword(kw, Mention()), 'word'))
    temps.append(Indicator(Keyword(kw), 'word'))
    for a in ['dep_label', 'lemma', 'dep_label,lemma']:
      temps.append(Indicator(Between(Mention(), Keyword(kw)), a))

  # Apply the templates
  for temp in temps:
    for feat in temp.apply(root, [cid]):
      yield feat
