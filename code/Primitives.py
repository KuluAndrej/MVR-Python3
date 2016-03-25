import math

def sin_(w, x):
    sin_.NumParam = 0
    sin_.NumVars = 1

    return math.sin(x)

def cos_(w, x):
    cos_.NumParam = 0
    cos_.NumVars = 1

    return math.cos(x)

def tan_(w, x):
    tan_.NumParam = 0
    tan_.NumVars = 1

    return math.tan(x)

def sina_(w, x):
    sina_.NumParam = 2
    sina_.NumVars = 1

    return math.sin(x * w[1] + w[0])

def cosa_(w, x):
    cosa_.NumParam = 2
    cosa_.NumVars = 1

    return math.cos(x * w[1] + w[0])

def tana_(w, x):
    tana_.NumParam = 2
    tana_.NumVars = 1

    return math.tan(x * w[1] + w[0])

def atan_(w, x):
    atan_.NumParam = 0
    atan_.NumVars = 1

    return math.atan(x)

def atana_(w, x):
    atana_.NumParam = 2
    atana_.NumVars = 1

    return math.atan(x * w[1] + w[0])

def ln_(w, x):
    ln_.NumParam = 0
    ln_.NumVars = 1

    return math.atan(x)

def lnl_(w, x):
    lnl_.NumParam = 2
    lnl_.NumVars = 1

    return math.atan(x * w[1] + w[0])


def exp_(w, x):
    exp_.NumParam = 0
    exp_.NumVars = 1

    return math.exp(x)


def expl_(w, x):
    expl_.NumParam = 2
    expl_.NumVars = 1

    return math.exp(x * w[1] + w[0])


def sqrt_(w, x):
    sqrt_.NumParam = 0
    sqrt_.NumVars = 1

    return math.sqrt(x)

def sqrtl_(w, x):
    sqrtl_.NumParam = 2
    sqrtl_.NumVars = 1

    return math.sqrt(x * w[1] + w[0])

def plus2_(w, x, y):
    plus2_.NumParam = 0
    plus2_.NumVars = 2

    return x + y

def plus_(w, x):
    plus_.NumParam = 1
    plus_.NumVars = 1

    return x + w[0]

def minus2_(w, x, y):
    minus2_.NumParam = 0
    minus2_.NumVars = 2

    return x - y

def frac2_(w, x, y):
    frac2_.NumParam = 0
    frac2_.NumVars = 2

    return x / y

def inv_(w, x):
    inv_.NumParam = 0
    inv_.NumVars = 1

    return 1 / x

def hyperbola_(w, x):
    hyperbola_.NumParam = 1
    hyperbola_.NumVars = 1

    return w[0] / x


def times2_(w, x, y):
    times2_.NumParam = 0
    times2_.NumVars = 2

    return x * y

def linear_(w, x):
    linear_.NumParam = 2
    linear_.NumVars = 1

    return x * w[1] + w[0]

def parabola_(w, x):
    parabola_.NumParam = 3
    parabola_.NumVars = 1
    
    return x * x * w[2] +  x * w[1] + w[0]






