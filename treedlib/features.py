from templates import *
import lxml.etree as et

BASIC_ATTRIBS = ['word', 'lemma', 'pos', 'ner']
BASIC_ATTRIBS_REL = ['word', 'lemma', 'pos', 'ner', 'dep_label']

m0 = Mention(0)
m1 = Mention(1)
btwn = Between(m0, m1)

"""
Args: root, mention1_idxs, mention2_idxs
"""
get_relation_features = Compile([
  # The full dependency path between
  [Indicator(btwn, a) for a in BASIC_ATTRIBS_REL],

  # The *first element on the* path to the root: ngram lemmas along it
  Ngrams(Parents(btwn, 1), 'lemma', (1,3)),

  # The ngrams between
  [Ngrams(btwn, a, (2,3)) for a in BASIC_ATTRIBS_REL],

  # The VBs and NNs between
  [Ngrams(Filter(btwn, 'pos', p), 'lemma', (1,3)) for p in ['VB', 'NN']],

  # The siblings of each mention
  [LeftNgrams(LeftSiblings(m0), a) for a in BASIC_ATTRIBS_REL],
  [LeftNgrams(LeftSiblings(m1), a) for a in BASIC_ATTRIBS_REL],
  [RightNgrams(RightSiblings(m0), a) for a in BASIC_ATTRIBS_REL],
  [LeftNgrams(LeftSiblings(m1), a) for a in BASIC_ATTRIBS_REL]

]).apply_relation
