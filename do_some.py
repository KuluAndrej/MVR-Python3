import code.input_output.MVRAttributesExtraction as MVRAttributesExtraction
import code.genetic_operations.RandomPopulation as RandomPopulation
import code.model_processing.Parametrizer as Parametrizer
import code.input_output.ReadTokensInfoForOptimization as ReadTokensInfoForOptimization
import code.input_output.InitModelsLoader as InitModelsLoader
import code.rule_simplification.PatternsCreator as PatternsCreator
import code.rule_simplification.ReplacementsCreator as ReplacementsCreator
import code.model_processing.DefConstructor as DefConstructor
import code.rule_simplification.CheckReplacementForFitting as CheckReplacementForFitting
from code.structures.Population import Population
from code.structures.Model import Model
import code.genetic_operations.MutationPopulation as MutationPopulation
import code.model_processing.Parametrizer as Parametrizer
import code.estimators_selectors.QualityEstimator as QualityEstimator
import code.genetic_operations.RandomPopulation as RandomPopulation
import code.estimators_selectors.SelectBestModels as SelectBestModels
import code.estimators_selectors.Evaluator as Evaluator
import code.input_output.InitModelsLoader as InitModelsLoader
import code.genetic_operations.CrossoverPopulation as CrossoverPopulation
import code.input_output.ConstructScipyOptimizeAttributes as ConstructScipyOptimizeAttributes
import code.rule_simplification.RuleSimplifier as RuleSimplifier
import code.input_output.ReadTokensInfoForOptimization as ReadTokensInfoForOptimization
import code.input_output.CreateBigRandomInitPopulation as CreateBigRandomInitPopulation
import code.model_processing.StringToModel as StringToModel
import code.input_output.MVRAttributesExtraction as MVRAttributesExtraction
import code.input_output.DataLoader as DataLoader
import code.DataFitting as DataFitting
import code.data_processing.DataPreprocesser as DataPreprocesser
import code.data_processing.SegmentatorTS as SegmentatorTS
import code.ObserverTheBestFunction as ObserverTheBestFunction
import code.input_output.SavePopulationToFile as SavePopulationToFile
import code.input_output.CutSegmentStoreToFile as CutSegmentStoreToFile
import code.input_output.CreateBigRandomInitPopulation as CreateBigRandomInitPopulation
import time, re
import numpy as np
import code.estimators_selectors.CalculatorModelValues as CalculatorModelValues
import matplotlib.patches as mpatches

import matplotlib.pyplot as plt
"""
lines = open("data/Rules_creation_files/proc_rules.txt",'r').readlines()
array = []
for ind, line in enumerate(lines):
    if ind % 2 == 0:
        array.append((line, lines[ind+1]))

array = sorted(array, key = lambda x: float(x[1].split()[0]))

file = open("data/Rules_creation_files/proc_rules.txt",'w')
for item in array:
    file.write(item[0]+item[1])

file.close()
"""
"""
from code.modules.model_reconstructer import model_reconstruct
fname = "data/Rules_creation_files/init_patterns.txt"
file = open(fname, 'r')
file_processed = open("data/Rules_creation_files/processed.txt", 'r')

models = file.readlines()
processed_models = file_processed.readlines()
models = [item for item in models if not item in processed_models]
models = list(map(Model, models))



for ind, model in enumerate(models):
    models[ind].handle = model_reconstruct(model.handle)


models = [item for item in models if len(item) > 1 and item]
models = sorted(models, key =  lambda x: (len(x), len(x.handle), x.handle))

population = Population(models)
population.unique_models_selection()
population.sort("len")
population = Parametrizer.parametrize_population(population)

file.close()
file = open(fname, 'w')

for model in population:
    file.write(model.handle + "\n")

file.close()
"""
"""
config           = MVRAttributesExtraction.extract_config()
dict_tokens_info = ReadTokensInfoForOptimization.read_info_tokens_for_optimization(config)

pattern = 'bump_(parameter_())'
replacement = 'zero_()'

population = Population([Model(pattern), Model(replacement)])
for model in population:
    print(model.number_of_terminals)
population = Parametrizer.parametrize_population(population)

DefConstructor.add_def_statements_attributes(population)
print('pattern =', population[0], "replacement =", population[1])

b = CheckReplacementForFitting.check(population[0], population[1], dict_tokens_info, config, False, True)
print(b[0])

"""

