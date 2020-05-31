# TEST 1: Validation of shared bigram significance test on English data

from ccnc.algorithm import ccnc_statistic
from ccnc.data import LexicalDataset, ShuffledVariant
from ccnc.filters import AnySubsequenceFilter
from clics2.model import Clics2Model
import statistics

# define segments for English IPA representation (determines tokenization,
#   and thereby what counts as a shared two-segment subsequence)
english_segments = ["a","ɑ","ɒ","ɑː","æ","ʌ","aʊ","b","d","dʒ","ð","ɛ","ə","eɪ","ɛə","f",
                    "g","h","ɪ","i","iː","aɪ","ɪə","j","k","l","m","n","ŋ","ɔː","əʊ","ɔɪ",
                    "p","r","s","ʃ","t","tʃ","θ","u","ʊ","uː","ɜː","ʊə","w","v","z"]

if __name__ == '__main__':
  
  eng_lexicon = LexicalDataset("../eng-data/english.tsv",english_segments)
  
  concepts = sorted(eng_lexicon.concept_to_forms.keys())
  
  print(str(len(concepts)) + " concepts: " + str(concepts))
  
  # load the CLICS2 network from the associated (data-specific) model files
  network = Clics2Model("../clics-data/clics2-network-ids.txt", "../clics-data/clics2-network-edges.txt")

  any_bigram_filter = AnySubsequenceFilter(2)

  print("English:")
  true_score = ccnc_statistic(eng_lexicon, network, any_bigram_filter, 2, True)
  num_samples = 1000
  num_scores_above_true_score = 0
  scores = list()
  for i in range(0,num_samples):
    pseudo_eng = ShuffledVariant(eng_lexicon)
    resampled_score = ccnc_statistic(pseudo_eng, network, any_bigram_filter, 2, False)
    scores.append(resampled_score)
    if resampled_score > true_score:
      num_scores_above_true_score += 1
  print("p-value: " + str(num_scores_above_true_score/num_samples))
  mu = sum(scores)/len(scores)
  sigma = statistics.stdev(scores)
  zscore = (true_score - mu)/sigma
  print("z-score: " + str(zscore))
  print()
