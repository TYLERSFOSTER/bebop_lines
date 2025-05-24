from __future__ import annotations

import pytest
import numpy as np
import torch

from bebop_lines.utils.data_convert import deg_to_char



@pytest.mark.parametrize("degree_list", [
    ([0,1,2,3,4,5,6,7,8,9]),
    ([0, 5, 100, 127]),
    ([])
])
def test_deg_to_char__on_list(degree_list):
  output = deg_to_char(degree_list)

  assert isinstance(output, torch.Tensor)
  assert output.dtype == torch.int64


@pytest.mark.parametrize("degree_list", [
    ([0,1,2,3,4,5,6,7,8,9]),
    ([0, 5, 100, 127]),
])
def test_deg_to_char__on_array(degree_list):
  output = deg_to_char(degree_list)

  assert isinstance(output, torch.Tensor)
  assert output.dtype == torch.int64