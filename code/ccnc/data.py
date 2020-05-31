import random

def tokenize(form,segments):
  tokens = []
  current_token = ""
  i = 0
  while i < len(form):
    found_segment = False
    for j in range(len(form),i,-1):
      if form[i:j] in segments:
        tokens.append(form[i:j])
        i = j
        found_segment = True
        break;
    if not found_segment:
      print("ERROR: could not parse token \"" + form[i] + "\" in form \"" + form + "\", form gets truncated!")
      break
  return tuple(tokens)

class LexicalDataset:
  
  def __init__(self, model_file_name,segments,concepts=None):
    self.concept_to_forms = dict()
    with open(model_file_name,"r") as model_file:
      for line in model_file:
        tokens = line.strip().split("\t")
        if len(tokens) < 2 or len(tokens[1]) == 0: continue
        concept = tokens[0]
        if concepts == None or concept in concepts:
          forms = tokens[1].split("/")
          tokenized_forms = []
          for form in forms:
            form_tokens = tokenize(form,segments)
            tokenized_forms.append(form_tokens)
          self.concept_to_forms[concept] = tokenized_forms
  
  def get_forms(self):
    forms = list()
    for concept in self.concept_to_forms:
      forms.extend(self.concept_to_forms[concept])
    return forms


class ShuffledVariant:
  
  def __init__(self, true_lexical_data):
    self.concept_to_forms = dict()
    forms = true_lexical_data.get_forms()
    random.shuffle(forms)
    for concept in true_lexical_data.concept_to_forms:
      forms_for_concept = []
      for i in range(0,len(true_lexical_data.concept_to_forms[concept])):
        forms_for_concept.append(forms.pop())
      self.concept_to_forms[concept] = forms_for_concept
