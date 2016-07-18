import math
import numpy as np
from code.Decorators import handicraft_exception_handler

@handicraft_exception_handler
def bump_(w0, w1, x):
    bump_.NumParam = 2
    bump_.NumVars = 1
    bump_.InitParams = [.25,.75]
    bump_.BoundsParams = ([0,0],[1,1])

    return np.logical_and(w0 < x, x < w1)

@handicraft_exception_handler
def hvs_(w0, x):
    hvs_.NumParam = 1
    hvs_.NumVars = 1
    hvs_.InitParams = [.5]
    hvs_.BoundsParams = ([0],[1])

    return w0 < x

@handicraft_exception_handler
def sina_(w0, w1, x):
    sina_.NumParam = 2
    sina_.NumVars = 1
    sina_.InitParams = [0,2]
    sina_.BoundsParams = ([-1,1.5],[1,np.inf])

    return np.sin(x * w1 + w0)

@handicraft_exception_handler
def tana_(w0, w1, x):
    tana_.NumParam = 2
    tana_.NumVars = 1
    tana_.InitParams = [0,1]
    tana_.BoundsParams = ([-1,1],[1,np.inf])

    return np.tan(x * w1 + w0)

@handicraft_exception_handler
def atana_(w0, w1, x):
    atana_.NumParam = 2
    atana_.NumVars = 1
    atana_.InitParams = [0,1]
    atana_.BoundsParams = ([-1,1],[1,np.inf])

    return np.arctan(x * w1 + w0)

@handicraft_exception_handler
def lnl_(w0, w1, x):
    lnl_.NumParam = 2
    lnl_.NumVars = 1
    lnl_.InitParams = [0,1]
    lnl_.BoundsParams = ([-1,0.5],[1,np.inf])

    return np.log10(abs(x * w1 + w0))

@handicraft_exception_handler
def expl_(w0, w1, x):
    expl_.NumParam = 2
    expl_.NumVars = 1
    expl_.InitParams = [0,1]
    expl_.BoundsParams = ([-1,0.5],[1,5])

    return np.exp(x * w1 + w0)

@handicraft_exception_handler
def sqrtl_(w0, w1, x):
    sqrtl_.NumParam = 2
    sqrtl_.NumVars = 1
    sqrtl_.InitParams = [0,0.5]
    sqrtl_.BoundsParams = ([-1,0.2],[1,np.inf])

    return np.sqrt(np.abs(x * w1 + w0))


def plus2_(x, y):
    plus2_.NumParam = 0
    plus2_.NumVars = 2
    plus2_.InitParams = []
    plus2_.BoundsParams = ([],[])

    return x + y

def plus_(w0, x):
    plus_.NumParam = 1
    plus_.NumVars = 1
    plus_.InitParams = [0.2]
    plus_.BoundsParams = ([-1],[1])

    return x + w0


def normal_(w0, w1, x):
    
    normal_.NumParam = 2
    normal_.NumVars = 1
    normal_.InitParams = [0,1]
    normal_.BoundsParams = ([-1,0.05],[1,np.inf])

    return (1/w1) * np.exp(-(x - w0)**2/w1)


def mult_(w0, x):
    mult_.NumParam = 1
    mult_.NumVars = 1
    mult_.InitParams = [0.5]
    mult_.BoundsParams = ([0.3],[np.inf])

    return w0 * x



def minus2_(x, y):
    minus2_.NumParam = 0
    minus2_.NumVars = 2
    minus2_.InitParams = []
    minus2_.BoundsParams = ([],[])

    return x - y

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
    linear_.BoundsParams = ([-5,0.2],[5,5])

    return x * w1 + w0

