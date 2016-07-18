"""
Functionality for storing values of pattern model to file.

We have a pattern model, say f(x,...). We create a grid and calculate the values of f(x,...)
on it. These values are used to construct another, simpler model, which acts as replacement
model.

Author: Kulunchakov Andrei, MIPT
"""

from numpy import random, linspace
import code.CalculatorModelValues as CalculatorModelValues

def loader(pattern_model, config):

    filename = config["rules_creation"]["rule_values"]
    grid =
    values  = CalculatorModelValues

