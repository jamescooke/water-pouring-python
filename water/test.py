import builtins
from functools import reduce
from unittest import TestCase
from unittest.mock import Mock, patch

from .game import or_reduction, Game


"""

        2.  If Game is not success, pours are made from each cup to every other
            and recursively called if the generated game is not already in the
            network.
        >>> g = Game(sizes=[(3, 0), (5, 5)])
        >>> g.is_solvable()
        False

        3.  A success example
        >>> g = Game(sizes=[(3, 3), (5, 1)])
        >>> g.is_solvable()
        True
"""

class TestSolvable(TestCase):
    """
    Tests around the recursive walk down the tree to ensure that solvableness
    works.
    """

    # --- Tests of is_solvable ------------------------------------------------

    @patch.object(Game, 'print_trace')
    @patch.object(Game, 'is_goal')
    def test_cup_is_goal(self, m_is_goal, m_print_trace):
        """
        If Game has a Cup of success then True
        """
        m_is_goal.return_value = True
        g = Game()

        result = g.is_solvable()

        self.assertTrue(result)
        # ``print_trace`` was called
        m_print_trace.assert_called_once_with()

    @patch.object(Game, 'make_children')
    @patch.object(Game, 'is_goal')
    def test_children_empty(self, m_is_goal, m_make_children):
        """
        If Game does not generate any children, then False
        """
        m_is_goal.return_value = False
        m_make_children.return_value = 0
        g = Game()

        result = g.is_solvable()

        self.assertFalse(result)

    @patch.object(Game, 'solvable_child')
    @patch.object(Game, 'make_children')
    @patch.object(Game, 'is_goal')
    def test_children_empty(self, m_is_goal, m_make_children,
                            m_solvable_child):
        """
        If Game has children and is not solvable itself, then child games are
        tested using the helper function.
        """
        m_is_goal.return_value = False
        m_make_children.return_value = 3
        m_solvable_child.return_value = True
        g = Game()

        result = g.is_solvable()

        self.assertTrue(result)
        # Ensure that solvable_child was called once
        m_solvable_child.assert_called_once_with()

    # --- Tests of solvable_child ---------------------------------------------

    def test_solvable_children_shortcircuit(self):
        """
        Game will check each child in order, if one is found to be solvable
        then no more are tested.
        """
        first = Mock(spec=Game)
        first.is_solvable.return_value = False
        second = Mock(spec=Game)
        second.is_solvable.return_value = True
        third = Mock(spec=Game)
        third.is_solvable.return_value = False
        g = Game()
        g.children = [first, second, third]

        result = g.solvable_child()

        self.assertTrue(result)
        self.assertEqual(first.is_solvable.call_count, 1)
        self.assertEqual(second.is_solvable.call_count, 1)
        self.assertEqual(third.is_solvable.call_count, 0)

    # --- Tests of print_trace ------------------------------------------------

    @patch.object(builtins, 'print')
    def test_print_trace_base_case(self, m_print):
        """
        print_trace with no parent just prints
        """
        g = Game()
        g.parent = None

        g.print_trace()

        m_print.assert_called_once_with(g.cups)

    @patch.object(builtins, 'print')
    def test_print_trace_recurse(self, m_print):
        """
        print_trace with no parent just prints
        """
        f = Mock(name='Parent game', spec=Game)
        g = Game()
        g.parent = f

        g.print_trace()

        f.print_trace.assert_called_once_with()
        m_print.assert_called_once_with(g.cups)
