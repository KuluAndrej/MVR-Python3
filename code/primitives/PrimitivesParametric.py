import math
import numpy as np
from code.Decorators import handicraft_exception_handler

@handicraft_exception_handler
def sin_(x):
    sin_.NumParam = 0
    sin_.NumVars = 1
    return np.sin(x)

@handicraft_exception_handler
def bump_(w0, w1, x):
    sin_.NumParam = 2
    sin_.NumVars = 1
    return np.logical_and(w0 < x, x < w1)

@handicraft_exception_handler
def hvs_(w0, x):
    sin_.NumParam = 1
    sin_.NumVars = 1
    return w0 < x


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
def sina_(w0, w1, x):
    sina_.NumParam = 2
    sina_.NumVars = 1
    return np.sin(x * w1 + w0)

@handicraft_exception_handler
def cosa_(w0, w1, x):
    cosa_.NumParam = 2
    cosa_.NumVars = 1
    return np.cos(x * w1 + w0)

@handicraft_exception_handler
def tana_(w0, w1, x):
    tana_.NumParam = 2
    tana_.NumVars = 1
    return np.tan(x * w1 + w0)

@handicraft_exception_handler
def atan_(x):
    atan_.NumParam = 0
    atan_.NumVars = 1

    return np.arctan(x)

@handicraft_exception_handler
def atana_(w0, w1, x):
    atana_.NumParam = 2
    atana_.NumVars = 1

    return np.arctan(x * w1 + w0)

@handicraft_exception_handler
def ln_(x):
    ln_.NumParam = 0
    ln_.NumVars = 1

    return np.log10(abs(x) + 0.000001)

@handicraft_exception_handler
def lnl_(w0, w1, x):
    lnl_.NumParam = 2
    lnl_.NumVars = 1

    return np.log10(abs(x * w1 + w0))



@handicraft_exception_handler
def exp_(x):
    exp_.NumParam = 0
    exp_.NumVars = 1

    return np.exp(x)


@handicraft_exception_handler
def expl_(w0, w1, x):
    expl_.NumParam = 2
    expl_.NumVars = 1
    return np.exp(x * w1 + w0)


@handicraft_exception_handler
def sqrt_(x):
    sqrt_.NumParam = 0
    sqrt_.NumVars = 1

    return np.sqrt(np.abs(x))

@handicraft_exception_handler
def sqrtl_(w0, w1, x):
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


def normal_(x):
    normal_.NumParam = 0
    normal_.NumVars = 1

    return np.exp(-x**2)

def hypo2_(x,y):
    hypo2_.NumParam = 0
    hypo2_.NumVars = 2

    return np.hypot(x,y)

def sinh_(x):
    sinh_.NumParam = 0
    sinh_.NumVars = 1

    return np.sinh(x)

def cosh_(x):
    cosh_.NumParam = 0
    cosh_.NumVars = 1

    return np.cosh(x)

def tanh_(x):
    tanh_.NumParam = 0
    tanh_.NumVars = 1

    return np.tanh(x)

def arcsinh_(x):
    arcsinh_.NumParam = 0
    arcsinh_.NumVars = 1

    return np.arcsinh(x)

def arccosh_(x):
    arccosh_.NumParam = 0
    arccosh_.NumVars = 1

    return np.arccosh(x)

def arctanh_(x):
    arctanh_.NumParam = 0
    arctanh_.NumVars = 1

    return np.arctanh(x)

def bessel_(x):
    bessel_.NumParam = 0
    bessel_.NumVars = 1

    return np.i0(x)

def sinc_(x):
    sinc_.NumParam = 0
    sinc_.NumVars = 1

    return np.sinc(x)
    

def mult_(w0, x):
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
    linear_.NumParam = 2
    linear_.NumVars = 1

    return x * w1 + w0

def parabola_(w0, w1, w2, x):
    parabola_.NumParam = 3
    parabola_.NumVars = 1
    
    return x * x * w2 +  x * w1 + w0
