# TEST 1: Shared bigram significance test for Proto-Aymaran and Proto-Quechuan

from ccnc.algorithm import ccnc_statistic
from ccnc.data import LexicalDataset, ShuffledVariant
from ccnc.filters import AnySubsequenceFilter
from clics2.model import Clics2Model
import statistics

# define segments for the two proto-languages (determines tokenization,
#   and thereby what counts as a shared two-segment subsequence)
proto_quechuan_segments = ["a","č","h","i","í","k","l","ʎ","m",
                           "n","ñ","p","q","r","s","š","t","tʂ","u","w","y"]
proto_aymaran_segments = ["a","č","č'","h","i","k","k'","kʰ","l","ʎ","m","n","ñ","p","p'","pʰ",
                          "q","q'","qʰ","r","s","š","t","t'","tʰ","tʂ","tʂ'","u","V","w","y"]

if __name__ == '__main__':
  
  # load full datasets in order to get access to the attested concepts
  pque_full_lexicon = LexicalDataset("../que-aym-data/proto-quechuan.tsv",proto_quechuan_segments)
  paym_full_lexicon = LexicalDataset("../que-aym-data/proto-aymaran.tsv",proto_aymaran_segments)
  
  concept_overlap = sorted(pque_full_lexicon.concept_to_forms.keys() & paym_full_lexicon.concept_to_forms.keys())
  
  print(str(len(concept_overlap)) + " shared concepts: " + str(concept_overlap))
  
  # reload relevant parts of the data (concepts for which we have data in bothlanguages)
  pque_lexicon = LexicalDataset("../que-aym-data/proto-quechuan.tsv",proto_quechuan_segments,concept_overlap)
  paym_lexicon = LexicalDataset("../que-aym-data/proto-aymaran.tsv",proto_aymaran_segments,concept_overlap)
  
  # load the CLICS2 network from the associated (data-specific) model files
  network = Clics2Model("../clics-data/clics2-network-ids.txt", "../clics-data/clics2-network-edges.txt")

  any_bigram_filter = AnySubsequenceFilter(2)

  print("Proto-Quechua:")
  true_score = ccnc_statistic(pque_lexicon, network, any_bigram_filter, 2, True)
  num_samples = 1000
  num_scores_above_true_score = 0
  scores = list()
  for i in range(0,num_samples):
    pseudo_pque = ShuffledVariant(pque_lexicon)
    resampled_score = ccnc_statistic(pseudo_pque, network, any_bigram_filter, 2, False)
    scores.append(resampled_score)
    if resampled_score > true_score:
      num_scores_above_true_score += 1
  print("p-value: " + str(num_scores_above_true_score/num_samples))
  mu = sum(scores)/len(scores)
  sigma = statistics.stdev(scores)
  zscore = (true_score - mu)/sigma
  print("z-score: " + str(zscore))
  print()

  print("Proto-Aymara:")
  true_score = ccnc_statistic(paym_lexicon, network, any_bigram_filter, 2, True)
  num_samples = 1000
  num_scores_above_true_score = 0
  scores = list()
  for i in range(0,num_samples):
    pseudo_paym = ShuffledVariant(paym_lexicon)
    resampled_score = ccnc_statistic(pseudo_paym, network, any_bigram_filter, 2, False)
    scores.append(resampled_score)
    if resampled_score > true_score:
      num_scores_above_true_score += 1
  print("p-value: " + str(num_scores_above_true_score/num_samples))
  mu = sum(scores)/len(scores)
  sigma = statistics.stdev(scores)
  zscore = (true_score - mu)/sigma
  print("z-score: " + str(zscore))
  print()

