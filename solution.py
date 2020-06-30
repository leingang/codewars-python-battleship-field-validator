#!/usr/bin/env python

from collections import Counter
from logging import DEBUG

from utils import add_logger, get_logger
logger = get_logger(__name__)
# logger.setLevel(DEBUG)

def ships_touch(field):
    """Check if the ships in *field* touch each other
    
    >>> ships_touch([[0,1],[1,0]])
    True

    >>> ships_touch([[1,1,0],[0,0,0],[0,1,1]])
    False

    """
    m, n = len(field), len(field[0])
    checks = [field[i][j]*field[i+1][j+1] for i in range(m-1) for j in range(n-1)]\
        + [field[i][j]*field[i-1][j+1] for i in range(1,m) for j in range(n-1)]
    return sum(checks) != 0

@add_logger
def validate_battlefield(field):
    """Determine if *field* is a valid Battleship field.

    Rules:

    1. All ships must be on the board
    2. No ships touching edges or corners.

    """
    if ships_touch(field): return False
    # that's the easy part

    ships_to_find = {4:1, 3:2, 2:3, 1:4}# length:count
    m, n = len(field), len(field[0])
    for d in sorted(ships_to_find.keys(),reverse=True):
        # look for a string of d consecutive 1's
        # horizontally
        for i in range(m):
            for j in range(n-d+1):
                if all(field[i][j+x] == 1 for x in range(d)):
                    logger.debug("Found a horizontal ship of length {d} at position[{i}][{j}]".format(d=d,i=i,j=j))
                    ships_to_find[d] -= 1
                    # zero it out
                    for x in range(d):
                        field[i][j+x] = 0
        # now vertically                        
        for j in range(n):
            for i in range(m-d+1):
                if all(field[i+x][j] == 1 for x in range(d)):
                    logger.debug("Found a vertical ship of length {d} at position[{i}][{j}]".format(d=d,i=i,j=j))
                    ships_to_find[d] -= 1
                    # zero it out
                    for x in range(d):
                        field[i+x][j] = 0
        logger.debug("ships_to_find: {}".format(ships_to_find))
    # Did all the ships get found?
    return all(ships_to_find[d] == 0 for d in ships_to_find)