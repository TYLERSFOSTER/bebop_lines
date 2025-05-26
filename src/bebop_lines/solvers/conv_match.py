"""
Tool for detecting presence of hardcoded gestures within a phrase
"""
from __future__ import annotations

import torch

from bebop_lines.melody import PermutationPhrase
from bebop_lines.utils.data_convert import deg_to_char


class MotionAnalyzer(torch.nn.Module):
    """
    Evaluates symbolic musical phrases by convolving them with fixed motion
    pattern kernels.

    This module takes a list of 2D convolutional kernels (e.g., pattern
    detectors for musical gestures), applies them to a one-hot encoded
    representation of a musical phrase, and computes a weighted score
    based on how often each kernel activates above a given threshold.

    Args:
        motion_instances : A list of 2D convolution kernels representing motion patterns.
        motion_weights : Weights for each motion pattern's contribution to the score.
            Defaults to uniform weights if not provided or mismatched in length.
        threshhold : The activation threshold for kernel responses to count toward the score.
    """
    def __init__(
        self,
        motion_instances : list[torch.Tensor],
        motion_weights : list[float],
        threshhold : float=2.0,
    ):
        super().__init__()
        self.motion_instances = motion_instances

        if len(motion_weights) != len(motion_instances):
            motion_weights = [1.0 for _ in self.motion_instances]

        self.motion_weights = motion_weights

        self.module_list = torch.nn.ModuleList()
        for kernel in self.motion_instances:
            kernel_shape = kernel.shape

            self.module_list.append(torch.nn.Conv2d(1, 1, kernel_shape, stride=1, bias=False)) # type: ignore

            self.module_list[-1].weight.data = kernel.unsqueeze(0).unsqueeze(0)
            self.module_list[-1].weight.requires_grad = False # type: ignore

        self.threshold = threshhold

    def __len__(self):
        return len(self.module_list)

    def forward(self, phrase : PermutationPhrase) -> float:
        """
        Computes a motion score for a symbolic phrase using fixed motion kernels.

        Converts the given `PermutationPhrase` into a one-hot tensor, applies each fixed
        convolutional kernel, thresholds the result, and sums up the weighted number of activations.

        Args:
            phrase : A symbolic musical phrase containing a list of degree values.

        Returns:
            A scalar score measuring the total presence of the learned motion patterns in phrase.
        """
        phrase_onehots = deg_to_char(phrase.degree_phrase)

        running_score = 0.0
        for module_index, convolution in enumerate(self.module_list):
            score_map = convolution(phrase_onehots.float().unsqueeze(0).unsqueeze(0))
            score_map = score_map.squeeze(0).squeeze(0)

            score_map = score_map >= self.threshold
            score = torch.sum(score_map)
            score = float(score)

            score_weight = self.motion_weights[module_index]

            running_score += score_weight * score

        return running_score
