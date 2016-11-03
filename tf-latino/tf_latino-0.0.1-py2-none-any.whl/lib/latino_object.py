class LatinoObject:
    def __init__(self,latino_object):
        import LatinoInterfaces
        self.serialized_object = LatinoInterfaces.LatinoCF.Save(latino_object)
        #if hasattr(latino_object, "GetType") and latino_object.GetType().IsGenericType:
        #    name = latino_object.GetType().GetGenericTypeDefinition()
        #a=latino_object.GetType()
        self.name=latino_object.__str__()

    def __repr__(self):
        return "<LatinoObject: " + self.name + ">"

    def load(self):
        import LatinoInterfaces
        return LatinoInterfaces.LatinoCF.Load(self.serialized_object)