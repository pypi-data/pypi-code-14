from copy import copy

from rv.api import NOTECMD, Note, Pattern, Project, read_sunvox_file


OFF = Note(note=NOTECMD.NOTE_OFF)


class PatternPolyphonist(object):

    def __init__(self, project):
        if isinstance(project, str):
            project = read_sunvox_file(project)
        elif not isinstance(project, Project):
            raise ValueError('Must provide a path or a Project instance')
        self.project = project

    @property
    def pattern_count(self):
        return sum(1 for p in self.project.patterns if p is not None)

    @property
    def is_compatible(self):
        # TODO: make sure there are no prev-track commands
        return all(pattern.tracks <= 4
                   for pattern in self.project.patterns
                   if pattern is not None)

    @property
    def module_numbers(self):
        found = set(
            note.module - 1
            for pattern in self.project.patterns if pattern
            for line in pattern.data
            for note in line if note.module != 0
        )
        return list(sorted(found))

    def polyphonized_pattern(self, pattern, mono_module, poly_module,
                             min_voice, max_voice):
        poly_pattern = Pattern(
            name=pattern.name,
            tracks=pattern.tracks * 4,
            lines=pattern.lines,
            y_size=pattern.y_size,
            appearance_flags=pattern.appearance_flags,
            icon=pattern.icon,
            fg_color=pattern.fg_color,
            bg_color=pattern.bg_color,
            flags=pattern.flags,
            x=pattern.x,
            y=pattern.y,
        )
        voices = [
            dict(
                last_track=None,
                last_offset=None,
            )
            for x in range(max_voice - min_voice + 1)
        ]
        tracks = [
            dict(
                last_offset=None,
                last_module=None,
                last_voice=None,
            )
            for x in range(pattern.tracks)
        ]
        current_voice = 0
        for lineno, line in enumerate(pattern.data):
            for trackno, note in enumerate(line):
                track = tracks[trackno]
                note_offset = track['last_offset'] or 0
                off_offset = (note_offset + 1) % 2
                note_meta_track = trackno * 4 + note_offset * 2
                note_track = note_meta_track + 1
                off_meta_track = trackno * 4 + off_offset * 2
                off_track = off_meta_track + 1
                last_track_note_was_poly = track['last_module'] == mono_module
                this_note_is_poly = note.module - 1 == mono_module
                last_voice = \
                    voices[track['last_voice']] \
                    if track['last_voice'] \
                    else None
                voice_not_reallocated = (
                    not last_voice or
                    last_voice['last_track'] == trackno
                )
                poly_line = poly_pattern.data[lineno]
                if note.note == NOTECMD.NOTE_OFF:
                    if not last_track_note_was_poly:
                        poly_line[note_track] = copy(note)
                    elif last_track_note_was_poly and voice_not_reallocated:
                        poly_line[note_track] = copy(note)
                        note_meta = poly_line[note_meta_track]
                        note_meta.module = poly_module + 1
                        note_meta.controller = 2
                        note_meta.val = current_voice + min_voice
                        voices[current_voice]['last_track'] = None
                elif note.note != NOTECMD.EMPTY:
                    poly_line[off_track] = copy(OFF)
                    if last_track_note_was_poly and voice_not_reallocated:
                        off_meta = poly_line[off_meta_track]
                        off_meta.module = poly_module + 1
                        off_meta.controller = 2
                        off_meta.val = track['last_voice'] + min_voice
                    if this_note_is_poly:
                        note_note = poly_line[note_track] = copy(note)
                        note_note.module = poly_module + 1
                        note_meta = poly_line[note_meta_track]
                        note_meta.module = poly_module + 1
                        note_meta.controller = 2
                        note_meta.val = current_voice + min_voice
                        track['last_voice'] = current_voice
                        voices[current_voice]['last_track'] = trackno
                    else:
                        note_note = poly_line[note_track] = copy(note)
                        track['last_voice'] = None
                    track['last_offset'] = off_offset
                    track['last_module'] = note.module - 1
                    current_voice += 1
                    current_voice %= len(voices)
        return poly_pattern

    def polyphonized_project(self, mono_module, poly_module,
                             min_voice, max_voice):
        poly_project = Project()
        for pattern in self.project.patterns:
            if pattern:
                poly_project.attach_pattern(
                    self.polyphonized_pattern(
                        pattern=pattern,
                        mono_module=mono_module,
                        poly_module=poly_module,
                        min_voice=min_voice,
                        max_voice=max_voice,
                    )
                )
        return poly_project