def plot_build():
    fname = "data/Rules_creation_files/received_rules.txt"
    init_patterns_file = "data/Rules_creation_files/init_patterns.txt"
    fname2 = "data/Rules_creation_files/received_rules_done.txt"
    primititives = open("code/primitives/Primitives.txt").readlines()[1:]

    file = open(fname, 'r')
    file2 = open(fname2, 'r')

    models = open(fname, 'r').readlines()
    models = [item.split()[0].strip() for item in models]
    models = [Model(item) for item in models]
    models = [Parametrizer.parametrize_model(item) for item in models]
    models_no_x1 = [item for item in models if not item.handle.count("X[1]")]
    #models_no_x1 = models
    print("new set:",len(models_no_x1),len(set(models_no_x1)))
    strcompl = [len(item) for item in models_no_x1]
    param = [item.number_of_parameters for item in models_no_x1]

    compl = np.unique(strcompl)
    pars  = np.unique(param)

    frequencies = np.zeros(len(primititives))
    for ind, func in enumerate(primititives):
        primitive = func.split()[0]
        for pattern in models_no_x1:
            if pattern.handle.count(primitive):
                frequencies[ind]+=1
    frequencies = frequencies / len(models_no_x1)

    for ind, func in enumerate(primititives):
        primitive = func.split()[0]
        print()
    print('\n'.join([repr(item)[0:4] for item in frequencies]))
    funcs = [item.split()[0] for item in primititives]

    argumentless = [item.split()[0].strip("_") for item in primititives if int(item.split()[2])==0]
    univariate_funcs = [item.split()[0].strip("_") for item in primititives if int(item.split()[2])==1]
    bivariate_funcs = [item.split()[0].strip("_") for item in primititives if int(item.split()[2])==2]

    freq_argumentless = [frequencies[ind] for ind,item in enumerate(primititives) if int(item.split()[2])==0]
    freq_univariate_funcs = [frequencies[ind] for ind,item in enumerate(primititives) if int(item.split()[2])==1]
    freq_bivariate_funcs = [frequencies[ind] for ind,item in enumerate(primititives) if int(item.split()[2])==2]

    for_sticks = []

    width = 0.5       # the width of the bars
    ind = 2*np.arange(len(argumentless))  # the x locations for the groups
    print(ind)
    for_sticks.extend(ind)
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, freq_argumentless, width, color='r')
    ind = max(ind) + 2 + 2*np.arange(len(univariate_funcs))
    for_sticks.extend(ind)
    print(ind)
    rects2 = ax.bar(ind, freq_univariate_funcs, width, color='y')
    ind = max(ind) + 2 + 2*np.arange(len(bivariate_funcs))
    for_sticks.extend(ind)
    print(ind)
    rects3 = ax.bar(ind, freq_bivariate_funcs, width, color='b')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(np.array(for_sticks) + width / 2)
    ax.set_xticklabels(tuple(argumentless + univariate_funcs + bivariate_funcs))
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 13}

    ax.legend((rects1[0], rects2[0],rects3[0]), ('Argumentless functions', 'Univariate functions', 'Bivariate functions'))
    plt.rc('font', **font)

    plt.show()

"""
for j in pars:
    print(" & ", end = "")
    print("\makebox[3em]{",j,"}", end = "")
print(r" \\\hline\hline", end = "")
print("")
for i in compl:
    print(i, end = "")
    for j in pars:
        pack = [item for item in models_no_x1 if len(item)==i and item.number_of_parameters == j]
        print(" & ",len(pack), end = "")
    print(r" \\\hline\hline")
"""



#print(done_rules)
#Population = Population(list(map(Model, done_patterns)))
#print("population size =", len(Population))
#print("old set:",len(done_patterns),len(set(done_patterns)))
"""

done_models = file2.readlines()
done_patterns = [item.split()[0] for item in done_models]
done_replaces = [item.split()[1] for item in done_models]
done_rules = [[Model(item.split()[0]),Model(item.split()[1])] for item in done_models]
unique_patterns = list(set(done_patterns))

done_rules = [done_rules[done_patterns.index(item)] for item in unique_patterns]

done_rules = sorted(done_rules, key =  lambda x: models.index(x[0].handle))

with open(fname2,'w') as file:
    for rule in done_rules:
        file.write(repr(rule[0]) + " " + repr(rule[1]) + "\n")
    file.close()

"""

def transform_rules():
    data = open("data/rules.txt", 'r').readlines()
    outp = open("data/rules.txt", 'w')

    for line in data:
        if line.count("sina_") > 0:
            backup = line
            backup = backup.replace("sina_", "sinla_")
            line = line.replace("sina_", "sinha_")
            outp.write(backup)
            outp.write(line)
        else:
            outp.write(line)
    outp.close()

