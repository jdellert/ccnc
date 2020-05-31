class Clics2Model:

  def __init__(self, id_file_path, edge_file_path):
    self.id_to_name = dict()
    self.name_to_id = dict()
    self.neighbors = dict()
    with open(id_file_path) as id_file:
      for id_line in id_file:
        id_line = id_line.strip()
        split_pos = id_line.index('\t')
        id = id_line[0:split_pos]
        name = id_line[split_pos+1:]
        self.id_to_name[id] = name
        self.name_to_id[name] = id
        self.neighbors[id] = set()
    with open(edge_file_path) as edge_file:
      for edge_line in edge_file:
        edge_line = edge_line.strip() 
        split_pos = edge_line.index('\t')
        id1 = edge_line[0:split_pos]
        id2 = edge_line[split_pos+1:]
        self.neighbors[id1].add(id2)
        self.neighbors[id2].add(id1)

  def get_neighbors(self, concept):
    concept_id = self.name_to_id[concept]
    neighbor_ids = self.neighbors[concept_id]
    return [self.id_to_name[neighbor_id] for neighbor_id in neighbor_ids]
