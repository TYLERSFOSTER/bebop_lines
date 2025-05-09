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
  ):
    self.permutation = permutation
    
    if isinstance(permutation_group, type(None)):
      self.permutation_group = ga.PermutationGroup(len(self.permutation))
    else:
      assert len(self.permutation) == len(permutation_group.number_of_elements)
      self.permutation_group = permutation_group

    self.start_idx = start_idx
    self.end_idx = end_idx
    self.int_shift = int_shift
    self.out_shift = out_shift
