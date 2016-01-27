from templates import *
import lxml.etree as et

BASIC_ATTRIBS = ['word', 'lemma', 'pos', 'ner']
BASIC_ATTRIBS_REL = ['word', 'lemma', 'pos', 'ner', 'dep_label']


get_relation_features = Compile([
  """Args: root, mention1_idxs, mention2_idxs"""
  # The full dependency path between
  Indicator(Between(Mention(0), Mention(1)), a) for a in BASIC_ATTRIBS_REL,

  # The ngrams between
  Ngrams(Between(Mention(0), Mention(1)), a, (2,3)) for a in BASIC_ATTRIBS_REL,

  # The VBs between
  Ngrams(Filter(Between(Mention(0), Mention(1)), 'pos', 'VB'), 'lemma', (1,3)),

  # The siblings of each mention
  LeftNgrams(LeftSiblings(Mention(0)), a) for a in BASIC_ATTRIBS_REL,
  LeftNgrams(LeftSiblings(Mention(1)), a) for a in BASIC_ATTRIBS_REL,
  RightNgrams(RightSiblings(Mention(0)), a) for a in BASIC_ATTRIBS_REL,
  LeftNgrams(LeftSiblings(Mention(1)), a) for a in BASIC_ATTRIBS_REL

]).apply_relation
