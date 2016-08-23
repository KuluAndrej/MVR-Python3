import math
import numpy as np
from code.primitives.Decorators import handicraft_exception_handler

@handicraft_exception_handler
def bump_(w0, w1, x):
    bump_.NumParam = 2
    bump_.NumVars = 1
    bump_.InitParams = [0,1]
    bump_.BoundsParams = ([-np.inf,-np.inf],[np.inf,np.inf])
    bump_.commutative = False


    return x * np.logical_and(w0 < x, x < w1)

def sinc_(w0, w1, x):
    sinc_.NumParam = 2
    sinc_.NumVars = 1
    sinc_.InitParams = [0,3]
    sinc_.BoundsParams = ([-np.inf,-np.inf],[np.inf,np.inf])
    sinc_.commutative = False

    return np.sinc(w1 * x + w0)

@handicraft_exception_handler
def hvs_(w0, x):
    hvs_.NumParam = 1
    hvs_.NumVars = 1
    hvs_.InitParams = [0]
    hvs_.BoundsParams = ([-np.inf],[np.inf])
    hvs_.commutative = False

    return x * (w0 < x)

@handicraft_exception_handler
def sina_(w0, w1, x):
    sina_.NumParam = 2
    sina_.NumVars = 1
    sina_.InitParams = [0,4]
    sina_.BoundsParams = ([-np.inf,-np.inf],[np.inf,np.inf])
    sina_.commutative = False

    return np.sin(w1 * x + w0)


@handicraft_exception_handler
def lnl_(w0, w1, x):
    lnl_.NumParam = 2
    lnl_.NumVars = 1
    lnl_.InitParams = [0,1]
    lnl_.BoundsParams = ([-np.inf,-np.inf],[np.inf,np.inf])
    lnl_.commutative = False

    return np.log10(abs(w1 * x + w0))

@handicraft_exception_handler
def expl_(w0, w1, x):
    expl_.NumParam = 2
    expl_.NumVars = 1
    expl_.InitParams = [0,1]
    expl_.BoundsParams = ([-np.inf,-np.inf],[np.inf,np.inf])
    expl_.commutative = False

    return np.exp(w1 * x + w0)

def plus2_(x, y):
    plus2_.NumParam = 0
    plus2_.NumVars = 2
    plus2_.InitParams = []
    plus2_.BoundsParams = ([],[])
    plus2_.commutative = True

    return x + y

def minus2_(x, y):
    minus2_.NumParam = 0
    minus2_.NumVars = 2
    minus2_.InitParams = []
    minus2_.BoundsParams = ([],[])
    minus2_.commutative = False

    return x - y

def normal_(w0, w1, x):
    
    normal_.NumParam = 2
    normal_.NumVars = 1
    normal_.InitParams = [0,1]
    normal_.BoundsParams = ([-np.inf,0],[np.inf,np.inf])
    normal_.commutative = False

    return (1/w1) * np.exp(-(x - w0)**2/w1)


@handicraft_exception_handler
def frac2_(x, y):
    frac2_.NumParam = 0
    frac2_.NumVars = 2
    frac2_.InitParams = []
    frac2_.BoundsParams = ([],[])
    frac2_.commutative = False

    return x / y

@handicraft_exception_handler
def neg_(x):
    neg_.NumParam = 0
    neg_.NumVars = 1
    neg_.InitParams = []
    neg_.BoundsParams = ([],[])
    neg_.commutative = False

    return -x

def hypot_(x, y):
    hypot_.NumParam = 0
    hypot_.NumVars = 2
    hypot_.InitParams = []
    hypot_.BoundsParams = ([],[])
    hypot_.commutative = True

    return np.hypot(x, y)

def times2_(x, y):
    times2_.NumParam = 0
    times2_.NumVars = 2
    times2_.InitParams = []
    times2_.BoundsParams = ([],[])
    times2_.commutative = True

    return x * y

def linear_(w0, w1, x):
    linear_.NumParam = 2
    linear_.NumVars = 1
    linear_.InitParams = [0,0.5]
    linear_.BoundsParams = ([-np.inf,-np.inf],[np.inf,np.inf])
    linear_.commutative = False

    return w1 * x + w0


def parabola_(w0, w1, w2, x):
    parabola_.NumParam = 3
    parabola_.NumVars = 1
    parabola_.InitParams = [0,0,2]
    parabola_.BoundsParams = ([-np.inf,-np.inf,-np.inf],[np.inf,np.inf,np.inf])
    parabola_.commutative = False

    return x * x * w2 +  x * w1 + w0

def unity_():
    unity_.NumParam = 0
    unity_.NumVars = 0
    unity_.InitParams = []
    unity_.BoundsParams = ([],[])
    unity_.commutative = False

    return 1

def zero_():
    zero_.NumParam = 0
    zero_.NumVars = 0
    zero_.InitParams = []
    zero_.BoundsParams = ([],[])
    zero_.commutative = False

    return 0

def parameter_(w0):
    parameter_.NumParam = 1
    parameter_.NumVars = 0
    parameter_.InitParams = [0.5]
    parameter_.BoundsParams = ([-np.inf],[np.inf])
    parameter_.commutative = False

    return w0