"""
Either atomic propositions, or combinations of boolean expressions by means of "and" and "or"
Atomic propositions: - equality statements e1 = e2, - strict inequality e1 < e2
x = y
x < 15 and 7 < x
x < 15 or 20 < x
"""

from parserComb import *
from arithmExpression import *
from z3 import *

class BoolExpr(ArithmExpr):
    def __equal__(self, other):
        return Equal(self, other)
    def __lessThan__(self, other):
        return LessThan(self, other)
    def eval_(self, env):
        print("Error! eval is not implemented")
    def toZ3(self):
        print("Error! toZ3 is not implemented BoolExpr")


class BoolVar(BoolExpr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def eval_(self, env):
        return env[self.name]

    def toZ3(self):
        return Bool(f'{self.name}')

class CombBool(BoolExpr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return f"({self.left} {self.op} {self.right})"
    def eval_(self, env):
        return self.fun(self.left.eval_(env), self.right.eval_(env))
    def toZ3(self):
        left_val = self.left.toZ3()
        right_val = self.right.toZ3()

class OrB(CombBool):
    op = "or"
    fun = lambda _, x, y: x or y

    def toZ3(self):
        return Or(self.left.toZ3(), self.right.toZ3())

class AndB(CombBool):
    op = "and"
    fun = lambda _, x, y: x and y

    def toZ3(self):
        return And(self.left.toZ3(), self.right.toZ3())

class AtomicProp(BoolExpr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return f"({self.left} {self.op} {self.right})"
    def toZ3(self):
        left_val = self.left.toZ3()
        right_val = self.right.toZ3()

class Equal(AtomicProp):
    op = "="

    def eval_(self, env):
        left_val = self.left
        right_val = self.right
        if type(left_val) == int and type(right_val) == int:
            return left_val == right_val 
        elif type(left_val) != int and type(right_val) == int:
            number_left = left_val.eval_(env)
            return number_left == right_val
        elif type(left_val) == int and type(right_val) != int:
            number_right = right_val.eval_(env)
            return left_val == number_right
        elif type(left_val) != int and type(right_val) != int:
            number_left = left_val.eval_(env)
            number_right = right_val.eval_(env)
            return number_left == number_right
        else:
            left_val = self.left.eval_(env)
            right_val = self.right.eval_(env)
            return left_val == right_val 

    def toZ3(self):     
        left_val = self.left
        right_val = self.right
        if type(left_val) == int and type(right_val) == int:
            return left_val == right_val 
        elif type(left_val) != int and type(right_val) == int:
            number_left = left_val.toZ3()
            return number_left == right_val
        elif type(left_val) == int and type(right_val) != int:
            number_right = right_val.toZ3()
            return left_val == number_right
        elif type(left_val) != int and type(right_val) != int:
            number_left = left_val.toZ3()
            number_right = right_val.toZ3()
            return number_left == number_right
        else:
            left_val = self.left.toZ3()
            right_val = self.right.toZ3()
            return left_val == right_val


class LessThan(AtomicProp):
    op = "<"

    def eval_(self, env):
        left_val = self.left
        right_val = self.right
        if type(left_val) == int and type(right_val) == int:
            return left_val < right_val 
        elif type(left_val) != int and type(right_val) == int:
            number_left = left_val.eval_(env)
            return number_left < right_val
        elif type(left_val) == int and type(right_val) != int:
            number_right = right_val.eval_(env)
            return left_val < number_right
        elif type(left_val) != int and type(right_val) != int:
            number_left = left_val.eval_(env)
            number_right = right_val.eval_(env)
            return number_left < number_right
        else:
            left_val = self.left.eval_(env)
            right_val = self.right.eval_(env)
            return left_val < right_val 

    def toZ3(self):     
        left_val = self.left
        right_val = self.right
        if type(left_val) == int and type(right_val) == int:
            return left_val < right_val 
        elif type(left_val) != int and type(right_val) == int:
            number_left = left_val.toZ3()
            return number_left < right_val
        elif type(left_val) == int and type(right_val) != int:
            number_right = right_val.toZ3()
            return left_val < number_right
        elif type(left_val) != int and type(right_val) != int:
            number_left = left_val.toZ3()
            number_right = right_val.toZ3()
            return number_left < number_right
        else:
            left_val = self.left.toZ3()
            right_val = self.right.toZ3()
            return left_val < right_val



"""
<boolean_expression> ::= <disjunct> 'or' <boolean_expression> | <disjunct>
<disjunct>           ::= <conjunct> 'and' <disjunct> | <conjunct>
<conjunct>           ::= <arithm_expression> <cmp> <arithm_expression> | (<boolean_expression>)
<cmp>                ::= '=' | '<'
"""

class ParseBoolExpr(ParseArithmExpr):
    def __init__(self):
        self.parser = ParseOr() ^ ParseDisj()

class ParseDisj(Parser):
    def __init__(self):
        self.parser = ParseAnd() ^ ParseConj()

class ParseConj(Parser):
    def __init__(self):
        self.parser = ParseCMP() ^ ParseParenBoolExpr()

class ParseOr(Parser):
    def __init__(self):
        self.parser = ParseDisj()       >> (lambda d:
                      ParseSymbol('or') >> (lambda _:
                      ParseBoolExpr()   >> (lambda b:
                      Return(OrB(d, b)))))

class ParseAnd(Parser):
    def __init__(self):
        self.parser = ParseConj()        >> (lambda c:
                      ParseSymbol('and') >> (lambda _:
                      ParseDisj()        >> (lambda d:
                      Return(AndB(c, d)))))

class ParseParenBoolExpr(Parser):
    def __init__(self):
        self.parser = ParseSymbol('(') >> (lambda _:
                      ParseBoolExpr()  >> (lambda b:
                      ParseSymbol(')') >> (lambda _:
                      Return(b))))

class ParseCMP(Parser):
    def __init__(self):
        self.parser = ParseEqual() ^ ParseLessThan() 

class ParseEqual(Parser):
    def __init__(self):
        self.parser = (ParseArithmExpr() >> (lambda a: 
                       ParseSymbol('=')  >> (lambda _:
                       ParseArithmExpr() >> (lambda e:
                       Return(Equal(a, e))))))

class ParseLessThan(Parser):
    def __init__(self):
        self.parser = (ParseArithmExpr() >> (lambda a: 
                       ParseSymbol('<')  >> (lambda _:
                       ParseArithmExpr() >> (lambda e:
                       Return(LessThan(a, e))))))