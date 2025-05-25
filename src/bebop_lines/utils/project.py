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
  print("\nPRESENT FUNCTION: utils.project.proj_to_degree")
  
  assert isinstance(phrase, PermutationPhrase)

  degree_phrase = phrase.degree_phrase
  print("      PHRASE.DEGREE_PHRASE:", degree_phrase)

  if use_pivot_score:
    print("            CASE: use_pivot_score == True")
    pivot_score_list = pivot_score(degree_phrase)
    print("            pivot_score_list:", pivot_score_list)
    velocity_phrase = torch.Tensor(pivot_score(degree_phrase))
    print("            velocity_phrase:", velocity_phrase)
    print("            VELOCITY_PHRASE.SHAPE:", velocity_phrase.shape)
  else:
    print("            CASE: use_pivot_score != True")
    velocity_phrase = torch.ones((len(degree_phrase)))

  # char_tensor = deg_to_char(torch.Tensor(degree_phrase))
  print("\n      In utils.project.proj_to_degree\n      --> BEFORE CALL degree_to_char(degree_phrase).")
  char_tensor = deg_to_char(degree_phrase)
  print("      <-- AFTER CALL degree_to_char(degree_phrase).")
  print("      CHAR_TENSOR.SHAPE:", char_tensor.shape)
  weighted_char_tensor = torch.matmul(char_tensor.long(), velocity_phrase.unsqueeze(0).T.long())
  print("      WEIGHTED_CHAR_TENSOR.SHAPE:", weighted_char_tensor.shape)
  char_vector = torch.sum(weighted_char_tensor, dim=-1)
  print("      CHAR_VECTOR.SHAPE:", char_vector.shape)

  if normalize and np.sum(char_vector) != 0:
    char_vector = char_vector / torch.sum(char_vector)

  return char_vector