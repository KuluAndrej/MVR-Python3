from code.modules.model_simplifier_by_rules import simplify_by_rules
from code.modules.model_reconstructer import model_reconstruct
import re

#handle = 'hyperbola_(linear_(parabola_(X[0])))'
#handle = re.sub(r'X\[(\d+)\]', r'x\1', handle)
handle = 'plus2_(minus2_(x0,x0),hyperbola_(linear_(parabola_(x0))))'
print(simplify_by_rules(handle))

