from feature_template import *
from itertools import chain

def get_mention_templates(cid, d):
  """
  Generate the DDLib mention features as per
  http://deepdive.stanford.edu/doc/basics/gen_feats.html
  """
  return [
    
    # The set of POS tags comprising the mention
    Indicator(Mention(cid), 'pos'),

    # The set of NER tags comprising the mention
    Indicator(Mention(cid), 'ner'),

    # The set of lemmas comprising the mention
    Indicator(Mention(cid), 'lemma'),

    # The set of words comprising the mention
    Indicator(Mention(cid), 'word'),

    # TODO: Sum of the lengths of the words comprising the mention

    # Whether the first word in the mention starts with a capital letter
    RgxIndicator('^[A-Z].*$', 'word', 'STARTS_WITH_CAPITAL', Mention(cid)),

    # The lemma n-grams in a window of size 3 *of siblings* to the left and right of the mention
    # *Note* that this differs from ddlib in only considering sibling nodes
    # (which is the same if the tree is just a chain in original sequence order...)
    Indicator(Left(Mention(cid)), 'lemma'),
    Indicator(Right(Mention(cid)), 'lemma'),

    # Indicator feature of whether a keyword is part of the mention
    Indicator(Keyword(d, Mention(cid)), 'word'),

    # Indicator features of whether keywords appear in sentence
    Indicator(Keyword(d), 'word'),

    # Shortest dependency path between mention and keyword
    Indicator(Between(Mention(cid), Keyword(d)), 'lemma'),
    Indicator(Between(Mention(cid), Keyword(d)), 'dep_label')]

def get_mention_features(cid, d, root):
  return chain.from_iterable(t.apply(root) for t in get_mention_templates(cid, d))  
