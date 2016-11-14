import random


class WordLists:
    adjectives = ['last', 'other', 'new', 'good', 'old', 'great', 'high', 'small', 'different', 'large', 'local', 'social',
                        'long', 'important', 'young', 'national', 'possible', 'big', 'right', 'early', 'public', 'only', 'able',
                        'political', 'particular', 'full', 'far', 'late', 'available', 'little', 'low', 'bad', 'main', 'major',
                        'economic', 'general', 'real', 'likely', 'certain', 'special', 'difficult', 'international', 'clear',
                        'sure', 'black', 'white', 'common', 'strong', 'whole', 'free', 'similar', 'necessary', 'central',
                        'true', 'open', 'short', 'personal', 'single', 'easy', 'private', 'financial', 'poor', 'foreign',
                        'human', 'simple', 'recent', 'wide', 'various', 'due', 'hard', 'royal', 'fine', 'natural', 'wrong',
                        'final', 'following', 'present', 'nice', 'trip', 'close', 'current', 'legal', 'red', 'happy', 'concerned',
                        'individual', 'normal', 'previous', 'serious', 'significant', 'prime', 'industrial', 'sorry', 'labor', 'left',
                        'dead', 'specific', 'total', 'appropriate', 'military', 'basic', 'original', 'successful', 'aware', 'popular',
                        'professional', 'heavy', 'top', 'dark', 'ready', 'useful']
    nouns = ['time', 'year', 'people', 'way', 'man', 'day', 'thing', 'child', 'government', 'part', 'life', 'case',
                        'woman', 'work', 'system', 'group', 'number', 'world', 'area', 'course', 'company',
                        'problem', 'service', 'hand', 'party', 'school', 'place', 'point', 'house', 'country', 'week',
                        'member', 'end', 'word', 'example', 'family', 'fact', 'state', 'percent', 'home', 'month', 'side',
                        'night', 'eye', 'head', 'information', 'question', 'business', 'power', 'money', 'change', 'interest',
                        'order', 'book', 'development', 'room', 'water', 'form', 'car', 'other', 'level', 'policy', 'council', 'line',
                        'need', 'effect', 'use', 'idea', 'study', 'lot', 'job', 'result', 'body', 'friend', 'right', 'authority', 'view',
                        'report', 'bit', 'face', 'market', 'hour', 'rate', 'law', 'door', 'court', 'office', 'war', 'reason', 'minister',
                        'subject', 'person', 'term', 'sort', 'period', 'society', 'process', 'mother', 'voice', 'police', 'kind',
                        'price', 'action', 'issue', 'position', 'cost', 'matter', 'community', 'figure', 'type', 'research', 'education',
                        'few', 'program', 'minute', 'moment', 'girl', 'age', 'center', 'control', 'value', 'health', 'decision', 'class',
                        'industry', 'back', 'force', 'condition', 'paper', 'century', 'father', 'section', 'patient', 'activity', 'road',
                        'table', 'church', 'mind', 'team', 'experience', 'death', 'act', 'sense', 'staff', 'student', 'language',
                        'department', 'management', 'morning', 'plan', 'role', 'practice', 'bank', 'support', 'event', 'building',
                        'range', 'stage', 'meeting', 'town', 'art', 'club', 'arm', 'history', 'parent', 'land', 'trade', 'situation',
                        'teacher', 'record', 'manager', 'relation', 'field', 'window', 'account', 'difference', 'material', 'air', 'wife',
                        'project', 'sale', 'relationship', 'light', 'care', 'rule', 'story', 'quality', 'tax', 'worker', 'nature', 'structure',
                        'data', 'pound', 'method', 'unit', 'bed', 'union', 'movement', 'board', 'detail', 'model', 'wall', 'computer',
                        'hospital', 'chapter', 'scheme', 'theory', 'property', 'officer', 'charge', 'director', 'approach',
                        'chance', 'application', 'top', 'amount', 'son', 'operation', 'opportunity', 'leader', 'look', 'share',
                        'production', 'firm', 'picture', 'source', 'security', 'contract', 'agreement', 'site', 'labor', 'test', 'loss',
                        'color', 'shop', 'benefit', 'animal', 'heart', 'election', 'purpose', 'standard', 'secretary', 'date', 'music',
                        'hair', 'factor', 'pattern', 'piece', 'front', 'evening', 'tree', 'population', 'plant', 'pressure', 'response',
                        'street', 'performance', 'knowledge', 'design', 'page', 'individual', 'rest', 'basis', 'size', 'environment',
                        'fire', 'series', 'success', 'thought', 'list', 'future', 'analysis', 'space', 'demand', 'statement', 'attention',
                        'love', 'principle', 'set', 'doctor', 'choice', 'feature', 'couple', 'step', 'machine', 'income', 'training',
                        'association', 'film', 'region', 'effort', 'player', 'award', 'village', 'organization', 'news', 'difficulty',
                        'cell', 'energy', 'degree', 'mile', 'means', 'growth', 'treatment', 'sound', 'task', 'provision', 'behavior',
                        'function', 'resource', 'defense', 'garden', 'floor', 'technology', 'style', 'feeling', 'science', 'doubt',
                        'horse', 'answer', 'user', 'fund', 'character', 'risk', 'dog', 'army', 'station', 'glass', 'cup', 'husband',
                        'capital', 'note', 'season', 'argument', 'show', 'responsibility', 'deal', 'economy', 'element', 'duty',
                        'attempt', 'leg', 'investment', 'brother', 'title', 'hotel', 'aspect', 'increase', 'help', 'summer', 'daughter',
                        'baby', 'sea', 'skill', 'claim', 'concern', 'university', 'discussion', 'customer', 'box', 'conference',
                        'whole', 'profit', 'division', 'procedure', 'king', 'image', 'oil', 'circumstance', 'proposal', 'client',
                        'sector', 'direction', 'instance', 'sign', 'measure', 'attitude', 'disease', 'commission', 'seat',
                        'president', 'addition', 'goal', 'affair', 'technique', 'respect', 'item', 'version', 'ability', 'good',
                        'campaign', 'advice', 'institution', 'surface', 'library', 'pupil', 'advantage', 'memory', 'culture',
                        'blood', 'majority', 'variety', 'press', 'bill', 'competition', 'general', 'access', 'stone']
    verbs = ['be', 'have', 'do', 'say', 'go', 'get', 'make', 'see', 'know', 'take', 'think', 'come', 'give', 'look',
                        'use', 'find', 'want', 'tell', 'put', 'work', 'become', 'mean', 'leave', 'seem', 'need', 'feel',
                        'may', 'ask', 'show', 'try', 'call', 'keep', 'provide', 'hold', 'follow', 'turn', 'bring', 'begin',
                        'like', 'write', 'start', 'run', 'set', 'help', 'play', 'move', 'pay', 'hear', 'meet', 'include',
                        'believe', 'allow', 'lead', 'stand', 'live', 'happen', 'carry', 'talk', 'sit', 'appear', 'continue',
                        'let', 'produce', 'involve', 'require', 'suggest', 'consider', 'read', 'change', 'offer', 'lose',
                        'add', 'expect', 'remember', 'remain', 'tall', 'speak', 'open', 'buy', 'stop', 'send', 'decide',
                        'win', 'understand', 'develop', 'receive', 'return', 'build', 'spend', 'describe', 'agree',
                        'increase', 'learn', 'reach', 'lie', 'walk', 'die', 'draw', 'hope', 'create', 'sell', 'report',
                        'pass', 'accept', 'cause', 'watch', 'break', 'support', 'explain', 'stay', 'wait', 'cover',
                        'apply', 'raise', 'claim', 'form', 'base', 'cut', 'grow', 'contain', 'bear', 'join', 'reduce',
                        'establish', 'face', 'choose', 'wish', 'achieve', 'drive', 'deal', 'place', 'seek', 'fail', 'serve',
                        'end', 'occur', 'kill', 'act', 'plan', 'eat', 'close', 'represent', 'love', 'rise', 'prepare', 'manage',
                        'discuss', 'prove', 'catch', 'pick', 'enjoy', 'suppose', 'wear', 'argue', 'introduce', 'enter',
                        'arrive', 'ensure', 'pull', 'refer', 'thank', 'present', 'control', 'affect', 'point', 'identify',
                        'relate', 'force', 'compare', 'suffer', 'announce', 'obtain', 'indicate', 'forget', 'publish',
                        'visit', 'listen', 'finish', 'fight', 'train', 'maintain', 'save', 'design', 'improve', 'avoid',
                        'wonder', 'tend', 'express', 'determine', 'exist', 'share', 'smile', 'treat', 'remove',
                        'state', 'throw', 'tilt', 'assume', 'mention', 'admit', 'replace', 'reflect', 'intend', 'encourage',
                        'miss', 'drop', 'fly', 'reveal', 'operate', 'discover', 'record', 'refuse', 'prevent', 'teach',
                        'cost', 'answer', 'depend']
    determiners = ['a', 'the', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'this', 'that']

    @classmethod
    def randomAdjective(cls):
        return random.choice(cls.adjectives)

    @classmethod
    def randomNoun(cls):
        return random.choice(cls.nouns)

    @classmethod
    def randomVerb(cls):
        return random.choice(cls.verbs)

    @classmethod
    def randomDeterminer(cls):
        return random.choice(cls.determiners)
