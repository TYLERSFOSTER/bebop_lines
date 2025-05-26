"""
Permutation groups on N letters
"""
from __future__ import annotations

import copy

import bebop_lines.group_action as ga


class Permutations():
    """
    Class for dynamically collecting full sets of permutations on n letters,
    for increasing n.
    """
    def __init__(self):
        self.permutation_dict = {1 : [[0]]}

    def fillout_to(self, n : int) -> None:
        """
        Fill out permutation_dict attribute up to n
        """
        if n in self.permutation_dict:
            return

        m = max(self.permutation_dict)

        for element_count in range(m, n):
            new_permutations = []
            for permutation in self.permutation_dict[element_count]:
                for idx in range(len(permutation) + 1):
                    current_permutation = copy.deepcopy(permutation)

                    current_permutation.insert(idx, element_count)

                    new_permutations.append(current_permutation)

            self.permutation_dict[element_count + 1] = new_permutations
        return

    def __len__(self) -> int:
        return self.completed_upto()

    def __getitem__(self, index: int) -> list[list[int]]:
        if index > self.completed_upto():
            self.fillout_to(index)

        permutation_group = self.permutation_dict[index]

        return permutation_group


    def completed_upto(self) -> int:
        """
        Return the largest number of letters on which all permutations
        have been stored as attributes
        """
        return max(self.permutation_dict)



class PermutationGroup():
    """
    Class representing the group of permutations on the set {0, 1, 2, ...., N-1},
    where N is the number_of_elements
    """
    def __init__(self, number_of_elements : int, permutations : ga.Permutations | None=None):
        if isinstance(permutations, type(None)):
            permutations = Permutations()

        self.number_of_elements = number_of_elements
        permutations.fillout_to(number_of_elements)

        self.underlying_set = permutations[number_of_elements]
        self.identity = range(number_of_elements)

    def __len__(self) -> int:
        length = len(self.underlying_set)

        return length

    def __getitem__(self, idx : int) -> list[int]:
        element = self.underlying_set[idx]

        return element

    def compose(self, elem_0 : list[int], elem_1 : list[int]) -> list[int]:
        """
        Compose two permutations in the permutation group
        """
        assert isinstance(elem_0, list)
        assert isinstance(elem_1, list)
        assert len(elem_0) == self.number_of_elements
        assert len(elem_1) == self.number_of_elements

        composite = [elem_1[elem_0[n]] for n in range(self.number_of_elements)]

        return composite

    def invert(self, element : list[int]) -> list[int]:
        """
        Invert a permutation in the permutation group
        """
        assert isinstance(element, list)
        assert len(element) == self.number_of_elements

        inverse_element = []

        for idx in range(self.number_of_elements):
            value = element.index(idx)
            inverse_element.append(value)

        return inverse_element
