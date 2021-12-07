import random
random.seed(42)
from virus import Virus


class Person(object):
    def __init__(self, _id, is_vaccinated = False, infection=False):
        self._id = _id # int
        self.is_alive = True  # boolean
        self.is_vaccinated = is_vaccinated  # boolean
        self.infection = False # boolean