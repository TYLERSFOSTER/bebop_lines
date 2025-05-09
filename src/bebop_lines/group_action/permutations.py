"""
Class for 
"""
from __future__ import annotations

import copy
import random

import numpy as np

import bebop_lines.group_action as ga


class Permutations():
  def __init__(self):
    self.permutation_dict = {1:[[0]]}

  def fillout_to(self, n : int) -> None:
    if n in self.permutation_dict:
      return
    else:
      m = max(self.permutation_dict)

      for element_count in range(m, n):
        new_permutations = []
        for permutation in self.permutation_dict[element_count]:
          for idx in range(len(permutation) + 1):
            current_permutation = copy.deepcopy(permutation)

            current_permutation.insert(idx, element_count)

            new_permutations.append(current_permutation)
            
        self.permutation_dict[element_count+1] = new_permutations
      return

  def __getitem__(self, element_count):
    if element_count > self.completed_upto():
      self.fillout_to(element_count)

    return self.permutation_dict[element_count]

  def completed_upto(self):
    return max(self.permutation_dict)



class PermutationGroup():
  def __init__(self, number_of_elements, permutations : ga.Permutations | None=None):
    if isinstance(permutations, type(None)):
      permutations = Permutations()

    self.number_of_elements = number_of_elements

    self.underlying_set = permutations[number_of_elements]
    self.identity = [n for n in range(number_of_elements)]

  def __len__(self):
    length = len(self.underlying_set)

    return length

  def __getitem__(self, idx):
    element = self.underlying_set[idx]

    return element

  def compose(self, elem_0, elem_1):
    assert isinstance(elem_0, list)
    assert isinstance(elem_1, list)
    assert len(elem_0) == self.number_of_elements
    assert len(elem_1) == self.number_of_elements

    composite = [elem_1[elem_0[n]] for n in range(self.number_of_elements)]

    return composite

  def invert(self, element):
    inverse_element = []

    for idx in range(self.number_of_elements):
      value = element.index(idx)
      inverse_element.append(value)
    
    return inverse_element




