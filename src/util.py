from collections import namedtuple
import re

def read_ptsv_element(x):
  """
  Parse an element in psql-compatible tsv format, i.e. {-format arrays
  Takes a string as input, handles float, int, str vals, and arrays of these types
  """
  if len(x) == 0:
    return None
  if x[0] == '{':
    return map(read_ptsv_element, re.split(r'\"?,\"?', re.sub(r'^\{\"?|\"?\}$', '', x)))
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

SentenceInput = namedtuple('SentenceInput', 'doc_id, sent_id, text, words, lemmas, poses, ners, word_idxs, dep_labels, dep_parents')

def load_sentences(f_path):
  """
  Helper fn to load NLP parser output file as SentenceInput objects
  """
  return [SentenceInput._make(read_ptsv(line)) for line in open(f_path, 'rb')] 
