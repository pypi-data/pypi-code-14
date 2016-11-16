__version__ = '0.1.0'


from .gender import CensusGenderDemographer

default_demographers = None


def process_tweet(tweet, demographers = None):
    """Process a single tweet (json format) and return a dictionary whose keys
    are demographic attributes and whose entries are lists of predictions.
    """
    global default_demographers
    
    if not demographers:
        if not default_demographers:
            default_demographers = [CensusGenderDemographer(use_classifier=True)]
        demographers = default_demographers

    result = []
    for demographer in demographers:
        result.append(demographer.process_tweet(tweet))

    return result
