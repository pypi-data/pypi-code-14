class Bundle:
    def __init__(self):
        self.params = {}
        self.errors = {}
    def add(self,param):
        self.params[param.name] = param
        return param
    def validate(self, values):
        self.errors.clear()
        for param in self.params.values():
            param.parse(values.get(param.name))
        for param in self.params.values():
            print('==> ' + param.name + " " + str(param.valid))
            if param.error:
                self.errors[param.name] = param
        return len(self.errors) == 0
