from brite_etl.abstracts import Frame


class CommittedRevisionsAll(Frame):

    _config = {
        'name': 'committed_revisions_all',
        'prepared': False
    }
