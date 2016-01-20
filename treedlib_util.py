from collections import namedtuple
import re

def read_ptsv_element(x, splitter='|^|'):
  """
  Parse an element in psql-compatible tsv format, i.e. {-format arrays
  Takes a string as input, handles float, int, str vals, and arrays of these types
  """
  if len(x) == 0:
    return None
  elif x[0] == '{':
    return map(read_ptsv_element, re.split(r'\"?,\"?', re.sub(r'^\{\"?|\"?\}$', '', x)))
  elif '|^|' in x:
    return map(read_ptsv_element, x.split('|^|'))
  for type_fn in [int, float, str]:
    try:
      return type_fn(x)
    except ValueError:
      pass
  raise ValueError("Type not recognized.")


def read_ptsv(line):
  """
  Parse a line in psql-compatible tsv format
  I.e. tab-separated with psql {-style arrays
  """
  return map(read_ptsv_element, line.rstrip().split('\t'))

#SentenceInput = namedtuple('SentenceInput', 'words, lemmas, poses, ners, dep_labels, dep_parents, word_idxs')

RelationInput = namedtuple('RelationInput', 'relation_id, doc_id, section_id, sent_id, gene_mention_id, gene_wordidxs, pheno_mention_id, pheno_wordidxs, words, lemmas, poses, ners, dep_paths, dep_parents, word_idxs')


CoreNLPInput = namedtuple('CoreNLPInput', 'doc_id, sent_id, text, words, lemmas, poses, ners, char_idxs, dep_labels, dep_parents, word_idxs')

def load_corenlp_sentences(f_path):
  """Helper fn to load NLP parser output file as CoreNLPInput objects"""
  for line in open(f_path, 'rb'):
    l = read_ptsv(line)
    yield CoreNLPInput._make(l + [range(len(l[3]))])


def tag_candidate(root, words, cid):
  """
  Hackey function to tag candidates in xml tree
  Note for example that this will get messed up if the words comprising the candidate occur
  elsewhere in the sentence also...
  """
  for word in words:
    root.findall(".//node[@word='%s']" % word)[0].set('cid', cid)
