from code.modules.model_simplifier_by_rules import simplify_by_rules
from code.modules.patterns_extracter import extract_patterns
from code.modules.model_reconstructer import model_reconstruct
import re
import numpy as np

#handle = 'hyperbola_(linear_(parabola_(X[0])))'
#handle = re.sub(r'X\[(\d+)\]', r'x\1', handle)
def get_population_from_file(filename):

    lines_file_content = []
    files_path = 'populations/collected_models5/'
    with open(files_path + filename, 'r') as f_in:
        lines_file_content = (line.rstrip() for line in f_in) # All lines including the blank ones
        lines_file_content = [line for line in lines_file_content if line] # Non-blank lines
    population = np.empty(len(lines_file_content), dtype = object)

    for ind, entity in enumerate(lines_file_content):
        model_name = entity.split(' ')[-1]
        population[ind] = re.sub(r'X\[(\d+)\]', r'x\1', model_name.strip())
    return population

population = get_population_from_file('heart_rate_4.txt')
print(extract_patterns('lnl_(normal_(linear_(sina_(sina_(sina_(x0))))))'))
