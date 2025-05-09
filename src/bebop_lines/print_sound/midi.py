from __future__ import annotations

import copy

import numpy as np
import mido
from mido import Message, MidiFile, MidiTrack

import bebop_lines.group_action as ga


def save_MIDI(pitch_phrase, duration_phrase, tonic=69):
  concatenated_lines = self.bebop_lines_single(element_count, frame_count=frame_count)
  
  mid = MidiFile()
  track = MidiTrack()
  mid.tracks.append(track)
  
  bpm = 200
  ticks_per_beat = mid.ticks_per_beat
  # microseconds_per_beat = mido.bpm2tempo(bpm)
  # track.append(mido.MetaMessage('set_tempo', tempo=microseconds_per_beat))

  running_clock = 0.0
  for pitch, duration in zip(pitch_phrase, duration_phrase):
    note = pitch + tonic

    track.append(Message('note_on', note=note, velocity=64, time=running_clock))
    
    running_clock = running_clock + duration
    track.append(Message('note_off', note=note, velocity=64, time=running_clock))

  mid.save('./bebop_lines/output.mid')