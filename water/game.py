from functools import reduce

from .cup import Cup


class Game(object):

    cups = None

    def __init__(self, sizes=None):
        """
        Set up a game with cups.

        Improvements
        * Just pass Cups instead of int configs for Cups
        * Put default cup config somewhere other than init

        >>> g = Game()
        >>> len(g.cups)
        3

        >>> h = Game(sizes=[(5, 5), (5, 0)])
        >>> len(h.cups)
        2
        """
        self.cups = []

        if sizes is None:
            # Set up cups with default sizes
            sizes = [(3, 0), (5, 0), (8, 8)]

        for cap, cont in sizes:
            self.cups.append(Cup(cap=cap, cont=cont))

    def is_goal(self):
        """
        There is a Cup in the Game that has the goal conditions.

        >>> g = Game(sizes=[(4, 4)])
        >>> g.is_goal()
        True

        >>> h = Game()
        >>> h.is_goal()
        False
        """
        return reduce(
            # OR reduction
            lambda x, y: x or y,
            [cup.is_goal() for cup in self.cups]
        )

    def __eq__(self, g):
        """
        Games have same number of Cups and all Cups are equal.

        >>> g = Game(sizes=[(3, 0), (5, 5)])

        1. Less or more games, even if equal, is not equal.
        >>> g == Game(sizes=[(3, 0)])
        False
        >>> g == Game(sizes=[(3, 0), (5, 5), (1, 1)])
        False

        2. Same num of cups means checking cups.
        >>> g == Game(sizes=[(3, 1), (5, 4)])
        False

        3. Equal is equal.
        >>> g == Game(sizes=[(3, 0), (5, 5)])
        True
        """
        return len(self.cups) == len(g.cups) and reduce(
            # AND reduction
            lambda x, y: x and y,
            [cup == g.cups[pos] for pos, cup in enumerate(self.cups)]
        )
