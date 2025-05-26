from __future__ import annotations

import math

import pytest

import bebop_lines.group_action as ga


def test_Permutations__init():
    permutations = ga.Permutations()

    assert isinstance(permutations, ga.Permutations)
    assert permutations.permutation_dict == {1: [[0]]}


@pytest.mark.parametrize("number_of_elements", [n for n in range(2, 10)])
def test_Permutations__fillout_to(number_of_elements):
    permutations = ga.Permutations()
    permutations.fillout_to(number_of_elements)

    dict_keys = list(permutations.permutation_dict.keys())

    assert dict_keys == [n + 1 for n in range(number_of_elements)]


@pytest.mark.parametrize("number_of_elements", [n for n in range(2, 10)])
def test_Permutations__getitem(number_of_elements):
    permutations = ga.Permutations()

    result = permutations[number_of_elements]

    dict_keys = list(permutations.permutation_dict.keys())

    assert dict_keys == [n + 1 for n in range(number_of_elements)]
    assert len(result) == math.factorial(number_of_elements)


@pytest.mark.parametrize("number_of_elements", [n for n in range(2, 10)])
def test_Permutations__completed_upto_after_fillout_to(number_of_elements):
    permutations = ga.Permutations()

    permutations.fillout_to(number_of_elements)

    number_completed = permutations.completed_upto()

    assert number_completed == number_of_elements


@pytest.mark.parametrize("number_of_elements", [n for n in range(2, 10)])
def test_Permutations__completed_upto_after_getitem(number_of_elements):
    permutations = ga.Permutations()

    permutations[number_of_elements]

    number_completed = permutations.completed_upto()

    assert number_completed == number_of_elements


@pytest.mark.parametrize("number_of_elements", [n for n in range(2, 10)])
def test_PermutationGroup__init_with_Permutations(number_of_elements):
    permutations = ga.Permutations()

    permutations.fillout_to(number_of_elements)

    group = ga.PermutationGroup(number_of_elements, permutations=permutations)

    assert len(group) == len(group.underlying_set)
    assert len(group) == math.factorial(number_of_elements)


@pytest.mark.parametrize("number_of_elements", [n for n in range(2, 10)])
def test_PermutationGroup__init_without_Permutations(number_of_elements):
    group = ga.PermutationGroup(number_of_elements)

    assert len(group) == len(group.underlying_set)
    assert len(group) == math.factorial(number_of_elements)


@pytest.mark.parametrize("number_of_elements", [n for n in range(3, 10)])
def test_PermutationGroup__getitem(number_of_elements):
    group = ga.PermutationGroup(number_of_elements)
    element = group[number_of_elements - 1]

    assert isinstance(element, list)
    assert len(element) == number_of_elements


@pytest.mark.parametrize("number_of_elements", [n for n in range(3, 10)])
def test_PermutationGroup__getitem__0th_element(number_of_elements):
    group = ga.PermutationGroup(number_of_elements)
    element = group[0]

    answer = [number_of_elements - n - 1 for n in range(number_of_elements)]

    assert element == answer


@pytest.mark.parametrize("number_of_elements", [n for n in range(3, 10)])
def test_PermutationGroup__compose(number_of_elements):
    group = ga.PermutationGroup(number_of_elements)
    elem_0 = [number_of_elements - n - 1 for n in range(number_of_elements)]

    result = group.compose(elem_0, elem_0)

    answer = [n for n in range(number_of_elements)]

    assert result == answer


@pytest.mark.parametrize("number_of_elements", [n for n in range(3, 10)])
def test_PermutationGroup__compose__transposition(number_of_elements):
    group = ga.PermutationGroup(number_of_elements)
    elem_0 = [n for n in range(number_of_elements)]
    elem_0[0] = 1
    elem_0[1] = 0

    result = group.compose(elem_0, elem_0)

    answer = [n for n in range(number_of_elements)]

    assert result == answer


@pytest.mark.parametrize("number_of_elements", [n for n in range(3, 10)])
def test_PermutationGroup__invert(number_of_elements):
    group = ga.PermutationGroup(number_of_elements)
    element = [number_of_elements - n - 1 for n in range(number_of_elements)]

    inverse = group.invert(element)

    assert inverse == element
    