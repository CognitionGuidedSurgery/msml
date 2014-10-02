__author__ = 'suwelack'


class SimulationResults(object):

    def __init__(self, initial_points={0,0,0} , deformed_points={0,0,0}, connectivity={}):
        self.deformed_Points = deformed_points
        self.initial_points = initial_points
        self.connectivity = connectivity

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

