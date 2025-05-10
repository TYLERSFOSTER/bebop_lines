## TODOs

### [ ] Refactor `melody_builder.py` for modularity
- **Reason**: Current implementation mixes pitch generation and rhythmic structure
- **Proposal**: Split into `pitch_generator.py` and `rhythm_generator.py`
- **Priority**: Medium
- **Owner**: @tyler
- **Notes**:
  - Might impact existing tests in `test_melody_builder.py`
  - Consider designing around a `MelodicCell` abstraction

---

### [ ] Add CLI interface for rendering output
- **Reason**: Allow users to generate MIDI/WAV from terminal without writing scripts
- **Status**: Blocked on `render_engine` refactor
