import json, os

class LocalStore:
    def __init__(self, path, filename):
        self.path = path
        self.filename = filename
        self.load()
    
    def get_data(self):
        return self.data
        
    def set_data(self, data):
        self.data = data
    
    def load(self):
        full_path = os.path.join(self.path, self.filename)
        
        with open(full_path, 'a+') as in_file:
            try:
                self.data = json.load(in_file)
            except:
                self.data = {}
            
    def dump(self):
        full_path = os.path.join(self.path, self.filename)
        with open(full_path, 'w+') as out_file:
            json.dump(self.data, out_file)