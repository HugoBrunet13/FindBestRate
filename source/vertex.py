class Vertex(object):
    """ Vertex class to model a pair (exchange, currency) """

    def __init__(self,exchange,currency):
        """ Constructor
         Args:
             exchange (str): exchange name
             currency (str): ISO code of a currency
        """

        if not isinstance(exchange, str):
            raise TypeError("'exchange' information not correct!") # exchange input must be a string
        if  not isinstance(currency, str):
            raise TypeError("'currency' information not correct!") # currency input must be a string
        else:
            self.__exchange = exchange.upper() # value of exchange in UPPER case
            self.__currency = currency.upper() # value of currency in UPPER case

    @property
    def exchange(self):
        """ Get exchange property """
        return self.__exchange

    @property
    def currency(self):
        """ Get currency property """
        return self.__currency

    def __str__(self):
        """ Formatting of print option for a vertex """
        return "%s, %s" % (self.exchange,self.currency)

    def __eq__(self,other):
        """ Overloading of operator == so as to enable the comparison between two vertices"""
        if not isinstance(other, Vertex):
            raise TypeError("other must be a Vertex")
        if self.exchange == other.exchange and self.currency == other.currency:
            return True
        else:
            return False