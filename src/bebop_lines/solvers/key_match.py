from __future__ import annotations

import numpy as np

import bebop_lines.melody as line
from bebop_lines.solvers.pivots import pivot_score


def proj_to_degree(phrase : line.PermutationPhrase) -> np.ndarray:
  """
  Generate a distribution on 12-TET MIDI scale degrees that encodes the
  total amplitude of degrees in a given phrase

  Args:
    phrase : Instance of the PermutationPhrase class

  Retuns:
    An np.ndarray providing a distribution of total amplitude in phrase
  """
  degree_phrase = phrase.degree_phrase
  velocity_phrase = pivot_score(degree_phrase)

  char_vector = np.zeros(128)
  for degree, velocity in zip(degree_phrase, velocity_phrase):
    char_vector[degree] += velocity

  char_vector = char_vector / np.sum(char_vector)

  return char_vector


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
  def __init__(self, degree_list : list[int], repeat_mod_12 : bool=False, degree_weights : np.ndarray=np.ones((128))):
    """
    Initialize a Scale object.

    Args:
      degree_list : The base degrees to include in the scale (0–127).
      repeat_mod_12 : If True, adds +/- 12k transpositions of each degree within the valid MIDI range. Defaults to False.
      degree_weights : A 128-element array specifying weights for each MIDI pitch. Defaults to ones.
    """
    assert len(degree_weights) == 128

    if repeat_mod_12:
      new_degree_list = []
      for degree in degree_list:
        if 0 <= degree <= 127:
          new_degree_list.append(degree)

          for n in range(-11, 11):
            new_degree = degree + n * 12

            if 0 <= new_degree <= 127 and not new_degree in new_degree_list:
              new_degree_list.append(new_degree)
              print("REPEAT_MOD_12:", repeat_mod_12)
      new_degree_list.sort()
      self.degree_list = new_degree_list
    else:
      self.degree_list = degree_list

    self.char_vector = np.array([int(n in self.degree_list) * degree_weights[n] 
                                   for n in range(128)])

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
    dist_of_phrase = proj_to_degree(phrase)

    matching_score = np.dot(self.char_vector, dist_of_phrase)

    return matching_score