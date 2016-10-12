import json
import os

import shutil

import datetime
import subprocess
import tempfile


class MimirHandler:

    def __init__(self):
        self.working_dir = os.getcwd()
        self.mimir_dir = self.working_dir + '/.mimir'
        self.config_name = '.mimir_config'
        self.config_location = self.mimir_dir + '/' + self.config_name
        self.notes_name = 'mimir_notes.txt'
        self.notes_location = self.mimir_dir + '/' + self.notes_name
        self.tmp_note_location = self.mimir_dir + '/tmp'

    def handle(self, action, **kwargs):
        """
        Handles a given action by building a function to call for the action
        :param action:
        :return:
        """
        action_handler = '_' + action
        handler = getattr(self, action_handler)
        handler(**kwargs)

    def _init(self, **kwargs):
        """
        Initialize a new mimir, creating a .mimir directory, an initial configuration file, and a notes file
        :return:
        """
        print 'Initializing mimir in {}...'.format(self.working_dir)
        try:
            if not os.path.exists(self.mimir_dir):
                # Attempt to make the .mimir directory in the current working directory
                os.makedirs(self.mimir_dir)
                os.makedirs(self.tmp_note_location)

                # Setup the base configuration dictionary. This will be written to the config file as json. The user
                # will have control over editing these settings.
                config = {"editor":"", "tag_symbol": "@", "encrypt":False}

                # If the above directory creation succeeded, attempt to create the base configuration file
                # (.mimir/.mimir_config)
                with open(self.config_location, 'w+') as f:
                    json.dump(config, f, indent=4)

                # Finally, create the actual notes file
                with open(self.notes_location, 'w+') as f:
                    current_time = datetime.datetime.now()
                    f.write('{:%Y-%m-%d %H:%M} :: MimirNotes initialized.'.format(current_time))

                print 'Successfully created a new mimir at {}'.format(self.mimir_dir)
            else:
                print 'A mimir directory already exists at {}! Aborting...'.format(self.mimir_dir)
                return
        except OSError as ex:
            print 'Something went wrong during initialization...'

    def _delete(self, **kwargs):
        """
        Delete any found mimirs in the given directory.
        :return:
        """
        try:
            if os.path.exists(self.mimir_dir):
                print 'Deleting mimir at {}'.format(self.mimir_dir)
                shutil.rmtree(self.mimir_dir)
            else:
                print 'No mimir found!'
        except OSError as ex:
            print 'Something went wrong attempting to delete this mimir...'

    def _new(self, **kwargs):
        """
        Create a new note entry in the mimir_notes.txt file
        :return:
        """
        # Check to ensure that all the requisite files/dirs exists before continuing
        if self.does_mimir_exist():
            note = kwargs['note']

            # If the note is a single word, it will be passed from Click as a string, if it was several words, it comes
            # across as a tuple, and we need to combine the elements to be coherent
            if isinstance(note, tuple):
                note = ' '.join(map(str, kwargs['note']))

            with open(self.notes_location, 'a') as f:
                f.write('\n\n')
                current_time = datetime.datetime.now()
                f.write('{:%Y-%m-%d %H:%M} :: {}'.format(current_time, note))

            self.clean_notes_file()
            print '[Entry added to mimir at {}]'.format(self.mimir_dir)

    def _editor_new(self, **kwargs):
        """
        Create a new entry using the default editor
        :param kwargs:
        :return:
        """
        if self.does_mimir_exist():
            with open(self.config_location) as config:
                config_options = json.load(config)

            if config_options['editor'] != '':
                temp_note = tempfile.NamedTemporaryFile(delete=False, suffix='.txt', dir=self.tmp_note_location)
                print temp_note.name
                p = subprocess.Popen((config_options['editor'], temp_note.name))
                p.wait()

                with open(temp_note.name) as f:
                    note = ''
                    for line in f:
                        note += line
                    self._new(note=note)

                os.remove(temp_note.name)
            else:
                self.editor_not_set()

    def _show(self, **kwargs):
        """
        Show the last n notes, where n is the value passed in from the -s flag
        :return:
        """
        if self.does_mimir_exist():
            amount_to_return = kwargs['num']
            with open(self.notes_location, 'r') as f:
                index = 0
                count = 0
                returned_notes = []
                for line in f:
                    # Skip the first two lines of the file, they merely record when the mimir was created
                    if index == 0 or index == 1:
                        index += 1
                        continue

                    if line != '\n':
                        returned_notes.append(line.rstrip())
                    else:
                        count += 1

                        if count >= amount_to_return and amount_to_return is not 0:
                            break
                    index += 1

                for note in returned_notes:
                    print str(note)

    def _edit(self, **kwargs):
        """
        Allows editing the mimir_notes.txt file, where all notes are stored. If a line is changed or deleted, the
        user is notified of this upon closing/saving the file.
        :param kwargs:
        :return:
        """
        if self.does_mimir_exist():
            with open(self.config_location) as config:
                config_options = json.load(config)

            if config_options['editor'] != '':
                print '[Opening {} in {}]'.format(self.notes_location, config_options['editor'])

                with open(self.notes_location, 'r') as f:
                    original_lines = f.readlines()

                initial_notes_count = self.count_notes()
                p = subprocess.Popen((config_options['editor'   ], self.notes_location))
                p.wait()

                # Clean up any whitespace left over from deleting/editing notes
                self.clean_notes_file()

                # Calculate which notes (if any) were edited, by check each line of the original file with the
                # changed file for similarity.
                with open(self.notes_location, 'r') as f:
                    new_lines = f.readlines()
                same = set(original_lines).intersection(new_lines)
                # Toss out new lines, those will always be the same
                same.discard('\n')

                new_notes_count = self.count_notes()
                deleted_notes_count = initial_notes_count - new_notes_count

                # Calculate the edited notes count. We need to subract one from the length here, to account for the
                # header note that is always present (but not technically a note).
                edited_notes_count = new_notes_count - (len(same) - 1)

                if edited_notes_count > 0:
                    print '[Edited {} notes successfully.]'.format(edited_notes_count)
                if deleted_notes_count > 0:
                    print '[Deleted {} notes successfully.]'.format(deleted_notes_count)

                if edited_notes_count == 0 and deleted_notes_count == 0:
                    print '[No changes to notes file detected.]'

            else:
                self.editor_not_set()

    def _status(self, **Kwargs):
        """
        Return the status information on the current mimir
        :param Kwargs:
        :return:
        """
        if self.does_mimir_exist():
            with open(self.notes_location, 'r') as f:
                status_line = f.readline()
                date_init = status_line.split("::")[0]
                print 'MimirNotes intialized on {}'.format(date_init)
            print 'Entries count: {}'.format(self.count_notes())

    def does_mimir_exist(self):
        """
        Check for the existence of a mimir, mimir config, and notes file
        :return:
        """
        if os.path.exists(self.mimir_dir) and os.path.exists(self.notes_location) and os.path.exists(self.config_location):
            return True
        else:
            print '[No mimir found, or files missing...are you sure you are in the correct dir? ({})]'\
                .format(self.working_dir)
            print '[To create a new mimir, run `mimir init`]'
            return False

    def count_notes(self):
        """
        Counts the total of all notes in the current mimir
        :return: int The count of all notes in the current mimir
        """
        if self.does_mimir_exist():
            with open(self.notes_location, 'r') as f:
                index = 0
                count = 0
                for line in f:
                    # Skip the first two lines of the file, they merely record when the mimir was created
                    if index == 0 or index == 1:
                        index += 1
                        continue

                    if line != '\n':
                        count += 1
                    index += 1

            return count

    def clean_notes_file(self):
        """
        Cleans up the notes file after editing (removes extra whitespace, primarily)
        :return:
        """
        if self.does_mimir_exist():
            # Open the notes files, and read in all the lines, we'll use these later to recreate the file with extra
            # blank lines deleted
            with open(self.notes_location, 'r') as f:
                lines = f.readlines()

            # Now, read through each line (Except the first two), check the line above it to see if its a newline.
            # If the line above is a new line, and the current line is a new line, delete, as it is an extra new line=
            with open(self.notes_location, 'w') as f:
                previous_line = ''
                index = 0
                for line in lines:
                    # Skip the first two lines of the file, they merely record when the mimir was created
                    if index == 0 or index == 1:
                        f.write(line)
                        previous_line = line
                        index += 1
                        continue

                    if previous_line == '\n' and line == '\n':
                        pass
                    else:
                        f.write(line)

                    previous_line = line
                    index += 1

    def editor_not_set(self):
        print '[Default editor not set! Set default editor in mimir config ({}).]'.format(self.config_location)

    @staticmethod
    def handler_not_found():
        print 'Handler not found!'





