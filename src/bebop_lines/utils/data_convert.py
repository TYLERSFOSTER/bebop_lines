"""
Utilities for transofroming data
"""
from __future__ import annotations

import torch
import torch.nn.functional as F

INT_DTYPES = {
    torch.int8,
    torch.uint8,
    torch.int16,
    torch.int32,
    torch.int64,
}

def deg_to_char(degree_phrase : list[int]) -> torch.Tensor:
    """
    Converts a list of pitch degrees into a one-hot encoded tensor.

    This function takes a list of integers representing pitch degrees
    (typically MIDI-like values) and converts it into a one-hot encoded
    tensor of shape (128, T), where T is the length of the input list.
    Each column in the resulting tensor represents the one-hot encoding
    of a single pitch degree with 128 possible pitch classes (0–127).

    Args:
        degree_phrase : A list of integer pitch degrees.

    Returns:
        torch.Tensor: A one-hot encoded tensor of shape (128, T), where each column represents
            a one-hot encoding of the corresponding pitch degree.
    """
    assert isinstance(degree_phrase, list)

    degree_phrase = list(map(int, degree_phrase))
    degree_phrase = torch.Tensor(degree_phrase) # type: ignore

    phrase_onehots = F.one_hot(
        degree_phrase.long(), # type: ignore
        num_classes=128,
    )

    phrase_onehots = phrase_onehots.T

    return phrase_onehots
