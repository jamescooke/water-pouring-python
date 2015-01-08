import copy
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

    def make_game(self, c_a, c_b):
        """
        Create a new game state by pouring Cup at ``c_a`` into Cup at ``c_b``.
        New game will have its parent set as this Game.

        1.  Does not care if the pour is a 'good pour', just returns the new
            game. If there are no contents to pour, or no space in the
            destination, then the new game will be in the same state and will
            be removed by the de-duplication search.
        >>> g = Game(sizes=[(3, 0), (5, 5)])
        >>> h = g.make_game(0, 1)
        >>> g == h
        True
        >>> h.parent is g
        True

        2.  When the pour is good, then the cups' states are adjusted
            accordingly. Original parent Game's cups stay the same.
        >>> g = Game(sizes=[(3, 3), (5, 5), (8, 0)])
        >>> h = g.make_game(0, 2)
        >>> expected = Game(sizes=[(3, 0), (5, 5), (8, 3)])
        >>> h == expected
        True
        >>> h.parent is g
        True
        >>> g.cups[0].contents
        3
        """
        new_game = copy.deepcopy(self)
        new_game.parent = self
        (new_game.cups[c_a],
         new_game.cups[c_b]) = new_game.cups[c_a].pour_into(new_game.cups[c_b])
        return new_game

    def make_children(self):
        """
        Do all the pours, check that new Games don't exist in the network and
        for those that are new add them to this Game's children.

        1.  If there's just one cup, does nothing
        >>> g = Game(sizes=[(4, 4)])
        >>> g.make_children()
        0
        >>> g.children
        []

        2.  If a pour option creates a Game that's already in the network then
            it's not added to the children.
        >>> g = Game(sizes=[(3, 0), (5, 5)])
        >>> g.make_children()
        1
        >>> expected = Game(sizes=[(3, 3), (5, 2)])
        >>> g.children[0] == expected
        True

        3.  TODO if the Game generated by pouring is already in the network,
            then no new games are generated.
        """
        for c_a in range(len(self.cups)):
            for c_b in range(len(self.cups)):
                if c_b == c_a:
                    continue
                new_game = self.make_game(c_a, c_b)
                if not self.net_has_game(new_game):
                    self.children.append(new_game)
        return len(self.children)

    def is_solvable(self):
        """
        Main function. Could be written as a one line boolean, but keeping it
        like this for readability. See unittests for coverage.
        """
        if self.is_goal():
            self.print_trace()
            return True

        if self.make_children() == 0:
            return False

        return self.solvable_child()

    def solvable_child(self):
        """
        Recursively walks list of Game's children looking for a solvable one.
        Wishing python was haskell ._. See unittests for coverage.
        """
        if len(self.children) < 1:
            return False

        for child in self.children:
            if child.is_solvable():
                return True

        return False

    def print_trace(self):
        print(self.cups)
