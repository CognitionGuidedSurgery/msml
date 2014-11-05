__author__ = 'suwelack'


class SimulationResults(object):

    def __init__(self, initial_points= None , deformed_points=None, connectivity=None):
        self.deformed_Points = deformed_points or {0,0,0}
        self.initial_points = initial_points or {0,0,0}
        self._connectivity = connectivity or set()

    @property
    def deformed_points(self):
        return self._deformed_points

    @deformed_points.setter
    def deformed_points(self, deformed_points):
        self._deformed_points = deformed_points

    @property
    def initial_points(self):
        return self._initial_points

    @initial_points.setter
    def initial_points(self, initial_points):
        self._initial_points = initial_points

    @property
    def connectivity(self):
        return self._connectivity

    @connectivity.setter
    def connectivity(self, connectivity):
        self._connectivity = connectivity

