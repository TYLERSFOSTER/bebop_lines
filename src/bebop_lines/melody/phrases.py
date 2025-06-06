"""
Class representing musical phrase
"""
from __future__ import annotations

import bebop_lines.melody as line


class PermutationPhrase():
    """
    Class representing an extended melodic phrase built up from
    multiple bars, i.e., from multiple bar.PermutationBar instances

    Attributes:
        bars_list : 
        permutations_list : 
        barline_degrees : 
        degree_phrase : 
        duration_phrase :
    """
    def __init__(self, bars_list : list[line.PermutationBar]):
        assert isinstance(bars_list, list)
        for entry in bars_list:
            assert isinstance(entry, line.PermutationBar)

        self.bars_list = bars_list
        self.permutations_list = [present_bar.permutation for present_bar in self.bars_list]

        degree_phrase = []
        duration_phrase = []
        barline_degrees = []
        for k, present_bar in enumerate(self.bars_list):
            barline_degrees.append(k)

            degree_list, duration_list = present_bar.print_line()

            degree_phrase = degree_phrase + degree_list
            duration_phrase = duration_phrase + duration_list
        self.barline_degrees = barline_degrees
        self.degree_phrase = degree_phrase
        self.duration_phrase = duration_phrase

    def __len__(self):
        total_phrase_length = 0
        for present_bar in self.bars_list:
            total_phrase_length += len(present_bar)

        return total_phrase_length
