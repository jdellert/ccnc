# TEST 2: Bigram significance tests in any position, as prefixes, and as suffixes, on the entire Proto-Quechuan dataset

from ccnc.algorithm import ccnc_statistic
from ccnc.data import LexicalDataset, ShuffledVariant
from ccnc.filters import AnySubsequenceFilter, PrefixSubsequenceFilter, SuffixSubsequenceFilter
from clics2.model import Clics2Model
import statistics

# define segments for the two proto-languages (determines tokenization,
#   and thereby what counts as a shared two-segment subsequence)
proto_quechuan_segments = ["a","č","h","i","í","k","l","ʎ","m",
                           "n","ñ","p","q","r","s","š","t","tʂ","u","w","y"]

if __name__ == '__main__':
  pque_lexicon = LexicalDataset("../que-aym-data/proto-quechuan.tsv",proto_quechuan_segments)
  
  # load the CLICS2 network from the associated (data-specific) model files
  network = Clics2Model("../clics-data/clics2-network-ids.txt", "../clics-data/clics2-network-edges.txt")

  any_bigram_filter = AnySubsequenceFilter(2)
  prefix_bigram_filter = PrefixSubsequenceFilter(2)
  suffix_bigram_filter = SuffixSubsequenceFilter(2)
  
  #ANY TWO-SEGMENT SUBSEQUENCE TEST
  print("Test for any two-segment subsequences:")
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

  #PREFIX TEST
  print("Test for any two-segment prefixes:")
  true_score = ccnc_statistic(pque_lexicon, network, prefix_bigram_filter, 2, True)
  num_samples = 1000
  num_scores_above_true_score = 0
  scores = list()
  for i in range(0,num_samples):
    pseudo_pque = ShuffledVariant(pque_lexicon)
    resampled_score = ccnc_statistic(pseudo_pque, network, prefix_bigram_filter, 2, False)
    scores.append(resampled_score)
    if resampled_score > true_score:
      num_scores_above_true_score += 1
  print("p-value: " + str(num_scores_above_true_score/num_samples))
  mu = sum(scores)/len(scores)
  sigma = statistics.stdev(scores)
  zscore = (true_score - mu)/sigma
  print("z-score: " + str(zscore))
  print()

  #SUFFIX TEST
  print("Test for any two-segment suffixes:")
  true_score = ccnc_statistic(pque_lexicon, network, suffix_bigram_filter, 2, True)
  num_samples = 1000
  num_scores_above_true_score = 0
  scores = list()
  for i in range(0,num_samples):
    pseudo_pque = ShuffledVariant(pque_lexicon)
    resampled_score = ccnc_statistic(pseudo_pque, network, suffix_bigram_filter, 2, False)
    scores.append(resampled_score)
    if resampled_score > true_score:
      num_scores_above_true_score += 1
  print("p-value: " + str(num_scores_above_true_score/num_samples))
  mu = sum(scores)/len(scores)
  sigma = statistics.stdev(scores)
  zscore = (true_score - mu)/sigma
  print("z-score: " + str(zscore))
  print()


