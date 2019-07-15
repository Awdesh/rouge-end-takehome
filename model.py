"""Encapsulates all models for mobile food locations."""


class Location(object):

    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location

    def __repr__(self):
        return '{}{}'.format(self.__class__.__name__, self.__dict__)

    def __lt__(self, other: 'Location') -> bool:
        return self.name < other.name

    def __eq__(self, other: 'Location') -> bool:
        return self.name == other.name and self.location == other.location
