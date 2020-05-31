import ccnc.filters

def ccnc_statistic(lexical_data, network, subsequence_filter, min_cluster_size, print_clusters=False):
  clusters = ccnc_clusters(lexical_data, network, subsequence_filter, min_cluster_size, print_clusters)
  return compute_clustering_statistic(clusters)

def ccnc_clusters(lexical_data, network, subsequence_filter, min_cluster_size, print_clusters=False):
  if not isinstance(subsequence_filter, ccnc.filters.SubsequenceFilter):
    print("ERROR: subsequence_filter argument needs to be an instance of (a subtype of) filters.SubsequenceFilter!")
  extracted_clusters = []
  already_covered_words = set()
  while True:
    found_cluster = False
    largest_cluster_size = min_cluster_size - 1
    words_in_largest_cluster = set()
    for concept in lexical_data.concept_to_forms.keys():
      subsequence_counts = dict()
      for form in lexical_data.concept_to_forms[concept]:
        if (concept,form) not in already_covered_words:
          for subsequence in subsequence_filter.extract_relevant_subsequences(form):
            if subsequence not in subsequence_counts:
              subsequence_counts[subsequence] = 0
            subsequence_counts[subsequence] += 1
      neighboring_concepts = network.get_neighbors(concept)
      num_covered_neighbors = 0
      for neighbor in neighboring_concepts:
        if neighbor not in lexical_data.concept_to_forms: continue
        num_covered_neighbors += 1
        for form in lexical_data.concept_to_forms[neighbor]:
          if (neighbor,form) not in already_covered_words:
            for subsequence in subsequence_filter.extract_relevant_subsequences(form):
              if subsequence in subsequence_counts:
                subsequence_counts[subsequence] += 1
      for subsequence in subsequence_counts.keys():
        if subsequence_counts[subsequence] > largest_cluster_size:
          found_cluster = True
          largest_cluster_size = subsequence_counts[subsequence]
          words_in_largest_cluster = set()
          for form in lexical_data.concept_to_forms[concept]:
            if subsequence_filter.check_subsequence_occurrence(form, subsequence) and (concept,form) not in already_covered_words:
              words_in_largest_cluster.add((concept,form))
          for neighbor in neighboring_concepts:
            if neighbor not in lexical_data.concept_to_forms: continue
            for form in lexical_data.concept_to_forms[neighbor]:
              if subsequence_filter.check_subsequence_occurrence(form, subsequence) and (neighbor,form) not in already_covered_words:
                words_in_largest_cluster.add((neighbor,form))
    if not found_cluster: break
    extracted_clusters.append(words_in_largest_cluster)
    if print_clusters: print("Found cluster of size " + str(largest_cluster_size) + ":")
    for (concept,form) in words_in_largest_cluster:
      if print_clusters: print("  \"" + "".join(form) + "\" assigned to concept " + concept)
      already_covered_words.add((concept,form))
  return extracted_clusters

def compute_clustering_statistic(clusters):
  # define cluster size weighting here (spelled out for easy modifiability)
  #   hard-coded weights up to maximum cluster size 16, error will result from any larger cluster size
  #   to use our clustering statistic in the unlikely case there are clusters with k > 16, expand by binom(k,2) values as needed
  counts_of_cluster_size = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  size_weights = [0,0,1,3,6,10,15,21,28,36,45,55,66,78,91,105,120]
  for cluster in clusters:
    counts_of_cluster_size[len(cluster)] += 1
  clustering_statistic = 0;
  for i in range(0,len(counts_of_cluster_size)):
    clustering_statistic += counts_of_cluster_size[i] * size_weights[i]
  return clustering_statistic
