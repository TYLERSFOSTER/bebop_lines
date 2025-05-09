"""
Generate "bebop" lines from translated permutations, and save as MIDI
"""
from __future__ import annotations

import copy
import random

import numpy as np
import matplotlib.pyplot as plt
import mido
from mido import Message, MidiFile, MidiTrack

import bebop_lines.group_action as ga


class BebopLines():
  def __init__(self):
    self.permutations = ga.Permutations()
    
  def __getitem__(self, element_count):
    count = self.permutations[element_count]

    return count


  def bebop_lines(self, element_count, frame_count=12):
    permutations = self[element_count]
    random_permutations_A = []
    random_permutations_B = []
    random_permutations_C = []
    random_permutations_D = []
    for _ in range(100):
      permutation_A = random.choice(permutations)
      permutation_B = random.choice(permutations)
      permutation_C = random.choice(permutations)
      permutation_D = random.choice(permutations)

      random_permutations_A.append(permutation_A)
      random_permutations_B.append(permutation_B)
      random_permutations_C.append(permutation_C)
      random_permutations_D.append(permutation_D)

    bebop_lines_dict = {}

    for step_size in range(1, element_count):
      for idx in range(100):
        permutation_A = random_permutations_A[idx]
        permutation_B = random_permutations_B[idx]
        permutation_C = random_permutations_C[idx]
        permutation_D = random_permutations_D[idx]
        bebop_line = copy.deepcopy(permutation_A)

        for frame_idx in range(frame_count):
          if frame_idx < frame_count//4:
            translated_line = [p + (frame_idx + 1) * step_size for p in permutation_A]
          elif frame_count//4 <= frame_idx < 2 * frame_count//4:
            translated_line = [p + (frame_idx + 1) * step_size for p in permutation_B]
          elif 2 * frame_count//4 <= frame_idx < 3 * frame_count//4:
            translated_line = [p + (frame_count - frame_idx) * step_size for p in permutation_D]
          else:
            translated_line = [p + (frame_count - frame_idx) * step_size for p in permutation_D]

          bebop_line = bebop_line + translated_line

        bebop_lines_dict[tuple(permutation_A), tuple(permutation_B), step_size] = bebop_line
    
    return bebop_lines_dict


  def bebop_lines_single(self, element_count, frame_count=6):
    dict_of_lines = self.bebop_lines(element_count, frame_count=frame_count)
    
    single_line = [-69, -69, -69]
    for line_id in dict_of_lines:
      line = dict_of_lines[line_id]
      single_line = single_line + [-69, -69, -69] + line

    return single_line


  def save_MIDI(self, element_count, tonic=69, frame_count=5):
    concatenated_lines = self.bebop_lines_single(element_count, frame_count=frame_count)
    
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    
    bpm = 200
    ticks_per_beat = mid.ticks_per_beat
    microseconds_per_beat = mido.bpm2tempo(bpm)
    track.append(mido.MetaMessage('set_tempo', tempo=microseconds_per_beat))

    for note in concatenated_lines:
      note = note + tonic
      duration_secs = 0.1
      ticks = int(mido.second2tick(duration_secs, ticks_per_beat, microseconds_per_beat))
      track.append(Message('note_on', note=note, velocity=64, time=0))
      track.append(Message('note_off', note=note, velocity=64, time=ticks))

    mid.save('./bebop_lines/output.mid')

        



if __name__ == "__main__":
  permutations = Permutations()
  print(permutations[5])
  print(len(permutations.bebop_lines(3)))
  print(permutations.bebop_lines(3))

  dataset = permutations.bebop_lines(5)

  permutations.save_MIDI(5)

  # for key in dataset: 
  #   data = list(dataset[key])
  #   height = max(data) + 1
  #   width = len(data)

  #   img = np.ones((height, width))  # white background

  #   for x, y in enumerate(data):
  #       img[height - 1 - y, x] = 0  # black pixel at (x, y)

  #   plt.figure(figsize=(width, height))  # match fig size to pixel dims
  #   plt.imshow(img, cmap='gray', aspect='equal')
  #   plt.axis('off')
  #   plt.savefig(f"./bebop_lines/{key}_raster.png", dpi=300, bbox_inches='tight', pad_inches=0)
  #   plt.close()
