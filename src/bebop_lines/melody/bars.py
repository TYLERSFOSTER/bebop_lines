"""
Provides class representing a musical bar derived from a permutation
"""
from __future__ import annotations

import bebop_lines.group_action as grp

class PermutationBar():
    """
    Represents a single musical bar generated from a permutation of pitch degrees.

    This class interprets a permutation as a sequence of MIDI pitch degrees over
    indexed time steps. Each index in the permutation corresponds to a discrete time
    step, and the value at that index determines the MIDI pitch (after shifting).
    The `PermutationBar` selects a contiguous segment of this sequence and applies
    optional time and pitch shifts to produce a chromatic line.

    Attributes:
          start_idx : The start index of the time step interval to include in this bar.
          end_idx : The end index (exclusive) of the time step interval for this bar.
          idx_shift : A circular shift applied to time step indices before indexing the permutation.
          value_shift : A constant shift applied to all values of the permutation 
              before converting to MIDI.
          permutation : The underlying permutation used to generate the chromatic segment.
          number_of_elements : Total number of elements in the permutation (i.e., its length).
          tonic_degree : The MIDI pitch number to use as the tonic (e.g., 69 for A4 = 440 Hz).
          permutation_group : The group object representing the full permutation structure.
          duration_list : A list of durations (in arbitrary units) corresponding to each 
              index in the permutation.
    """
    def __init__(
        self,
        permutation : list[int],
        start_idx : int,
        end_idx : int,
        idx_shift : int,
        value_shift : int,
        permutation_group : grp.PermutationGroup | None=None,
        tonic_degree : int=69, # MIDI pitch number for A4 = 440 Hz
        duration_list : list | None=None,
    ):
        self.start_idx = start_idx
        self.end_idx = end_idx

        self.idx_shift = idx_shift
        self.value_shift = value_shift

        self.permutation = permutation
        self.number_of_elements = len(self.permutation)

        self.tonic_degree = tonic_degree

        if isinstance(permutation_group, type(None)):
            self.permutation_group = grp.PermutationGroup(self.number_of_elements)
        elif isinstance(permutation_group, grp.PermutationGroup):
            assert len(self.permutation) == permutation_group.number_of_elements
            self.permutation_group = permutation_group

        if isinstance(duration_list, type(None)):
            self.duration_list = [1 for n in range(self.number_of_elements)]
        else:
            assert len(duration_list) == self.number_of_elements
            self.duration_list = duration_list


    def __len__(self):
        bar_window_length = self.end_idx - self.start_idx

        return bar_window_length
        

    def change_bounds(self, new_start_idx : int, new_end_idx : int) -> None:
        """
        Update the start and end indices defining the time step interval for the bar.

        Args:
            new_start_idx : The new starting index of the bar.
            new_end_idx : The new ending index (exclusive) of the bar.
        """
        self.start_idx = new_start_idx
        self.end_idx = new_end_idx

    def change_shifts(self, new_idx_shift : int, new_value_shift : int) -> None:
        """
        Update the index and pitch shift parameters.

        Args:
            new_idx_shift : New circular index shift to apply to time steps before
                indexing the permutation.
            new_value_shift : New amount to add to each pitch value in the 
                permutation before mapping to MIDI.
        """
        self.ind_shift = new_idx_shift
        self.value_shift = new_value_shift

    def print_line(self) -> tuple[list[int], list[int]]:
        """
        Print the ultimate list of MIDI degrees and list of durations
        represented by this class.
        """
        degree_list = []
        duration_list = []

        for idx in range(self.start_idx, self.end_idx):
            shifted_idx = (idx - self.idx_shift)%self.number_of_elements

            value = self.permutation[shifted_idx]
            duration = 30 * self.duration_list[shifted_idx]

            shifted_value = value + self.value_shift
            shifted_value_at_tonic = shifted_value + self.tonic_degree

            degree_list.append(shifted_value_at_tonic)
            duration_list.append(duration)

        return degree_list, duration_list

    def first_degree(self) -> int:
        """Return first degree value in bar"""
        first_degree = self.print_line()[0][0]

        return first_degree

    def last_degree(self) -> int:
        """Return last degree value in bar"""
        last_degree = self.print_line()[0][-1]

        return last_degree
