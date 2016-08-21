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
models = sorted(models, key =  lambda x: (len(x), len(x.handle)))

population = Population(models)
population.unique_models_selection()
population.sort("len")
population = Parametrizer.parametrize_population(population)

file.close()
file = open(fname, 'w')

for model in population:
    file.write(model.handle)

file.close()

"""
"""
config           = MVRAttributesExtraction.extract_config()
dict_tokens_info = ReadTokensInfoForOptimization.read_info_tokens_for_optimization(config)

pattern = 'normal_(zero_())'
replacement = 'parameter_()'

population = Population([Model(pattern), Model(replacement)])
for model in population:
    print(model.number_of_terminals)
population = Parametrizer.parametrize_population(population)

DefConstructor.add_def_statements_attributes(population)
print('pattern =', population[0], "replacement =", population[1])

b = CheckReplacementForFitting.check(population[0], population[1], dict_tokens_info, config, False, True)
print(b[0])
"""
fname = "data/Rules_creation_files/received_rules.txt"
file = open(fname, 'r')

models = file.readlines()
models = [item.split()[0] for item in models]
print(len(models),len(set(models)))

