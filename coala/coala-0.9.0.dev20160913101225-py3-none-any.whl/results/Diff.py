import copy
import difflib

from coalib.results.LineDiff import LineDiff, ConflictError
from coalib.results.SourceRange import SourceRange
from coala_utils.decorators import enforce_signature, generate_eq


@generate_eq("_file", "modified", "rename", "delete")
class Diff:
    """
    A Diff result represents a difference for one file.
    """

    def __init__(self, file_list, rename=False, delete=False):
        """
        Creates an empty diff for the given file.

        :param file_list: The original (unmodified) file as a list of its
                          lines.
        :param rename:    False or str containing new name of file.
        :param delete:    True if file is set to be deleted.
        """
        self._changes = {}
        self._file = file_list
        self.rename = rename
        self.delete = delete

    @classmethod
    def from_string_arrays(cls, file_array_1, file_array_2, rename=False):
        """
        Creates a Diff object from two arrays containing strings.

        If this Diff is applied to the original array, the second array will be
        created.

        :param file_array_1: Original array
        :param file_array_2: Array to compare
        :param rename:       False or str containing new name of file.
        """
        result = cls(file_array_1, rename=rename)

        matcher = difflib.SequenceMatcher(None, file_array_1, file_array_2)
        # We use this because its faster (generator) and doesn't yield as much
        # useless information as get_opcodes.
        for change_group in matcher.get_grouped_opcodes(1):
            for (tag,
                 a_index_1,
                 a_index_2,
                 b_index_1,
                 b_index_2) in change_group:
                if tag == "delete":
                    for index in range(a_index_1+1, a_index_2+1):
                        result.delete_line(index)
                elif tag == "insert":
                    # We add after line, they add before, so dont add 1 here
                    result.add_lines(a_index_1,
                                     file_array_2[b_index_1:b_index_2])
                elif tag == "replace":
                    result.change_line(a_index_1+1,
                                       file_array_1[a_index_1],
                                       file_array_2[b_index_1])
                    result.add_lines(a_index_1+1,
                                     file_array_2[b_index_1+1:b_index_2])
                    for index in range(a_index_1+2, a_index_2+1):
                        result.delete_line(index)

        return result

    @classmethod
    def from_clang_fixit(cls, fixit, file):
        """
        Creates a Diff object from a given clang fixit and the file contents.

        :param fixit: A cindex.Fixit object.
        :param file:  A list of lines in the file to apply the fixit to.
        :return:      The corresponding Diff object.
        """
        assert isinstance(file, (list, tuple))

        oldvalue = '\n'.join(file[fixit.range.start.line-1:
                                  fixit.range.end.line])
        endindex = fixit.range.end.column - len(file[fixit.range.end.line-1])-1

        newvalue = (oldvalue[:fixit.range.start.column-1] +
                    fixit.value +
                    oldvalue[endindex:])
        new_file = (file[:fixit.range.start.line-1] +
                    type(file)(newvalue.splitlines(True)) +
                    file[fixit.range.end.line:])

        return cls.from_string_arrays(file, new_file)

    def _get_change(self, line_nr, min_line=1):
        if not isinstance(line_nr, int):
            raise TypeError("line_nr needs to be an integer.")
        if line_nr < min_line:
            raise ValueError("The given line number is not allowed.")

        return self._changes.get(line_nr, LineDiff())

    def stats(self):
        """
        Returns tuple containing number of additions and deletions in the diff.
        """
        additions = 0
        deletions = 0
        for line_diff in self._changes.values():
            if line_diff.change:
                additions += 1
                deletions += 1
            elif line_diff.delete:
                deletions += 1
            if line_diff.add_after:
                additions += len(line_diff.add_after)
        return additions, deletions

    def __len__(self):
        """
        Returns total number of additions and deletions in diff.
        """
        return sum(self.stats())

    @property
    def rename(self):
        """
        :return: string containing new name of the file.
        """
        return self._rename

    @rename.setter
    @enforce_signature
    def rename(self, rename: (str, False)):
        """
        :param rename: False or string containing new name of file.
        """
        self._rename = rename

    @property
    def delete(self):
        """
        :return: True if file is set to be deleted.
        """
        return self._delete

    @delete.setter
    @enforce_signature
    def delete(self, delete: bool):
        """
        :param delete: True if file is set to be deleted, False otherwise.
        """
        self._delete = delete

    @property
    def original(self):
        """
        Retrieves the original file.
        """
        return self._file

    @property
    def modified(self):
        """
        Calculates the modified file, after applying the Diff to the original.
        """
        result = []

        if self.delete:
            return result

        current_line = 0

        # Note that line_nr counts from _1_ although 0 is possible when
        # inserting lines before everything
        for line_nr in sorted(self._changes):
            result.extend(self._file[current_line:max(line_nr-1, 0)])
            linediff = self._changes[line_nr]
            if not linediff.delete and not linediff.change and line_nr > 0:
                result.append(self._file[line_nr-1])
            elif linediff.change:
                result.append(linediff.change[1])

            if linediff.add_after:
                result.extend(linediff.add_after)

            current_line = line_nr

        result.extend(self._file[current_line:])

        return result

    @property
    def unified_diff(self):
        """
        Generates a unified diff corresponding to this patch.

        Note that the unified diff is not deterministic and thus not suitable
        for equality comparison.
        """
        return ''.join(difflib.unified_diff(
            self.original,
            self.modified,
            tofile=self.rename if isinstance(self.rename, str) else ''))

    def __json__(self):
        """
        Override JSON export, using the unified diff is the easiest thing for
        the users.
        """
        return self.unified_diff

    def affected_code(self, filename):
        """
        Creates a list of SourceRange objects which point to the related code.
        Changes on continuous lines will be put into one SourceRange.

        :param filename: The filename to associate the SourceRange's to.
        :return:         A list of all related SourceRange objects.
        """
        return list(diff.range(filename)
                    for diff in self.split_diff(distance=0))

    def split_diff(self, distance=1):
        """
        Splits this diff into small pieces, such that several continuously
        altered lines are still together in one diff. All subdiffs will be
        yielded.

        A diff like this with changes being together closely won't be splitted:

        >>> diff = Diff.from_string_arrays([     'b', 'c', 'e'],
        ...                                ['a', 'b', 'd', 'f'])
        >>> len(list(diff.split_diff()))
        1

        If we set the distance to 0, it will be splitted:

        >>> len(list(diff.split_diff(distance=0)))
        2

        If a negative distance is given, every change will be yielded as an own
        diff, even if they are right beneath each other:

        >>> len(list(diff.split_diff(distance=-1)))
        3

        If a file gets renamed or deleted only, it will be yielded as is:

        >>> len(list(Diff([], rename='test').split_diff()))
        1

        An empty diff will not yield any diffs:

        >>> len(list(Diff([]).split_diff()))
        0

        :param distance: Number of unchanged lines that are allowed in between
                         two changed lines so they get yielded as one diff.
        """
        if not self:
            return

        last_line = -1
        this_diff = Diff(self._file, rename=self.rename, delete=self.delete)
        for line in sorted(self._changes.keys()):
            if line > last_line + distance + 1 and len(this_diff._changes) > 0:
                yield this_diff
                this_diff = Diff(self._file, rename=self.rename,
                                 delete=self.delete)

            last_line = line
            this_diff._changes[line] = self._changes[line]

        # If the diff contains no line changes, the loop above will not be run
        # else, this_diff will never be empty and thus this has to be yielded
        # always.
        yield this_diff

    def range(self, filename):
        """
        Calculates a SourceRange spanning over the whole Diff. If something is
        added after the 0th line (i.e. before the first line) the first line
        will be included in the SourceRange.

        The range of an empty diff will only affect the filename:

        >>> range = Diff([]).range("file")
        >>> range.file is None
        False
        >>> print(range.start.line)
        None

        :param filename: The filename to associate the SourceRange with.
        :return:         A SourceRange object.
        """
        if len(self._changes) == 0:
            return SourceRange.from_values(filename)

        start = min(self._changes.keys())
        end = max(self._changes.keys())
        return SourceRange.from_values(filename,
                                       start_line=max(1, start),
                                       end_line=max(1, end))

    def __add__(self, other):
        """
        Adds another diff to this one. Will throw an exception if this is not
        possible. (This will *not* be done in place.)
        """
        if not isinstance(other, Diff):
            raise TypeError("Only diffs can be added to a diff.")

        if self.rename != other.rename and False not in (self.rename,
                                                         other.rename):
            raise ConflictError("Diffs contain conflicting renamings.")

        result = copy.deepcopy(self)
        result.rename = self.rename or other.rename
        result.delete = self.delete or other.delete

        for line_nr in other._changes:
            change = other._changes[line_nr]
            if change.delete is True:
                result.delete_line(line_nr)
            if change.add_after is not False:
                result.add_lines(line_nr, change.add_after)
            if change.change is not False:
                result.change_line(line_nr, change.change[0], change.change[1])

        return result

    def __bool__(self):
        """
        >>> bool(Diff([]))
        False
        >>> bool(Diff([], rename="some"))
        True
        >>> bool(Diff([], delete=True))
        True
        >>> bool(Diff.from_string_arrays(['1'], []))
        True

        :return: False if the patch has no effect at all when applied.
        """
        return (self.rename is not False or
                self.delete is True or
                len(self._changes) > 0)

    def delete_line(self, line_nr):
        """
        Mark the given line nr as deleted. The first line is line number 1.
        """
        linediff = self._get_change(line_nr)
        linediff.delete = True
        self._changes[line_nr] = linediff

    def delete_lines(self, line_nr_start, line_nr_end):
        """
        Delete lines in a specified range, inclusively.
        """
        for line_nr in range(line_nr_start, line_nr_end + 1):
            self.delete_line(line_nr)

    def add_lines(self, line_nr_before, lines):
        """
        Adds lines after the given line number.

        :param line_nr_before: Line number of the line before the additions.
                               Use 0 for insert lines before everything.
        :param lines:          A list of lines to add.
        """
        if lines == []:
            return  # No action

        linediff = self._get_change(line_nr_before, min_line=0)
        if linediff.add_after is not False:
            raise ConflictError("Cannot add lines after the given line since "
                                "there are already lines.")

        linediff.add_after = lines
        self._changes[line_nr_before] = linediff

    def change_line(self, line_nr, original_line, replacement):
        """
        Changes the given line with the given line number. The replacement will
        be there instead.
        """
        linediff = self._get_change(line_nr)
        if linediff.change is not False and linediff.change[1] != replacement:
            raise ConflictError("An already changed line cannot be changed.")

        linediff.change = (original_line, replacement)
        self._changes[line_nr] = linediff
