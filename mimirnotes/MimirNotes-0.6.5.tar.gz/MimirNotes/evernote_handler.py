import datetime
from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
from evernote.edam.error.ttypes import EDAMUserException, EDAMErrorCode, EDAMSystemException
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec


class EvernoteHandler(object):

    def __init__(self):
        self.client = None
        self.token = None

    def connect_to_evernote(self, auth_token):
        user = None
        self.token = auth_token

        try:
            print '[Establishing connection to Evernote...]'
            self.client = EvernoteClient(token=auth_token,
                                         sandbox=False)
            self.user_store = self.client.get_user_store()
            user = self.user_store.getUser()
        except (EDAMUserException, EDAMSystemException) as ex:
            error = ex.errorCode
            print("[Error attempting to authenticate with Evernote: {}]".format(EDAMErrorCode._VALUES_TO_NAMES[error]))
            return False

        if user:
            print "[Authenticated to Evernote as user {}]".format(user.username)
            return True
        else:
            return False

    def _get_notebooks(self):
        note_store = self.client.get_note_store()
        notebooks = note_store.listNotebooks()
        return {n.name: n for n in notebooks}

    def _create_notebook(self, notebook):
        note_store = self.client.get_note_store()
        return note_store.createNotebook(notebook)

    def _update_notebook(self, notebook):
        note_store = self.client.get_note_store()
        note_store.updateNotebook(notebook)
        return

    def _check_and_make_notebook(self, notebook_name, stack=None):
        notebooks = self._get_notebooks()
        if notebook_name in notebooks:
            # This notebook already exists
            print "[Notebook found!]"
            notebook = notebooks[notebook_name]
            if stack:
                notebook.stack = stack
                self._update_notebook(notebook)
            return notebook
        else:
            # Notebook does not exist, so create  new one
            print "[Notebook not found...creating]"
            notebook = Types.Notebook()
            notebook.name = notebook_name
            if stack:
                notebook.stack = stack
            notebook = self._create_notebook(notebook)
            return notebook

    def create_note(self, notebook, filename=None, notes_data=None):
        note = Types.Note()
        note.title = "Synced Mimir Notes [{}]".format(datetime.datetime.now())
        note.notebookGuid = notebook.guid

        note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>'
        for note_line in notes_data:
            note.content += note_line + '<br /><br />'
        note.content += '</en-note>'

        return note

    def upload_to_notebook(self, notebook_name, notes_data=None):
        # First check that evernote notebook exists; if not, create it
        print "[Checking for existance of notebook {}]".format(notebook_name)
        notebook = self._check_and_make_notebook(notebook_name)

        print "[Uploading mimir notes to {}]".format(notebook_name)

        try:
            note_store = self.client.get_note_store()
            note_filter = NoteFilter()
            note_filter.notebookGuid = notebook.guid
            spec = NotesMetadataResultSpec()
            search_results = note_store.findNotesMetadata(self.token, note_filter, 0, 10, spec)
            print "[Re-syncing all notes. Removing {} old notes]".format(len(search_results.notes))
            for note in search_results.notes:
                note_store.deleteNote(note.guid)

            note = self.create_note(notebook, notes_data=notes_data)

            # Finally, store the note
            note_store = self.client.get_note_store()
            note = note_store.createNote(note)

            print "[Mimir notes successfully synced to Evernote notebook {}!]".format(notebook_name)
        except Exception as ex:
            print "[Something went wrong while attempting to sync...{}]".format(ex)

    @staticmethod
    def _parse_query_string(authorize_url):
        uargs = authorize_url.split('?')
        vals = {}
        if len(uargs) == 1:
            raise Exception('Invalid Authorization URL')
        for pair in uargs[1].split('&'):
            key, value = pair.split('=', 1)
            vals[key] = value

        return vals

    def oauth(self, consumer_key, consumer_secret):
        try:
            client = EvernoteClient(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                sandbox=False
            )

            request_token = client.get_request_token('http://localhost')

            print "Paste this URL into your browser and login:"
            print '\t'+ client.get_authorize_url(request_token)
            print '-----'

            print 'Paste the URL after login here:'
            auth_url = raw_input()

            vals = self._parse_query_string(auth_url)

            auth_token = client.get_access_token(
                request_token['oauth_token'],
                request_token['oauth_token_secret'],
                vals['oauth_verifier']
            )

            client = EvernoteClient(token=auth_token,
                                    sandbox=False)

            # Test the new auth token to ensure it works
            user_store = client.get_user_store()
            user = user_store.getUser()

            print "Tokens successfully generated for user {}".format(user.username)
            print "Your Evernote auth_token: {}".format(auth_token)
            print "Your Evernote oauth_token: {}".format(request_token['oauth_token'])
            print "Paste the above tokens into .mimir/.mimir-config under the 'evernote_auth_token' and evernote_oaith_token settings."
        except Exception as ex:
            print "[Something went wrong trying to generate an auth token! Message: {}]".format(ex)