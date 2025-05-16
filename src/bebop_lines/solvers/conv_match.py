from __future__ import annotations

import torch

import bebop_lines.melody as line


class MotionAnalyzer(torch.nn.Module):
  def __init__(self, motion_instances : list[torch.Tensor], motion_weigths : list[float] | None=None):
    self.motion_instances = motion_instances

    if not isinstance(motion_weigths, list):
      motion_weigths = [1.0 for _ in self.motion_instances]

    self.motion_weights = motion_weigths

    module_list = []
    for kernel in self.motion_instances:
      module_list.append(torch.nn.Conv2d(1, 1, kernel.shape))
      module_list[-1].weight.data = kernel
      module_list[-1].weight.requires_grad = False
    self.module_list = torch.nn.ModuleList(module_list)

  def __forward__(self, phrase : line.PermutationPhrase) -> float:
    degree_phrase = torch.Tensor(phrase.degree_phrase)
    
    running_score = 0.0
    for module_index, convolution in enumerate(self.module_list):
      score_map = convolution(degree_phrase)

      score = torch.sum(score_map)
      score = float(score)

      score_weight = self.motion_weights[module_index]

      running_score += score_weight * score

      return running_score
