import math
import numpy as np
from code.Decorators import handicraft_exception_handler

@handicraft_exception_handler
def bump_(w0, w1, x):
    bump_.NumParam = 2
    bump_.NumVars = 1
    bump_.InitParams = [0,1]
    bump_.BoundsParams = ([-1,-1],[1,1])

    return x * np.logical_and(w0 < x, x < w1)

@handicraft_exception_handler
def hvs_(w0, x):
    hvs_.NumParam = 1
    hvs_.NumVars = 1
    hvs_.InitParams = [0]
    hvs_.BoundsParams = ([-1],[1])

    return x * (w0 < x)

@handicraft_exception_handler
def sinla_(w0, w1, x):
    sinla_.NumParam = 2
    sinla_.NumVars = 1
    sinla_.InitParams = [0,4]
    sinla_.BoundsParams = ([-5,3.5],[5,5])

    return np.sin(x * w1 + w0)

@handicraft_exception_handler
def sinha_(w0, w1, x):
    sinha_.NumParam = 2
    sinha_.NumVars = 1
    sinha_.InitParams = [0,9]
    sinha_.BoundsParams = ([-5,5.1],[5,np.inf])

    return np.sin(x * w1 + w0)

@handicraft_exception_handler
def lnl_(w0, w1, x):
    lnl_.NumParam = 2
    lnl_.NumVars = 1
    lnl_.InitParams = [0,1]
    lnl_.BoundsParams = ([-5,0.5],[5,np.inf])

    return np.log10(abs(x * w1 + w0))

@handicraft_exception_handler
def expl_(w0, w1, x):
    expl_.NumParam = 2
    expl_.NumVars = 1
    expl_.InitParams = [0,1]
    expl_.BoundsParams = ([-5,0.5],[5,5])

    return np.exp(x * w1 + w0)

def plus2_(x, y):
    plus2_.NumParam = 0
    plus2_.NumVars = 2
    plus2_.InitParams = []
    plus2_.BoundsParams = ([],[])

    return x + y


def normal_(w0, w1, x):
    
    normal_.NumParam = 2
    normal_.NumVars = 1
    normal_.InitParams = [0,1]
    normal_.BoundsParams = ([-.75,0.05],[1,np.inf])

    return (1/w1) * np.exp(-(x - w0)**2/w1)


@handicraft_exception_handler
def frac2_(x, y):
    frac2_.NumParam = 0
    frac2_.NumVars = 2
    frac2_.InitParams = []
    frac2_.BoundsParams = ([],[])

    return x / y

@handicraft_exception_handler
def inv_(x):
    inv_.NumParam = 0
    inv_.NumVars = 1
    inv_.InitParams = []
    inv_.BoundsParams = ([],[])

    return 1 / x

@handicraft_exception_handler
def neg_(x):
    neg_.NumParam = 0
    neg_.NumVars = 1
    neg_.InitParams = []
    neg_.BoundsParams = ([],[])

    return -x

def times2_(x, y):
    times2_.NumParam = 0
    times2_.NumVars = 2
    times2_.InitParams = []
    times2_.BoundsParams = ([],[])

    return x * y

def linear_(w0, w1, x):
    linear_.NumParam = 2
    linear_.NumVars = 1
    linear_.InitParams = [0,0.5]
    linear_.BoundsParams = ([-50,0.2],[50,5])

    return x * w1 + w0


def parabola_(w0, w1, w2, x):
    parabola_.NumParam = 3
    parabola_.NumVars = 1
    parabola_.InitParams = [0,0,2]
    parabola_.BoundsParams = ([-np.inf,-4,1],[np.inf,4,np.inf])
    
    return x * x * w2 +  x * w1 + w0

