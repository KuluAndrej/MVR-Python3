from code.modules.model_simplifier_by_rules import simplify_by_rules
import re

#handle = 'hyperbola_(linear_(parabola_(X[0])))'
#handle = re.sub(r'X\[(\d+)\]', r'x\1', handle)
handle = 'hyperbola_(linear_(parabola_(plus_(x0)))'
print(simplify_by_rules(handle))