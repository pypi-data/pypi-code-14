from __future__ import division
from .demographer import Demographer

class CensusGenderDemographer(Demographer):
    import re
    asciiex = re.compile(r'[a-zA-Z]+')
    name_key = 'gender'
    
    def __init__(self, dictionary_filename=None, classifier_filename=None, use_classifier=False, use_name_dictionary=True):
        import cPickle, os, sys
        # Load the dictionary
        self.name_dictionary = None
        self.classifier = None
        
        if use_name_dictionary:
            self.name_dictionary = load_name_dictionary(dictionary_filename)
            
        # Load the classifier.
        if use_classifier:
            if not classifier_filename:
                dir = os.path.dirname(sys.modules[__package__].__file__)
                filename = os.path.join(dir, 'data/gender_classifier.p')
            else:
                filename = classifier_filename
        
            with open(filename) as input:
                self.hasher = cPickle.load(input)
                self.classifier = cPickle.load(input)


    def process_tweet(self, tweet):
        user_info = tweet.get('user')
        name_string = user_info.get('name')
        
        return self._process_name(name_string)


    def _process_name(self, name_string):
        """Get something like a name from a string using a simple regex.
        """
        matcher = self.asciiex.search(name_string.split(' ')[0])
        if matcher:
            firstname = matcher.group(0)
            result = self._name_probability(firstname)
        else:
            result = []

        return {self.name_key : result}

    
    def _name_probability(self, first_name_anycase):
        """Given something from the name field, predict gender based on
        social security data from the US.

        In this simple version, we use raw counts and compute probabilities
        based on the percentage of male vs. female children registered
        with those names.
        """
        firstname = first_name_anycase.lower()
        result = []
        
        if self.name_dictionary and firstname in self.name_dictionary:
            f_ct = self.name_dictionary[firstname]['all']['F']
            m_ct = self.name_dictionary[firstname]['all']['M']
            tot = (f_ct + m_ct) * 1.0
            prob_f = f_ct / tot
            prob_m = m_ct / tot
            result.append({"value":"F", "prob":prob_f, "count":f_ct})
            result.append({"value":"M", "prob":prob_m, "count":m_ct})
        elif self.classifier:
            features = extract_gender_features(firstname)
            vector = self.hasher.transform([features])
            prediction = self.classifier.predict(vector)[0]
            score = self.classifier.decision_function(vector)[0]
            result.append({"value": prediction, "score": score })
            
            
        #Sort the list from most probable to least probable.
        result = sorted(result, key=lambda x:x.get("prob"))
        result.reverse()
        
        return result
        

#----------------------------------------
def load_name_dictionary(dictionary_filename):
    import cPickle, os, sys
    
    if not dictionary_filename:
        dir = os.path.dirname(sys.modules[__package__].__file__)
        filename = os.path.join(dir, 'data/census_gender_dct.p')
    else:
        filename = dictionary_filename
    
    with open(filename) as input:
        name_dictionary = cPickle.load(input)
    
    return name_dictionary
    

def extract_gender_features(word):
    """ Produce features for classification.
    If you choose to add new features, be sure to delete the pickled
    classifier (or the new features will not be used).
    """
    word = word.lower()
    features = {}

    # First and last n-grams.
    features['last_letter=%s' % word[-1]] = 1
    features['first_letter=%s' % word[0]] = 1

    if len(word)>1:
        features['first_2=%s' % word[:2]] = 1
        features['last_2=%s' % word[-2:]] = 1
    if len(word)>2:
        features['first_3=%s' % word[:3]] = 1
        features['last_3=%s' % word[-3:]] = 1
    if len(word)>3:
        features['first_4=%s' % word[:4]] = 1
        features['last_4=%s' % word[-4:]] = 1

    if word[0] in 'aeiou':
        features['starts_vowel'] = 1
    else:
        features['starts_consonant'] = 1
    
    if word[-1] in 'aeiou':
        features['ends_vowel'] = 1
    else:
        features['ends_consonant'] = 1
        
    # Whole name
    features['name=%s' % word] = 1

    return features
                

def create_census_gender_dict(data_path, dictionary_filename):
    from collections import defaultdict
    import csv, logging
    
    """Read in data, produce pickled dictionary.

    name_dict[NAME][YEAR][GENDER] = # NAME with GENDER in YEAR

    Example: name_dict[susan][1880][F] = #female susans in 1880

    Note: also includes count over all years -- example:
    name_dict[susan]['all'][F] = total # female susans from 1880-2014
    """

    years = range(1916, 2000)
    name_dict = defaultdict(defaultdict)
    logging.info('Reading from: %s' % data_path)
    for year in years:
        try:
            file = open(data_path + 'yob%s.txt' % year)
            CSV_file = csv.reader(file)
        except:
            import sys
            err_msg = "Error: Data failed to load, please check that " +\
                     "name data is in data directory.\n"
            logging.critical(err_msg)
            sys.exit(err_msg)
            
        for line in CSV_file:
            name, gender, count = line
            name = name.lower()
            count = int(count)
            if year not in name_dict[name]:
                name_dict[name][year] = {'F':0,'M':0}
            name_dict[name][year][gender] = count
        
        file.close()
        

    for name in name_dict:
        f_ct, m_ct = 0, 0
        for year in name_dict[name]:
            f_ct += name_dict[name][year]['F']
            m_ct += name_dict[name][year]['M']

        name_dict[name]['all'] = {'F':f_ct,'M':m_ct}

    logging.info('Saving to %s' % dictionary_filename)
    with open(dictionary_filename, 'w') as writer:
        import cPickle
        cPickle.dump(name_dict, writer)

  
def train_gender_classifier(classifier_filename, dictionary_filename=None):
    '''
    Train a classifier based on the given data.
    If you choose to change the classifier (or features), be sure to delete
    the pickled classifier, or you will not see changes to your model.
    '''
    import random, logging, cPickle
    from sklearn.feature_extraction import FeatureHasher
    from sklearn.linear_model import SGDClassifier
    #from sklearn.grid_search import GridSearchCV
    
    logging.info('Loading name dictionary')
    name_dictionary = load_name_dictionary(dictionary_filename)

    unique_features = set()
    
    train_set = []
    for name in name_dictionary:
        vals = name_dictionary[name]['all']
        label = 'M'

        # Label name by gender more frequently associated with it.
        if vals['F'] > vals['M']:
            label = 'F'
            
        features_dict = extract_gender_features(name)
                    
        unique_features.update(features_dict.keys())
        
        train_set.append((features_dict, label))
    
    # Convert to sklearn instances
    hasher = FeatureHasher(n_features=len(unique_features) * 2)
    
    random.seed(0)
    random.shuffle(train_set)
    
    train_features = [features_dict for features_dict, label in train_set]
    train_labels = [label for features_dict, label in train_set]
    
    train_vectors = hasher.transform(train_features)
    
    logging.info('Training')
    parameters={'alpha':[0.000001, 10]}
    classifier = SGDClassifier(loss='hinge', penalty='l2')
    classifier.fit(train_vectors, train_labels)

    '''
    gs = GridSearchCV(classifier, parameters)
    gs.fit(train_vectors, train_labels)
    classifier = gs.best_estimator_
    logging.info('Selected alpha=%s' % str(gs.best_params_['alpha']))
    '''
    
    from sklearn.metrics import accuracy_score
    logging.info('Train accuracy: %.4f' % accuracy_score(train_labels, classifier.predict(train_vectors)))
    
    logging.info('Saving classifier to %s' % classifier_filename)
    with open(classifier_filename, 'w') as writer:
        cPickle.dump(hasher, writer)
        cPickle.dump(classifier, writer)
    
