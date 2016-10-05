
class Extractor(object):

    def __init__(self):
    	self.renamed_input_fields = list()

    def extract(self, doc):
        raise NotImplementedError("Need to implement extract function")

    # should create a new dictionary each time
    def get_metadata(self):
        raise NotImplementedError("Need to implement get_metadata function")

    def set_metadata(self):
        raise NotImplementedError("Need to implement set_metadata function")

    def get_renamed_input_fields(self):
        raise NotImplementedError(
            "Need to implement get_renamed_input_fields function")

    def set_renamed_input_fields(self, renamed_input_fields):
        if not (isinstance(renamed_input_fields, basestring) or\
                isinstance(renamed_input_fields, types.ListType)):
            raise ValueError("renamed_input_fields must be a string or a list")
        self.renamed_input_fields = renamed_input_fields
        return self
