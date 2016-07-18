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
def sinla_(w0, w1, x):
    if abs(w1) > 1:
        return np.inf
    sinla_.NumParam = 2
    sinla_.NumVars = 1
    return np.sin(x * w1 + w0)

def sinm1a_(w0, w1, x):
    if abs(w1) < 1 or abs(w1) > 2:
        return np.inf
    sinm1a_.NumParam = 2
    sinm1a_.NumVars = 1
    return np.sin(x * w1 + w0)

def sinm2a_(w0, w1, x):
    if abs(w1) < 2 or abs(w1) > 3:
        return np.inf
    sinm2a_.NumParam = 2
    sinm2a_.NumVars = 1
    return np.sin(x * w1 + w0)

def sinm3a_(w0, w1, x):
    if abs(w1) < 3 or abs(w1) > 4:
        return np.inf
    sinm3a_.NumParam = 2
    sinm3a_.NumVars = 1
    return np.sin(x * w1 + w0)

def sinm4a_(w0, w1, x):
    if abs(w1) < 4 or abs(w1) > 5:
        return np.inf
    sinm4a_.NumParam = 2
    sinm4a_.NumVars = 1
    return np.sin(x * w1 + w0)

def sinha_(w0, w1, x):
    if abs(w1) < 5:
        return np.inf
    sinha_.NumParam = 2
    sinha_.NumVars = 1
    return np.sin(x * w1 + w0)

@handicraft_exception_handler
def tana_(w0, w1, x):
    tana_.NumParam = 2
    tana_.NumVars = 1
    return np.tan(x * w1 + w0)

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
def atana_(w0, w1, x):
    if abs(w1) < 2:
        return 1000000
    atana_.NumParam = 2
    atana_.NumVars = 1

    return np.arctan(x * w1 + w0)

@handicraft_exception_handler
def lnl_(w0, w1, x):
    lnl_.NumParam = 2
    lnl_.NumVars = 1

    return np.log10(abs(x * w1 + w0))

@handicraft_exception_handler
def expl_(w0, w1, x):
    #if abs(w1)+abs(w0) > 6:
    #    return np.inf
    expl_.NumParam = 2
    expl_.NumVars = 1
    return np.exp(x * w1 + w0)

@handicraft_exception_handler
def sqrtl_(w0, w1, x):
    if abs(w1) < 0.2:
        return np.inf
    sqrtl_.NumParam = 2
    sqrtl_.NumVars = 1

    return np.sqrt(np.abs(x * w1 + w0))


def plus2_(x, y):
    plus2_.NumParam = 0
    plus2_.NumVars = 2

    return x + y

def plus_(w0, x):
    plus_.NumParam = 1
    plus_.NumVars = 1

    return x + w0


def normal_(w0, w1, x):
    if abs(w0) < 0.05:
        return np.inf
    normal_.NumParam = 2
    normal_.NumVars = 1

    return (1/w0) * np.exp(-(x - w1)**2/w0)


def bessel_(x):
    bessel_.NumParam = 0
    bessel_.NumVars = 1

    return np.i0(x)


def mult_(w0, x):
    if abs(w0 - 1) < .05:
        return np.inf
    plus_.NumParam = 1
    plus_.NumVars = 1

    return w0 * x



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

@handicraft_exception_handler
def hyperbola_(w0, x):

    hyperbola_.NumParam = 1
    hyperbola_.NumVars = 1

    return w0 / x


def times2_(x, y):
    times2_.NumParam = 0
    times2_.NumVars = 2

    return x * y

def linear_(w0, w1, x):
    if abs(w1) < .003:
        return np.inf
    linear_.NumParam = 2
    linear_.NumVars = 1

    return x * w1 + w0