# classes
class Tournament(object):
    def __init__(self, name, url, start_date, end_date):
        self.name = name
        self.url = url
        self.start_date = start_date
        self.end_date = end_date

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self):
        return self.name
