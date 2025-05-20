from abc import ABC, abstractmethod
from math import pi, tan

class FigureColor:
    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        return self._color

class GeometricFigure(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def name(self):
        pass

class Pentagon(GeometricFigure):
    _figure_name = "Pentagon"

    def __init__(self, side_length, color):
        self.side = side_length
        self.color_obj = FigureColor(color)

    def area(self):
        return (5 * self.side ** 2) / (4 * tan(pi / 5))

    def name(self):
        return self._figure_name

    def describe(self):
        return "Figure: {}, Side: {:.2f}, Area: {:.2f}, Color: {}".format(
            self.name(), self.side, self.area(), self.color_obj.color
        )