def compare_trajectories(filename_rules, filename):
    file_rules = open(filename_rules,'r')
    file = open(filename,'r')

    matrix_of_measurements_rules = np.zeros(25)
    count = 0
    for line in file_rules.readlines():
        if line[0]=='[' and line[-2]==']':
            if len(eval(line)) == 25:
                matrix_of_measurements_rules += np.array(eval(line[:-1]))
                count  += 1
    matrix_of_measurements_rules /= count

    matrix_of_measurements = np.zeros(25)
    count = 0
    for line in file.readlines():
        if line[0]=='[' and line[-2]==']':
            if len(eval(line)) == 25:
                matrix_of_measurements += np.array(eval(line[:-1]))
                count  += 1

    matrix_of_measurements /= count
    plt.plot(matrix_of_measurements_rules,'b',matrix_of_measurements,'r')
    plt.rc('text', usetex=True)
    plt.rcParams.update({'font.size': 12})

    red_patch = mpatches.Patch(color='red', label='With rule rewriting')
    blue_patch = mpatches.Patch(color='blue', label='Without rule rewriting')
    plt.legend(handles=[red_patch, blue_patch])

    plt.title(r'Evolution of error for \lambda = 0')
    plt.show()
    matrix_of_measurements_rules /= matrix_of_measurements
    print(matrix_of_measurements_rules)

def compare_lengths():
    file_rules = open("results/with rules",'r')
    file = open("results/without rules",'r')


def rewrite_strings_from_file_to_file():
    file_rules = open("results/Сентябрь 01, 2016/fit models to options",'r')
    file1 = open("results/Сентябрь 02, 2016/fit models to options2",'r')
    lines = file1.readlines()
    file_rules.close()
    file1.close()

    start_line_index = -1
    file_rules_write = open("results/Сентябрь 01, 2016/fit models to options",'a')
    file_write = open("results/Сентябрь 01, 2016/fit models to options2",'w')
    print(len(lines))
    for ind, line in enumerate(lines):
        if ind >= start_line_index:
            file_rules_write.write(line)
        else:
            file_write.write(line)

    file_write.close()
    file_rules_write.close()

def find_number_of_launches(filename = "results/without rules MSE"):
    source = open(filename,'r')
    count = 0
    for line in source.readlines():
        if line.startswith("Launch"):
            count += 1

    print(count)

def recopy_content_of_file():
    source = open("results/Сентябрь 01, 2016/fit models to options2",'r')
    destiny = open("results/without rules",'w')

    for line in source.readlines():
        destiny.write(line)

    source.close()
    destiny.close()

def parse_file(filename = "results/Only MSE/without rules MSE"):
    file = open(filename,'r')
    """
    for line in file.readlines():
        if line.startswith("Launch"):
            launches.append([])
        else:
            launches[-1].append(line)

    return launches[1:]
    """
    launches = [[]]
    for line in file.readlines():
        if line[0]=='[' and line[-2]==']':
            if len(eval(line)) == 25:
                launches.append([])
        else:
            launches[-1].append(line)


    return launches[::2]


def process_one_launch(launch):
    populations = []
    for line in launch:
        if re.match("\d+. (.*)",line):
            pieces = line.split()
            index = int(pieces[0][:-1])
            func  = pieces[1].strip()
            if index == 0:
                populations.append([])
            populations[-1].append(Model(func))
    return populations

def get_average_lengths(launches):
    last_populations = []
    for ind, launch in enumerate(launches):
        pops = process_one_launch(launch)
        if pops:
            last_populations.append(process_one_launch(launch)[-1])
    average_lengths = []
    for item in last_populations:
        average_lengths.append([])
        for model in item:
            average_lengths[-1].append(len(model))
        try:
            average_lengths[-1] = np.mean(average_lengths[-1])
        except:
            print(average_lengths)

    return np.mean(average_lengths)

def analysis_populations(fname_rules, fname):
    launches = parse_file(filename = fname_rules)
    av_length = get_average_lengths(launches)
    print(av_length)

    launches = parse_file(filename = fname)
    av_length = get_average_lengths(launches)
    print(av_length)

fname_rules = "results/with rules MSE"
fname = "results/without rules MSE"

find_number_of_launches(fname)
find_number_of_launches(fname)
compare_trajectories(fname_rules, fname)
#analysis_populations(fname_rules, fname)
#launches = parse_file(filename = "results/With parsimony pressure 0.01/with rules")

