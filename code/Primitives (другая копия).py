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
def sina_(w0, w1, x):
    sina_.NumParam = 2
    sina_.NumVars = 1
    return np.sin(x * (0.5 + abs(w1)) + w0)

@handicraft_exception_handler
def tana_(w0, w1, x):
    tana_.NumParam = 2
    tana_.NumVars = 1
    return np.tan(x * (0.5 + abs(w1)) + w0)

@handicraft_exception_handler
def atana_(w0, w1, x):
    atana_.NumParam = 2
    atana_.NumVars = 1

    return np.arctan(x * (0.5 + abs(w1)) + w0)

@handicraft_exception_handler
def lnl_(w0, w1, x):
    lnl_.NumParam = 2
    lnl_.NumVars = 1

    return np.log10(abs(x * (0.5 + abs(w1)) + w0))

@handicraft_exception_handler
def expl_(w0, w1, x):
    expl_.NumParam = 2
    expl_.NumVars = 1
    return np.exp(x * (0.5 + abs(w1)) + w0)

@handicraft_exception_handler
def sqrtl_(w0, w1, x):
    sqrtl_.NumParam = 2
    sqrtl_.NumVars = 1

    return np.sqrt(np.abs(x * (0.5 + abs(w1)) + w0))


def plus2_(x, y):
    plus2_.NumParam = 0
    plus2_.NumVars = 2

    return x + y

def plus_(w0, x):
    plus_.NumParam = 1
    plus_.NumVars = 1

    return x + w0


def normal_(w0, w1, x):
    normal_.NumParam = 2
    normal_.NumVars = 1

    return (0.5 + abs(w0)) * np.exp(-(x - w1)**2)

def sinh_(w0, w1, x):
    sinh_.NumParam = 2
    sinh_.NumVars = 1

    return np.sinh(x * (0.5 + abs(w1)) + w0)

def cosh_(w0, w1, x):
    cosh_.NumParam = 2
    cosh_.NumVars = 1

    return np.cosh(x * (0.5 + abs(w1)) + w0)

def tanh_(w0, w1, x):
    tanh_.NumParam = 2
    tanh_.NumVars = 1

    return np.tanh(x * (0.5 + abs(w1)) + w0)

def arcsinh_(w0, w1, x):
    arcsinh_.NumParam = 2
    arcsinh_.NumVars = 1

    return np.arcsinh(x * (0.5 + abs(w1)) + w0)

def arccosh_(w0, w1, x):
    arccosh_.NumParam = 2
    arccosh_.NumVars = 1

    return np.arccosh(x * (0.5 + abs(w1)) + w0)

def arctanh_(w0, w1, x):
    arctanh_.NumParam = 2
    arctanh_.NumVars = 1

    return np.arctanh(x * (0.5 + abs(w1)) + w0)

def bessel_(w0, w1, x):
    bessel_.NumParam = 2
    bessel_.NumVars = 1

    return np.i0(x * (0.5 + abs(w1)) + w0)

def sinc_(w0, w1, x):
    sinc_.NumParam = 2
    sinc_.NumVars = 1

    return np.sinc(x * (0.5 + abs(w1)) + w0)


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
def hyperbola_(w0, x):
    hyperbola_.NumParam = 1
    hyperbola_.NumVars = 1

    return (0.5 + abs(w0)) / x


def times2_(x, y):
    times2_.NumParam = 0
    times2_.NumVars = 2

    return x * y

def linear_(w0, w1, x):
    linear_.NumParam = 2
    linear_.NumVars = 1

    return x * (0.5 + abs(w1)) + w0

def parabola_(w0, w1, w2, x):
    parabola_.NumParam = 3
    parabola_.NumVars = 1
    
    return x * x * (0.5 + abs(w2)) +  x * w1 + w0
