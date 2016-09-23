import math
import numpy as np
from code.primitives.Decorators import handicraft_exception_handler


def sinc_(w0, w1, x):
    sinc_.NumParam = 2
    sinc_.NumVars = 1
    sinc_.InitParams = [0,3]
    sinc_.BoundsParams = ([-1,2],[0.5,np.inf])
    sinc_.commutative = False

    return np.sinc(w1 * x + w0)


@handicraft_exception_handler
def sinla_(w0, w1, x):
    sinla_.NumParam = 2
    sinla_.NumVars = 1
    sinla_.InitParams = [0,4]
    sinla_.BoundsParams = ([-5,3.5],[5,5])
    sinla_.commutative = False

    return np.sin(w1 * (x - w0))

@handicraft_exception_handler
def sinha_(w0, w1, x):
    sinha_.NumParam = 2
    sinha_.NumVars = 1
    sinha_.InitParams = [0,9]
    sinha_.BoundsParams = ([-5,5.1],[5,np.inf])
    sinha_.commutative = False

    return np.sin(w1 * (x - w0))


@handicraft_exception_handler
def lnl_(w0, w1, x):
    lnl_.NumParam = 2
    lnl_.NumVars = 1
    lnl_.InitParams = [0,1]
    lnl_.BoundsParams = ([-5,0.5],[5,np.inf])
    lnl_.commutative = False

    return np.log10(abs(w1 * x + w0))

@handicraft_exception_handler
def expl_(w0, w1, x):
    expl_.NumParam = 2
    expl_.NumVars = 1
    expl_.InitParams = [0,1]
    expl_.BoundsParams = ([-5,0.5],[5,5])
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
    normal_.BoundsParams = ([-.75,0.05],[1,np.inf])
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
    linear_.BoundsParams = ([-50,-0.2],[50,5])
    linear_.commutative = False

    return w1 * x + w0


def parabola_(w0, w1, w2, x):
    parabola_.NumParam = 3
    parabola_.NumVars = 1
    parabola_.InitParams = [0,0,2]
    parabola_.BoundsParams = ([-np.inf,-4,1],[np.inf,4,np.inf])
    parabola_.commutative = False

    return x * x * w2 +  x * w1 + w0
