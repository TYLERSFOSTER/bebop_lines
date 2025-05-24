from __future__ import annotations

import numpy as np
import torch
import torch.nn.functional as F

from bebop_lines.melody.phrases import PermutationPhrase

INT_DTYPES = {
    torch.int8,
    torch.uint8,
    torch.int16,
    torch.int32,
    torch.int64,
}

def deg_to_char(phrase : list[int] | PermutationPhrase | np.ndarray | torch.Tensor) -> torch.Tensor:
    if isinstance(phrase, PermutationPhrase):
        print("CASE A STARTED.")
        degree_phrase = phrase.degree_phrase
        assert all(0 <= value <= 127 for value in degree_phrase), "phrase.degree_phrase must have all entries between MIDI pitch degrees 0 and 127"
        degree_phrase = torch.Tensor(degree_phrase)
        print("CASE A FINISHED.")
    elif isinstance(phrase, list):
        print("CASE B STARTED.")
        assert all(isinstance(value, int) for value in phrase)
        assert all(0 <= value <= 127 for value in phrase)
        degree_phrase = torch.Tensor(phrase)
        print("CASE B FINISHED.")
    elif isinstance(phrase, np.ndarray):
        print("CASE C STARTED.")
        assert len(phrase.shape) == 1
        assert np.issubdtype(phrase.dtype, np.integer)
        assert all(0 <= int(value) <= 127 for value in phrase)
        degree_phrase = torch.from_numpy(phrase)
        print("CASE C FINISHED.")
    elif isinstance(phrase, torch.Tensor):
        print("CASE D STARTED.")
        assert len(phrase.shape) == 1
        print("TYPE(PHRASE):", type(phrase))
        print("PHRASE.DTYPE:", phrase.dtype)
        # assert phrase.dtype in INT_DTYPES
        assert all(0 <= int(value) <= 127 for value in phrase)
        degree_phrase = phrase
        print("CASE D FINISHED.")

    print("DEGREE_PHRASE:", degree_phrase)
    
    phrase_onehots = F.one_hot(
        degree_phrase.long(),
        num_classes=128,
    )

    print("PHRASE_ONEHOTS.SHAPE:", phrase_onehots.shape)

    phrase_onehots = phrase_onehots.T

    return phrase_onehots