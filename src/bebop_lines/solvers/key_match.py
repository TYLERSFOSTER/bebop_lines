from __future__ import annotations

import torch
import numpy as np

from bebop_lines.utils.data_convert import deg_to_char
from bebop_lines.utils.project import proj_to_degree
import bebop_lines.melody as line


class Scale():
  """
  Represents a musical scale in 12-tone equal temperament (12-TET)
  using MIDI pitch degrees.

  Attributes:
    degree_list (list[int]): List of MIDI degrees representing the scale,
      possibly extended via mod 12 repetition.
    char_vector (np.ndarray): A 128-length array where each index corresponds
      to a MIDI pitch, weighted if it's part of the scale.
    repeat_mod_12 (bool): Whether to include repeated versions of the degrees
      modulo 12 across the MIDI range.
  """
  def __init__(
      self,
      degree_list : list[int],
      repeat_mod_12 : bool=False,
      degree_weights : np.ndarray=np.ones(128),
  ):
    """
    Initialize a Scale object.

    Args:
      degree_list : The base degrees to include in the scale (0–127).
      repeat_mod_12 : If True, adds +/- 12k transpositions of each degree within the valid MIDI range. Defaults to False.
      degree_weights : A 128-element array specifying weights for each MIDI pitch. Defaults to ones.
    """
    assert len(degree_weights) == 128

    if repeat_mod_12 == True:
      new_degree_list = []
      for degree in degree_list:
        if 0 <= degree <= 127:
          new_degree_list.append(degree)

          for n in range(-14, 14):
            new_degree = degree + n * 12

            if 0 <= new_degree <= 127 and not new_degree in new_degree_list:
              new_degree_list.append(new_degree)

      new_degree_list.sort()
      self.degree_list = new_degree_list
    else:
      self.degree_list = degree_list

    self.char_vector = deg_to_char(self.degree_list)

    self.repeat_mod_12 = repeat_mod_12

  def dot(self, phrase : line.PermutationPhrase) -> float:
    """
    Compute a matching score between this scale and a phrase, using a dot product.

    Args:
      phrase : The phrase to compare, represented by its degree distribution.

    Returns:
      float: The dot product between the scale's characteristic vector and the
        degree distribution of the phrase.
    """
    print("PHRASE:", phrase)
    print("TYPE(PHRASE):", type(phrase))
    print("PHRASE.DEGREE_PHEASE:", phrase.degree_phrase)
    dist_of_phrase = proj_to_degree(phrase)

    print("DIST_OF_PHRASE:", dist_of_phrase)

    matching_score = torch.matmul(self.char_vector, dist_of_phrase)
    print("MATCHING_SCORE.SHAPE:", matching_score.shape)
    matching_score = float(matching_score)

    return matching_score