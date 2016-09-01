import math
import numpy as np
from code.Decorators import handicraft_exception_handler

@handicraft_exception_handler
def bump_(w0, w1, x):
    bump_.NumParam = 2
    bump_.NumVars = 1
    return np.logical_and(w0 < x, x < w1)

@handicraft_exception_handler
def hvs_(w0, x):
    hvs_.NumParam = 1
    hvs_.NumVars = 1
    return w0 < x


@handicraft_exception_handler
def sin_(x):
    sin_.NumParam = 0
    sin_.NumVars = 1
    return np.sin(x)

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

    return np.log10(abs(x))

@handicraft_exception_handler
def exp_(x):
    exp_.NumParam = 0
    exp_.NumVars = 1
    return np.exp(x)

@handicraft_exception_handler
def sqrtl_(x):
    sqrtl_.NumParam = 0
    sqrtl_.NumVars = 1

    return np.sqrt(np.abs(x))


def plus2_(x, y):
    plus2_.NumParam = 0
    plus2_.NumVars = 2

    return x + y

def plus_(w0, x):
    plus_.NumParam = 1
    plus_.NumVars = 1

    return x + w0


def normal_(x):
    normal_.NumParam = 0
    normal_.NumVars = 1

    return np.exp(-(x)**2)


def bessel_(x):
    bessel_.NumParam = 0
    bessel_.NumVars = 1

    return np.i0(x)




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