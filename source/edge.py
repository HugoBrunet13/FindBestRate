from vertex import Vertex
from dateutil import parser
from datetime import datetime

class Edge():
    """ Edge class to model an edge:  <vertex_source> <vertex_destination> <weight> <date> """

    def __init__(self,vertex_source, vertex_destination, weight, date):
        """ Constructor
        Args:
            vertex_source: source vertex of the edge
            vertex_destination: destination vertex of the edge
            weight: weight of the edge, represent the rate between two vertex
            date: date of last update of the edge information
        """
        # We test the type of each input
        if not isinstance(vertex_source, Vertex):
            raise TypeError("'vertex_source' must be a Vertex")
        if not isinstance(vertex_destination, Vertex):
            raise TypeError("'vertex_destination' must be a Vertex")
        if not isinstance(weight, int) and not isinstance(weight, float):
            raise TypeError("'weight' must be a numeric value")
        if not isinstance(parser.parse(date), datetime): # The date parameter must be parsable into datetime object
            raise TypeError("Date format incorrect")
        else:
            self.__vertex_source = vertex_source
            self.__vertex_destination = vertex_destination
            self.__weight = weight
            self.__date = parser.parse(date) # Date parameter converted as datetime object

    @property
    def vertex_source(self):
        """ Get vertex_source property """
        return self.__vertex_source

    @property
    def vertex_destination(self):
        """ Get vertex_destination property """
        return self.__vertex_destination

    @property
    def weight(self):
        """ Get weight property """
        return self.__weight

    @property
    def date(self):
        """ Get date property """
        return self.__date

    @weight.setter
    def weight(self, value):
        """ Set weight property, with parameter 'value' which must be an int or a float """
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("'weight' must be a numeric value")
        else:
            self.__weight = value

    @date.setter
    def date(self,value):
        """ Set date property with parameter 'value' which must be convertible into a datetime object """
        try:
            date = parser.parse(value)
            self.__date=date
        except:
            raise ValueError("Date format incorrect")

    def __str__(self):
        """" Formatting of print option for an edge """
        return "%s (%s) ---- %s ---> (%s)" % (str(self.date), self.vertex_source, str(self.weight), self.vertex_destination)