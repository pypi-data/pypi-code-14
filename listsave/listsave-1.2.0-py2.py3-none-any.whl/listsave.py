class Listings:

    """
    filename - Please set this to the name
    you would like the config file to be
    """

    def __init__(self, filename):
        self.filename = filename

    def write(self, lists):
        f = open(self.filename, "a")
        self.lists = lists
        for item in lists:
            f.write(str(item) + "\n")
        f.close()

    def remove_from_lists(self, item):
        self.item = item
        f = open(self.filename,"r")
        lines = f.readlines()
        f.close()
        f = open(self.filename,"w")
        for line in lines:
          if line != str(self.item) + "\n":
            f.write(str(line))

    def read(self):
        lines = open(self.filename).readlines()
        clean_lines = [x.strip() for x in lines]
        return clean_lines
