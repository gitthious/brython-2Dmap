# -*- coding: utf-8 -*-

"""
Base type for geographic 2D bounding box.
"""

__author__ = "thierry.herve@free.fr"
__copyright__ = "Thierry Hervé"
__license__ = "MIT"

class BoundingBox(tuple):
    """
    Define geographic bounding box. Use official order for parameters, as
    south, west, north, east
    >>> b = BoundingBox(48.5766,7.5929,48.6057,7.6645)
    >>> b
    (48.5766, 7.5929, 48.6057, 7.6645)

    or string
    >>> b = BoundingBox("48.5766,7.5929,48.6057,7.6645")
    >>> b
    (48.5766, 7.5929, 48.6057, 7.6645)

    or string with parenthesis
    >>> b = BoundingBox("(48.5766, 7.5929, 48.6057, 7.6645)")
    >>> b
    (48.5766, 7.5929, 48.6057, 7.6645)

    You can use it as tuple
    >>> s, w, n, e = b
    >>> s, w, n, e
    (48.5766, 7.5929, 48.6057, 7.6645)

    And you can iter on it:
    >>> vs =[c for c in b]
    >>> vs
    [48.5766, 7.5929, 48.6057, 7.6645]

    You can pass args as tuple like this
    >>> b = BoundingBox((48.5766,7.5929,48.6057,7.6645))
    >>> b
    (48.5766, 7.5929, 48.6057, 7.6645)

    or with 2 points:
    >>> b = BoundingBox((48.5766,7.5929),(48.6057,7.6645))
    >>> b
    (48.5766, 7.5929, 48.6057, 7.6645)

    BoundingBox reorder values if necessary:
    >>> b = BoundingBox((48.6057,7.6645), (48.5766,7.5929))
    >>> b
    (48.5766, 7.5929, 48.6057, 7.6645)
    
    Properties and aliases are also defined for comprehensive access:
    >>> (b.west,b.east) == (b.xmin,b.xmax)
    True

    """
    __slots__ = []
    def __new__(cls, *args):
        assert len(args) == 1 or len(args) == 2 or len(args) == 4
        if len(args) == 1:
            if isinstance(args[0], str):
                # "48.5766, 7.5929, 48.6057, 7.6645" ou
                # "(48.5766, 7.5929, 48.6057, 7.6645)"
                south, west, north, east = eval(args[0])
            else:
                south, west, north, east = args[0]
        elif len(args) == 2:
            (south, west), (north, east) = args[0], args[1]
        else:
            south, west, north, east = args
        if south > north: south, north = north, south
        if west > east: west, east = east, west
        return tuple.__new__(cls, (south, west, north, east))
    @property
    def south(self): return self[0]
    @property
    def west(self): return self[1]
    @property
    def north(self): return self[2]
    @property
    def east(self): return self[3]
    # alias
    xmin = west
    xmax = east
    ymin = south
    ymax = north
    # others alias
    left = west
    bottom = south
    right = east
    top = north
    def __contains__(self, point):
        lat, lon = point
        return  lat >= self.south and lat <= self.north \
                and lon >= self.west and lon <= self.east
    def __str__(self):
        return ', '.join((f"{float(v):.5f}".rstrip('0') for v in self))

    # def __repr__(self):
        # return str(self)

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)