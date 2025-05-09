from __future__ import annotations

import copy

import numpy as np
import mido
from mido import Message, MidiFile, MidiTrack

import bebop_lines.group_action as ga


def save_MIDI(element_count, tonic=69, frame_count=5):
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