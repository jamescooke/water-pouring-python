from .cup import Cup


class Game(object):

    cups = None

    def __init__(self, sizes=None):
        """
        Set up a game with cups

        Improvements
        * Just pass Cups instead of int configs for Cups

        >>> g = Game()
        >>> len(g.cups)
        3

        >>> h = Game(sizes=[(5, 5), (5, 0)])
        >>> len(h.cups)
        2
        """
        self.cups = []

        if sizes is None:
            sizes = [(3, 0), (5, 0), (8, 8)]

        for cap, cont in sizes:
            self.cups.append(Cup(cap=cap, cont=cont))
