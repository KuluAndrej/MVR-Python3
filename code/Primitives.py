import math
import numpy as np
from code.Decorators import handicraft_exception_handler

@handicraft_exception_handler
def sin_(x):
    sin_.NumParam = 0
    sin_.NumVars = 1
    return np.sin(x)

@handicraft_exception_handler
def cos_(x):
    cos_.NumParam = 0
    cos_.NumVars = 1
    return np.cos(x)

@handicraft_exception_handler
def tan_(x):
    tan_.NumParam = 0
    tan_.NumVars = 1
    return np.tan(x)

@handicraft_exception_handler
def atan_(x):
    atan_.NumParam = 0
    atan_.NumVars = 1

    return np.arctan(x)

@handicraft_exception_handler
def ln_(x):
    ln_.NumParam = 0
    ln_.NumVars = 1

    return np.log10(abs(x) + 0.000001)

@handicraft_exception_handler
def exp_(x):
    exp_.NumParam = 0
    exp_.NumVars = 1

    return np.exp(x)


@handicraft_exception_handler
def sqrt_(x):
    sqrt_.NumParam = 0
    sqrt_.NumVars = 1

    return np.sqrt(np.abs(x))

def plus2_(x, y):
    plus2_.NumParam = 0
    plus2_.NumVars = 2

    return x + y

def plus_(x):
    plus_.NumParam = 0
    plus_.NumVars = 1

    return x + 1

def minus2_(x, y):
    minus2_.NumParam = 0
    minus2_.NumVars = 2

    return x - y

@handicraft_exception_handler
def frac2_(x, y):
    frac2_.NumParam = 0
    frac2_.NumVars = 2
    return x / y

@handicraft_exception_handler
def inv_(x):
    inv_.NumParam = 0
    inv_.NumVars = 1

    return 1 / x

def times2_(x, y):
    times2_.NumParam = 0
    times2_.NumVars = 2

    return x * y





