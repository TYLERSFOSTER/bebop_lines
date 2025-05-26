from __future__ import annotations

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

def deg_to_char(degree_phrase : list[int]) -> torch.Tensor:
    assert isinstance(degree_phrase, list)

    degree_phrase = list(map(int, degree_phrase))
    degree_phrase = torch.Tensor(degree_phrase) # type: ignore
    
    phrase_onehots = F.one_hot(
        degree_phrase.long(), # type: ignore
        num_classes=128,
    )

    phrase_onehots = phrase_onehots.T

    return phrase_onehots