class NameValuePair:
    def __init__(self,name,value):
      self.name = name
      self.value = value

    def printname(self):
        print(self.name, self.value)

    def to_json(self):
        return {"NameValuePair": {'label': self.name,
                               'value': self.value}}