
class SubsequenceFilter:
  
  # override this method in each specific filter, return the list of relevant subsequences
  def extract_relevant_subsequences(self, sequence):
    return []
  
  # override this method in each specific filter, returns True iff sequence contains the relevant subsequence
  #   result must be consistent with the result of extract_relevant_subsequences
  #   (only separated for potentially higher efficiency)
  def check_subsequence_occurrence(self, sequence, subsequence):
    return False


class AnySubsequenceFilter(SubsequenceFilter):
  
  def __init__(self, subsequence_length):
    self.n = subsequence_length
  
  def extract_relevant_subsequences(self, sequence):
    subsequence_list = []
    for i in range(0,len(sequence)-self.n):
      subsequence_list.append(sequence[i:i+self.n])
    return subsequence_list
  
  def check_subsequence_occurrence(self, sequence, subsequence):
    for i in range(0,len(sequence)-self.n):
      if sequence[i:i+self.n] == subsequence: return True
    return False


class PrefixSubsequenceFilter(SubsequenceFilter):
  
  def __init__(self, prefix_length):
    self.n = prefix_length

  def extract_relevant_subsequences(self, sequence):
    return [sequence[0:self.n]]
  
  def check_subsequence_occurrence(self, sequence, prefix):
    return sequence[0:self.n] == prefix


class SuffixSubsequenceFilter(SubsequenceFilter):
  
  def __init__(self, suffix_length):
    self.n = suffix_length
  
  def extract_relevant_subsequences(self, sequence):
    return [sequence[-self.n:]]
  
  def check_subsequence_occurrence(self, sequence, suffix):
    return sequence[-self.n:] == suffix
