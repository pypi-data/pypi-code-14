from brite_etl.abstracts import Frame


class CommittedRevisions(Frame):

    _config = {
        'name': 'committed_revisions',
        'prepared': False
    }
