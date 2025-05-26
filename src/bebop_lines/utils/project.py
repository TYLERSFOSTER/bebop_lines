from __future__ import annotations

import numpy as np
import torch


from bebop_lines.utils.data_convert import deg_to_char
from bebop_lines.melody import PermutationPhrase
from bebop_lines.solvers.pivots import pivot_score


def proj_to_degree(
    phrase : PermutationPhrase | list[int],
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
  assert isinstance(phrase, PermutationPhrase)

  degree_phrase = phrase.degree_phrase

  if use_pivot_score:
    velocity_phrase = torch.Tensor(pivot_score(degree_phrase))
  else:
    velocity_phrase = torch.ones((len(degree_phrase)))

  char_tensor = deg_to_char(degree_phrase)

  weighted_char_tensor = torch.matmul(char_tensor.long(), velocity_phrase.unsqueeze(0).T.long())

  char_vector = torch.sum(weighted_char_tensor, dim=-1)

  if normalize and np.sum(char_vector) != 0:
    char_vector = char_vector / torch.sum(char_vector)

  return char_vector