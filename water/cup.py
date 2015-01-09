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

    @property
    def space(self):
        """
        >>> c = Cup(cap=3, cont=1)
        >>> c.space
        2
        """
        return self.capacity - self.contents

    def is_goal(self):
        """
        Contains Goal amount

        >>> c = Cup(cap=5, cont=4)
        >>> c.is_goal()
        True
        """
        return self.contents == GOAL

    def __eq__(self, c):
        """
        NOTE does not care about types.

        >>> c = Cup(cap=5, cont=4)

        1.  If either capacity or contents are different then not equal
        >>> c == Cup(cap=6, cont=4)
        False
        >>> c == Cup(cap=5, cont=5)
        False

        2. If both are the same then equal
        >>> c == Cup(cap=5, cont=4)
        True
        """
        return self.capacity == c.capacity and self.contents == c.contents

    def pour_into(self, other_cup):
        """
        Pour some / all content of this cup into other cup and make two new
        cups.

        1.  If current cup is empty, nothing changes.
        >>> c = Cup(cap=3, cont=0)
        >>> d = Cup(cap=5, cont=1)
        >>> e, f = c.pour_into(d)
        >>> e == c
        True
        >>> f == d
        True

        2.  If other cup is full, nothing changes.
        >>> c = Cup(cap=3, cont=3)
        >>> d = Cup(cap=5, cont=5)
        >>> e, f = c.pour_into(d)
        >>> e == c
        True
        >>> f == d
        True

        3.  If other cup has space and this cup has water, then transition.
            First cup is 5/5 and second cup is 0/3, this gives 2/5 and 3/3.
        >>> c = Cup(cap=5, cont=5)
        >>> d = Cup(cap=3, cont=0)
        >>> e, f = c.pour_into(d)
        >>> e.contents
        2
        >>> f.contents
        3
        """
        return (
            Cup(
                cap=self.capacity,
                cont=self.contents-min(self.contents, other_cup.space)
            ),
            Cup(
                cap=other_cup.capacity,
                cont=other_cup.contents+min(self.contents, other_cup.space)
            )
        )

    def __repr__(self):
        return "<Cup {}/{}>".format(self.contents, self.capacity)
