from z3 import *
from parserComb import *

class Expression():
    pass

"""
Integer constants, variables, addition and multiplication
42
x
x + 2*y
15 + x*x
x + y + z
"""

class ArithmExpr(Expression):
    def __add__(self, other):
        return Plus(self, other)

    def __mul__(self, other):
        return Times(self, other)

    def eval_(self, env):
        print("Error! eval is not implemented ArithmExpr")

    def toZ3(self):
        print("Error! toZ3 is not implemented ArithmExpr")

class Con(ArithmExpr):
    def __init__(self, val : float):
        self.val = val

    def __str__(self):
        return str(self.val)

    def __eq__(self, other):
        if type(other) == Con:
            return self.val == other.val
        return False

    def eval_(self, env):
        return self.val

    def vars_(self):
        return []

    def toZ3(self):
        self.val = Int(f'{self.val}')
        return self.val


class Var(ArithmExpr):
    def __init__(self, name : str):
        self.name = name
    
    def __str__(self):
        return self.name

    def __eq__(self, other):
        if type(other) == Var:
            return self.name == other.name
        return False

    def eval_(self, env):
        return env[self.name]

    def vars_(self):
        return [self.name]
    
    def toZ3(self):
        self.name = Int(f'{self.name}')
        return self.name


class BinOp(ArithmExpr):
    def __init__(self, left : ArithmExpr, right : ArithmExpr):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.op} {self.right})"

    def eval_(self, env):
        left_val = self.left.eval_(env)
        right_val = self.right.eval_(env)

    def vars_(self):
        return list(set(self.left.vars_() + self.right.vars_()))

    def toZ3(self):
        left_val = self.left.toZ3()
        right_val = self.right.toZ3()


class Plus(BinOp):
    op = "+"

    def fun(self, x, y):
        return x + y

    def eval_(self, env):
        left_val = self.left
        right_val = self.right
        if type(left_val) == int and type(right_val) == int:
            return left_val + right_val
        elif type(left_val) != int and type(right_val) == int:
            number_left = left_val.eval_(env)
            return number_left + right_val
        elif type(left_val) == int and type(right_val) != int:
            number_right = right_val.eval_(env)
            return left_val + number_right
        elif type(left_val) != int and type(right_val) != int:
            number_left = left_val.eval_(env)
            number_right = right_val.eval_(env)
            return number_left + number_right
        else:
            left_val = self.left.eval_(env)
            right_val = self.right.eval_(env)
            return left_val + right_val
    
    def toZ3(self):
        left_val = self.left
        right_val = self.right
        if type(left_val) == int and type(right_val) == int:
            return left_val + right_val
        elif type(left_val) != int and type(right_val) == int:
            number_left = left_val.toZ3()
            return number_left + right_val
        elif type(left_val) == int and type(right_val) != int:
            number_right = right_val.toZ3()
            return left_val + number_right
        elif type(left_val) != int and type(right_val) != int:
            number_left = left_val.toZ3()
            number_right = right_val.toZ3()
            return number_left + number_right
        else:
            left_val = self.left.toZ3()
            right_val = self.right.toZ3()
            return left_val + right_val


class Times(BinOp):
    op = "*"

    def fun(self, x, y):
        return x * y

    def eval_(self, env):
        left_val = self.left
        right_val = self.right
        if type(left_val) == int and type(right_val) == int:
            return left_val * right_val
        elif type(left_val) != int and type(right_val) == int:
            number_left = left_val.eval_(env)
            return number_left * right_val
        elif type(left_val) == int and type(right_val) != int:
            number_right = right_val.eval_(env)
            return left_val * number_right
        elif type(left_val) != int and type(right_val) != int:
            number_left = left_val.eval_(env)
            number_right = right_val.eval_(env)
            return number_left * number_right
        else:
            left_val = self.left.eval_(env)
            right_val = self.right.eval_(env)
            return left_val * right_val

    def toZ3(self):
        left_val = self.left
        right_val = self.right
        if type(left_val) == int and type(right_val) == int:
            return left_val * right_val
        elif type(left_val) != int and type(right_val) == int:
            number_left = left_val.toZ3()
            return number_left * right_val
        elif type(left_val) == int and type(right_val) != int:
            number_right = right_val.toZ3()
            return left_val * number_right
        elif type(left_val) != int and type(right_val) != int:
            number_left = left_val.toZ3()
            number_right = right_val.toZ3()
            return number_left * number_right
        else:
            left_val = self.left.toZ3()
            right_val = self.right.toZ3()
            return left_val * right_val




"""
<arithm_expression> ::= <term> '+' <arithm_expression> | <term>
<term>              ::= <factor> '*' <term> | <factor>
<factor>            ::= '(' <arithm_expression> ')' | <int> | <variable>
<int>               ::= INTEGER
<variable>          ::= IDENTIFIER 
"""

class ParseArithmExpr(Parser):
    def __init__(self):
        self.parser = ParsePlus() ^ ParseTerm()

class ParseTerm(Parser):
    def __init__(self):
        self.parser = ParseTimes() ^ ParseFactor()

class ParseFactor(Parser):
    def __init__(self):
        self.parser = ParseParen() ^ ParseInt() ^ ParseVar()

class ParseVar(Parser):
    def __init__(self):
        self.parser = ParseIdent() >> (lambda name:
                      Return(Var(name)))

class ParseParen(Parser):
    def __init__(self):
        self.parser = ParseSymbol('(')  >> (lambda _:
                      ParseArithmExpr() >> (lambda e:
                      ParseSymbol(')')  >> (lambda _:
                      Return(e))))

class ParsePlus(Parser):
    def __init__(self):
        self.parser = ParseTerm()            >> (lambda t:
                      ParseSymbol('+')       >> (lambda _:
                      ParseArithmExpr()      >> (lambda e:
                      Return(Plus(t, e)))))

class ParseTimes(Parser):
    def __init__(self):
        self.parser = ParseFactor()    >> (lambda x:
                      ParseSymbol('*') >> (lambda _:
                      ParseTerm()      >> (lambda y:
                      Return(Times(x, y)))))