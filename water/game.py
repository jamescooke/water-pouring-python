from functools import reduce

from .cup import Cup


or_reduction = lambda x, y: x or y
and_reduction = lambda x, y: x and y


class Game(object):

    cups = None
    parent = None       # Game that created this one
    children = None

    def __init__(self, sizes=None, parent=None):
        """
        Set up a game with cups.

        Improvements
        * Just pass Cups instead of int configs for Cups
        * Put default cup config somewhere other than init

        >>> g = Game()
        >>> len(g.cups)
        3
        >>> g.parent is None
        True
        >>> g.children
        []

        >>> h = Game(sizes=[(5, 5), (5, 0)], parent=g)
        >>> len(h.cups)
        2
        >>> h.parent is g
        True
        """
        self.cups = []

        if sizes is None:
            # Set up cups with default sizes
            sizes = [(3, 0), (5, 0), (8, 8)]

        for cap, cont in sizes:
            self.cups.append(Cup(cap=cap, cont=cont))

        # Save a pointer to the parent
        self.parent = parent

        # Children starts empty
        self.children = []

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
            or_reduction,
            [cup.is_goal() for cup in self.cups]
        )

    def __eq__(self, g):
        """
        Games have same number of Cups and all Cups are equal.

        :pre: Game has at least one cup.

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
        return (
            len(self.cups) == len(g.cups)
            and reduce(
                and_reduction,
                [cup == g.cups[pos] for pos, cup in enumerate(self.cups)]
            )
        )

    def net_has_game(self, g):
        """
        Game's network of games contains this game.
        """
        return self.top_parent().has_game(g)

    def top_parent(self):
        """
        Returns the top parent for a game, the parent state that has no parent.
        """
        return self if self.parent is None else self.parent.top_parent()

    def has_game(self, g):
        """
        Passed Game ``g`` is in this Game's tree of Games

        >>> from unittest.mock import Mock
        >>> g = Game(sizes=[(3, 0), (5, 5)])

        1.  If the game being seached for matches, then True
        >>> g.has_game(Game(sizes=[(3, 0), (5, 5)]))
        True

        2.  If game does not match and no child games, False
        >>> g.has_game(Game(sizes=[(4, 0), (5, 5)]))
        False

        3.  If game being search for does not match, sub games are searched
        >>> s_a = Mock(name='sub Game A')
        >>> s_a.has_game.return_value = False
        >>> s_b = Mock(name='sub Game B')
        >>> s_b.has_game.return_value = True
        >>> g.children.append(s_a)
        >>> g.children.append(s_b)
        >>> g.has_game(Game(sizes=[(4, 0), (5, 5)]))
        True
        """
        return (
            self == g
            or (
                len(self.children) > 0
                and reduce(
                    or_reduction,
                    [game.has_game(g) for game in self.children]
                )
            )
        )
