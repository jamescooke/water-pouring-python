GOAL = 4


class Cup(object):

    capacity = 1
    contents = 0

    def __init__(self, cap=1, cont=0):
        """
        Makes cups ready for pouring

        0.  Cup set up
        >>> c = Cup()
        >>> c.capacity
        1
        >>> c.contents
        0

        1.  Prevents cups being made with more water than capacity
        >>> d = Cup(cap=1, cont=2)
        Traceback (most recent call last):
        ...
        ValueError: Too much contents
        """
        if cap < cont:
            raise ValueError('Too much contents')
        self.capacity = cap
        self.contents = cont

    def has_space(self):
        """
        >>> b = Cup(cap=5, cont=4)
        >>> b.has_space()
        True
        >>> c = Cup(cap=5, cont=5)
        >>> c.has_space()
        False
        """
        return self.contents < self.capacity

    def is_goal(self):
        """
        Contains Goal amount

        >>> c = Cup(cap=5, cont=4)
        >>> c.is_goal()
        True
        """
        return self.contents == GOAL
