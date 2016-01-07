from feature_templates import *

BASIC_ATTRIBS = ['word', 'lemma', 'pos', 'ner']

def get_generic_mention_features(root, cid, keywords):
  """
  Get the generic mention features as listed in the DDLib documentation
  http://deepdive.stanford.edu/doc/basics/gen_feats.html
  """
  temps = []

  # The basic attribs of the mention candidate span
  temps += [Indicator(Mention(cid), a) for a in BASIC_ATTRIBS]

  # Whether the mention candidate starts with a capital letter
  temps.append(Regexp(Mention(cid), 'word', r'^[A-Z].*$', 'STARTS_W_CAPITAL'))

  # The window features
  for a in BASIC_ATTRIBS:
    r = RightNgrams(RightSiblings(Mention(cid)), a)
    l = LeftNgrams(LeftSiblings(Mention(cid)), a)
    temps += [r, l, Combinations(r, l)]

  # Keyword in mention, in sentence; dep path labels + edges between kw and mention
  for kw in keywords:
    temps.append(Indicator(Keyword(kw, Mention(cid)), 'word'))
    temps.append(Indicator(Keyword(kw), 'word'))
    for a in ['dep_label', 'lemma', 'dep_label,lemma']:
      temps.append(Indicator(Between(Mention(cid), Keyword(kw)), a))

  # Apply the templates
  for temp in temps:
    for feat in temp.apply(root):
      yield feat
