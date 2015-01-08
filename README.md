# Water Pouring Problem

A sketch of a "water pouring problem" in Python3.

This README contains basic setup and test instructions. Full [blog post is
*ABOUT TO BE* available](http://jamescooke.info/sketch-water-pouring.html) with
more information.

## The Problem

> There are three glasses on the table - 3, 5, and 8 oz. The first two are
> empty, the last contains 8 oz of water. By pouring water from one glass to
> another make at least one of them contain exactly 4 oz of water.

Source: A. Bogomolny, [3 Glasses
Puzzle](http://www.cut-the-knot.org/water.shtml) from Interactive Mathematics
Miscellany and Puzzles
[http://www.cut-the-knot.org/water.shtml](http://www.cut-the-knot.org/water.shtml),
Accessed 08 January 2015

## Set up and Solve

Grab the code and change into the directory created:

```sh
git clone https://github.com/jamescooke/water-pouring-python.git
cd water-pouring-python
```

I like to make a virtualenv. This sketch is Python3, so specify that when
making the env.

```sh
virtualenv env --python=python3
source env/bin/activate
```

I also like iPython, so install that and run it:

```sh
pip install ipython
ipython
```

Now the 'water' module can be used to solve the problem with the 3, 5 and 8 oz
cups set up as described above.

```py
In [1]: from water.game import Game

In [2]: game = Game(sizes=[(3, 0), (5, 0), (8, 8)])

In [3]: game.is_solvable()
[<Cup 0/3>, <Cup 0/5>, <Cup 8/8>]
[<Cup 3/3>, <Cup 0/5>, <Cup 5/8>]
[<Cup 0/3>, <Cup 3/5>, <Cup 5/8>]
[<Cup 3/3>, <Cup 3/5>, <Cup 2/8>]
[<Cup 1/3>, <Cup 5/5>, <Cup 2/8>]
[<Cup 1/3>, <Cup 0/5>, <Cup 7/8>]
[<Cup 0/3>, <Cup 1/5>, <Cup 7/8>]
[<Cup 3/3>, <Cup 1/5>, <Cup 4/8>]
Out[3]: True
```

This shows that the problem described above is solvable and a route to the
solution. When printing the state of the Game, each Cup is printed with its
contents and capacity shown as:

```
<Cup `contents`/`capacity`>
```

## Testing

There are tests in the code as a side effect of writing it in a generally TDD
manner.

Tests require nose, but flake8 is also helpful. Install both with the test
requirements file:

```sh
pip install -r test-requirements.txt
```

Now run each in turn:

```sh
nosetests
flake8 water
```

... and both should pass. Happy days.

## License and contribution

Please open any discussion using GitHub Issues. Contributions and questions
very welcome.

Licensed under GNU GPL v2.0
