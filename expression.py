from z3 import *
"""
<expr> ::= <boolean_expression> | <arithm_expression>
"""

from arithmExpression import *
from boolExpression import *


class ParseExpression(Parser):
    def __init__(self):
        self.parser = ParseBoolExpr() ^ ParseArithmExpr()


def printExpr(inp):
    """
    >>> printExpr("x = y")
    (x = y)
    >>> printExpr("x + 2 * y")
    (x + (2 * y))
    >>> printExpr("x < 2 and y < 1")
    ((x < 2) and (y < 1))
    >>> printExpr("(x + 2*y < 15 + x * x) or z = 5")
    (((x + (2 * y)) < (15 + (x * x))) or (z = 5))
    >>> printExpr("x + 2*y < 15 + x * x or z = 5")
    (((x + (2 * y)) < (15 + (x * x))) or (z = 5))
    """
    exprStr = result(ParseExpression().parse(inp))
    print(exprStr)


def evalExpr(inp, env):
    """
    >>> env = {'x':1, 'y':2, 'z':3}
    >>> evalExpr("x = y", env)
    False
    >>> evalExpr("x + 2 * y", env)
    5
    >>> evalExpr("x < 2 and y < 1", env)
    False
    >>> evalExpr("(x + 2*y < 15 + x * x) or z = 5", env)
    True
    >>> evalExpr("x + 2*y < 15 + x * x or z = 5", env)
    True
    >>> evalExpr("x * 2 + 3 < x * (2 + 3)", env)
    False
    >>> evalExpr("y * 2 + 3 < y * (2 + 3)", env)
    True
    """
    res = ParseExpression().parse(inp)
    if res != []:
        expr = result(res)
        result_val = expr.eval_(env)
        print(result_val)

def solve(exprs):
    """
    >>> sol = solve(["x + y + z = 10", "x < y", "x < 3", "0 < x"])
    >>> sol
    ['x = 2', 'y = 3', 'z = 5']
    >>> sol = solve(["x + y + z = 10", "x < y", "x < 3", "5 < x"])
    No solution!
    >>> sol = solve(["x + y + z = 10", "x < y or x = y", "x < 3", "5 < x or 0 < x"])
    >>> sol
    ['x = 1', 'y = 2', 'z = 7']
    """
    
    s = Solver()
    
    for i in exprs:
        res = ParseExpression().parse(i)
        expr = result(res)
        exprZ3 = expr.toZ3()
        s.add(exprZ3)

    if s.check() == sat:
        solution = set()
        model = s.model()
        for d in model:
            solution.add(str("%s = %s" % (d, model[d])))   
        solution_list = list(solution)
        solution_list.sort()
        return solution_list
    else:
        print("No solution!")
