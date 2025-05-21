from __future__ import annotations

import torch
import torch.nn.functional as F

import bebop_lines.melody as line


class MotionAnalyzer(torch.nn.Module):
  def __init__(
      self,
      motion_instances : list[torch.Tensor],
      motion_weights : list[float]=[],
      threshhold : float=2.0,
  ):
    super().__init__()
    self.motion_instances = motion_instances

    if len(motion_weights) != len(motion_instances):
      motion_weights = [1.0 for _ in self.motion_instances]

    self.motion_weights = motion_weights

    module_list = torch.nn.ModuleList()
    self.module_list = module_list
    for kernel in self.motion_instances:
      kernel_shape = kernel.shape

      self.module_list.append(torch.nn.Conv2d(1, 1, kernel_shape, stride=1, bias=False)) # type: ignore

      self.module_list[-1].weight.data = kernel.unsqueeze(0).unsqueeze(0)
      self.module_list[-1].weight.requires_grad = False # type: ignore
    
    self.threshold = threshhold

  def forward(self, phrase : line.PermutationPhrase) -> float: # type: ignore
    degree_phrase = torch.Tensor(phrase.degree_phrase)
    
    phrase_onehots = F.one_hot(
        degree_phrase.long(),
        num_classes=128,
    )
    phrase_onehots = phrase_onehots.T
    
    running_score = 0.0
    for module_index, convolution in enumerate(self.module_list):
      score_map = convolution(phrase_onehots.float().unsqueeze(0).unsqueeze(0))
      score_map = score_map.squeeze(0).squeeze(0)

      score_map = (score_map >= self.threshold)
      score = torch.sum(score_map)
      score = float(score)

      score_weight = self.motion_weights[module_index]

      running_score += score_weight * score

    return running_score
