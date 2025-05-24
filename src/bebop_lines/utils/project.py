from __future__ import annotations

import numpy as np
import torch


from bebop_lines.utils.data_convert import deg_to_char
import bebop_lines.melody as line
from bebop_lines.solvers.pivots import pivot_score


def proj_to_degree(
    phrase : line.PermutationPhrase | list[int],
    use_pivot_score : bool=True,
    normalize : bool=False,
) -> torch.Tensor:
  """
  Generate a distribution on 12-TET MIDI scale degrees that encodes the
  total amplitude of degrees in a given phrase

  Args:
    phrase : Instance of the PermutationPhrase class

  Retuns:
    An np.ndarray providing a distribution of total amplitude in phrase

  """
  print("PHRASE:", phrase)
  if isinstance(phrase, line.PermutationPhrase):
    degree_phrase = phrase.degree_phrase
  elif isinstance(phrase, list):
    degree_phrase = [int(value) for value in phrase]
  elif isinstance(phrase, np.ndarray):
    degree_phrase = list(phrase)

  if use_pivot_score:
    velocity_phrase =torch.Tensor(pivot_score(degree_phrase))
  else:
    velocity_phrase = torch.ones((len(degree_phrase)))

  char_tensor = deg_to_char(torch.Tensor(degree_phrase))
  
  print("CHAR_TENSOR.SHAPE:", char_tensor.shape)
  print("VELOCITY_PHRASE.SHAPE:", velocity_phrase.shape)
  weighted_char_tensor = torch.matmul(char_tensor.long(), velocity_phrase.T.long())

  print("CHAR_TENSOR:", char_tensor)
  print("CHAR_TENSOR.SHAPE:", char_tensor.shape)
  print("WEIGHTED_CHAR_TENSOR:", weighted_char_tensor)
  print("WEIGHTED_CHAR_TENSOR.SHAPE:", weighted_char_tensor.shape)
  char_vector = torch.sum(weighted_char_tensor, dim=-1)
  print("CHAR_VECTOR:", char_vector)


  if normalize and np.sum(char_vector) != 0:
    char_vector = char_vector / torch.sum(char_vector)

  return char_vector