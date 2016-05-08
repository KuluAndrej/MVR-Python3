import cProfile

import code.CrossoverPopulation as CrossoverPopulation
import code.DataLoader as DataLoader
import code.Evaluator as Evaluator
import code.InitModelsLoader as InitModelsLoader
import code.MVRAttributesExtraction as MVRAttributesExtraction
import code.MutationPopulation as MutationPopulation
import code.Parametrizer as Parametrizer
import code.QualityEstimator as QualityEstimator
import code.RandomPopulation as RandomPopulation
import code.SelectBestModels as SelectBestModels
import code.StringToModel as StringToModel
import code.UniqueModelsSelection as UniqueModelsSelection

population = RandomPopulation.random_population(1000, 2, 8)
"""
for i in range(100):
    for j in range (100):
        print(population[i], population[j])
        populationNew = CrossoverPopulation.crossover_population([population[i], population[j]], 2)
        populationNew = populationNew[-2:]
        Parametrizer.parametrize_population(population)
"""

population = StringToModel.strings_to_population(['ln_(frac2_(sqrt_(ln_(frac2_(X[0],X[1]))),X[1]))', 'lnl_(atana_(X[1]))'])
for i in range(100):
    populationNew = CrossoverPopulation.crossover_population(population, 10)
    Parametrizer.parametrize_population(populationNew)
