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

  char_vector = np.zeros_like(degree_phrase)
  for degree, velocity in zip(degree_phrase, velocity_phrase):
    char_vector[degree] += velocity

  char_vector = char_vector / np.sum(char_vector)

  return char_vector


class Scale():
  """
  Class reprenting a 12-TET musical scale using MIDI pitch degrees
  """
  def __init__(self, degree_list : list[int], repeat_mod_12 : bool=False, degree_weights : list[float] | None=None):
    assert len(degree_weights) == 128

    new_degree_list = []
    for degree in degree_list:
      if 0 <= degree <= 127:
        new_degree_list.append(degree)

        if repeat_mod_12:
          for n in range(-11, 11):
            new_degree = degree + n * 12

            if 0 <= new_degree <= 127:
              new_degree_list.append(new_degree)

    new_degree_list.sort()
    self.degree_list = new_degree_list

    if isinstance(degree_weights, type(None)):
      degree_weights = np.ones((127,))
    self.char_vector = np.array([int(n in self.degree_list) * degree_weights[n]
                                 for n in range(128)])

    self.repeat_mod_12 = repeat_mod_12

  def dot(self, phrase : line.PermutationPhrase) -> float:
    """
    Return the dot product between a degree scale and a degree phrase 
    """
    dist_of_phrase = proj_to_degree(phrase)

    matching_score = np.dot(self.char_vector, dist_of_phrase)

    return matching_score