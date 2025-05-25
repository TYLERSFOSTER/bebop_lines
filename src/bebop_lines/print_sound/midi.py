"""
Safe PermutationPhrase instance as MIDI file
"""
from __future__ import annotations

from mido import Message, MidiFile, MidiTrack

from bebop_lines.melody import PermutationPhrase
from bebop_lines.utils.gen_filenames import get_timestamped_filename
from bebop_lines.solvers.pivots import pivot_score, to_midi_velocity


def save_midi(phrase : PermutationPhrase, use_curve_amplitude : bool=False):
	"""
	Converts a `PermutationPhrase` instance, with pitch and duration data, into
	a single-track MIDI file and saves it to disk with a timestamped filename.
	
	If `use_curve_amplitude` is True, note velocities are dynamically assigned based
	on the local curvature (pivot score) of the pitch sequence. Otherwise, all notes
	are given a fixed velocity of 96.

	Args:
			phrase : A musical phrase object containing `degree_phrase`
					(a list of MIDI note numbers) and `duration_phrase` (a list of durations).
			use_curve_amplitude : If True, use pivot score to compute note
					velocities. If False, use a constant velocity. Defaults to False.

	Saves:
			A `.mid` file in the "outputs/midi" directory, with a filename prefixed by "line"
			and suffixed with a timestamp.
	"""
	degree_phrase = phrase.degree_phrase
	duration_phrase = phrase.duration_phrase
	if use_curve_amplitude:
		pivot_score_list = pivot_score(degree_phrase)
		velocity_phrase = to_midi_velocity(pivot_score_list)
	else:
		velocity_phrase = [96 for _ in range(len(degree_phrase))]

	midi_file = MidiFile()
	track = MidiTrack()
	midi_file.tracks.append(track)

	for pitch, duration, velocity in zip(degree_phrase, duration_phrase, velocity_phrase):
		track.append(Message('note_on', note=pitch, velocity=velocity, time=3))
		track.append(Message('note_off', note=pitch, velocity=velocity, time=10 * duration))

	filename = get_timestamped_filename(prefix="line", ext="mid", outdir="outputs/midi")
	midi_file.save(filename)
