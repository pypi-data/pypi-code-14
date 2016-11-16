from .demographer import Demographer

class GenderCDemographer(Demographer):
    import re
    asciiex = re.compile(r'[a-zA-Z]+')
    name_key = 'gender'
    
    def __init__(self, data_filename=None):
        import cPickle, os, sys
        
        # Load the namelist        
        if not data_filename:
            dir = os.path.dirname(sys.modules[__package__].__file__)
            data_filename = os.path.join(dir, 'data/nam_dict.txt.gz')
        
        self.name_to_gender, self.alias, self.name_to_popularity = load_data(data_filename)
        


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
            result = self._resolve_gender(firstname)
        else:
            result = []
        
        return {self.name_key : result}
    
    def _resolve_gender(self, firstname):
        firstname = firstname.lower()
        
        result = []
        gender = None
        
        if firstname in self.name_to_gender:
            gender = self.name_to_gender[firstname]
        elif firstname in self.alias:
            names = self.alias[firstname]

            from collections import Counter
            gender_counter = Counter()
            for name in names:
                gender = self.name_to_gender.get(name, None)
                if gender:
                    gender_counter[gender] += 1

            if len(gender_counter) > 0:
                gender = gender_counter.most_common(1)[0][0]
        
        if gender:
            result.append({"value": gender })
        
        return result


#----------------------------------------
def get_country_popularity_map(line, column_names):
    popularity_map = {}
    line = line.strip()[:-2]
    popularity = line[-55:]
    
    for index, score in enumerate(popularity):
        if score == 'A':
            score = '10'
        elif score == 'B':
            score = '11'
        elif score == 'C':
            score = '12'
        elif score == 'D':
            score = '13'
        elif score == ' ':
            continue
        score = int(score)
        country_name = column_names[index]
        popularity_map[country_name] = score

    return popularity_map
    

def load_data(data_filename):
    # See the header of the data file for a description of its format
    import gzip, logging
    
    lines = []
    skipped = 0
    country_list = []
    unique_names = set()
    in_country_list = False
    
    with gzip.open(data_filename) as input:
        for line in input:
            try:
                line = line.decode('ascii')
            except:
                skipped += 1
                continue
        
            if in_country_list:
                country_list.append(line)
            
            if line.startswith('#'):
                if line.startswith('#  countries:'):
                    in_country_list = True
                elif in_country_list and line.startswith('##') and len(country_list) > 1:
                    in_country_list = False
                continue

            if line[29] == '+':
                continue
            
            lines.append(line)
        
    
    column_names = {}
    for entry in country_list:
        name = entry.strip()[1:-1].strip()
        if name == '|' or len(name) == 0:
            continue

        column_names[len(column_names)] = name

    name_to_gender = {}
    alias = {}
    name_to_popularity = {}
    
    for line in lines:
        split_line = line.split(' ')
        gender = split_line[0]
        name = split_line[2].lower()

        if '+' in name or len(name) == 0:
            continue
    
        if gender == '=':
            short_name = split_line[2].lower()
            long_name = split_line[3].lower()
            alias.setdefault(short_name, []).append(long_name)
            gender = None
            unique_names.add(short_name)
            unique_names.add(long_name)  
        elif gender == 'M' or gender == '1M' or gender == '?M':
            gender = 'M'
        elif gender == 'F' or gender == '1F' or gender == '?F':
            gender = 'F'
        elif gender == '?':
            gender = None
        else:
            gender = None
    
        if gender:
            name_to_gender[name] = gender
            unique_names.add(name)
        
            popularity_map = get_country_popularity_map(line, column_names)
            name_to_popularity[name] = popularity_map
    
    logging.info('Loaded %d unique names' % len(unique_names))
    
    return name_to_gender, alias, name_to_popularity
    