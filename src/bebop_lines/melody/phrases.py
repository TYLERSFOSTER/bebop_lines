from __future__ import annotations

import math

import bebop_lines.group_action as ga
from bebop_lines.melody.bars import PermutationBar


class PermutationPhrase():
  def __inti__(self, bars_list : list[PermutationBar]):
    assert isinstance(bars_list, list)
    for entry in bars_list:
      assert isinstance(entry, PermutationBar)

    self.bars_list = bars_list

    bar_jumps = []
    absolute_bar_jumps = []
    for idx in range(1, len(self.bars_list)):
        last_ending_degree = bars_list[idx -1 ].last_degree()
        next_starting_degree = bars_list[idx -1 ].first_degree()

        difference = next_starting_degree - last_ending_degree
        absolute_difference = math.abs(difference)

    self.bar_jumps = []
