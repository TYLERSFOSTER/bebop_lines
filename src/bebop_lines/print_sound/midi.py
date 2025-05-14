from __future__ import annotations

from mido import Message, MidiFile, MidiTrack

import bebop_lines.melody as line
from bebop_lines.utils.gen_filenames import get_timestamped_filename
from bebop_lines.solvers.pivots import to_midi_velocity


def save_MIDI(phrase : line.PermutationPhrase, use_curve_amplitude=False):
  degree_phrase = phrase.degree_phrase
  duration_phrase = phrase.duration_phrase
  if use_curve_amplitude:
    velocity_phrase = to_midi_velocity(degree_phrase)
  else:
    velocity_phrase = [96 for _ in range(len(degree_phrase))]
  
  midi_file = MidiFile()
  track = MidiTrack()
  midi_file.tracks.append(track)

  for pitch, duration, velocity in zip(degree_phrase, duration_phrase, velocity_phrase):
    print("VELOCITY:", velocity)
    track.append(Message('note_on', note=pitch, velocity=velocity, time=3))
    track.append(Message('note_off', note=pitch, velocity=velocity, time=10 * duration))

  filename = get_timestamped_filename(prefix="line", ext="mid", outdir="outputs/midi")
  midi_file.save(filename)