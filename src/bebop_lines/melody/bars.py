from __future__ import annotations

import bebop_lines.group_action as ga

class PermutationBar():
  def __init__(
    self,
    permutation : list[int],
    start_idx : int,
    end_idx : int,
    int_shift : int,
    out_shift : int,
    permutation_group : ga.PermutationGroup | None=None,
    tonic_degree : int=69, # MIDI pitch number for A4 = 440 Hz
  ):
    self.start_idx = start_idx
    self.end_idx = end_idx

    self.idx_shift = idx_shift
    self.value_shift = value_shift

    self.permutation = permutation
    self.number_of_elements = len(self.permutation)

    if isinstance(permutation_group, type(None)):
      self.permutation_group = ga.PermutationGroup(self.number_of_elements)
    else:
      assert len(self.permutation) == len(permutation_group.number_of_elements)
      self.permutation_group = permutation_group
  
  def change_bounds(self, new_start_idx, new_end_idx):
    self.start_idx = new_start_idx
    self.end_idx = new_end_idx

  def change_shifts(self, new_idx_shift, new_value_shift):
    self.ind_shift = new_idx_shift
    self.value_shift = new_value_shift

  def print_degrees(self):
    degree_list = []

    for idx in range(self.start_idx, self.end_idx):
      shifted_idx = (idx - self.idx_shift)%self.number_of_elements
    
      value = self.permutation[shifted_idx]

      shifted_value = value + self.value_shift
      shifted_valued_at_tonic = shifted_value + tonic_degree
      
      degree_list.append(shifted_valued_at_tonic)

    return degree_list
