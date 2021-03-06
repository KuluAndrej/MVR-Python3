"""
Main file responsible for launching rules creation.
Rule is a pair of models, one is called *pattern* model, the other is *replacement*.
Rules are used for models simplification.

Author: Kulunchakov Andrei
"""

import code.input_output.MVRAttributesExtraction as MVRAttributesExtraction
import code.model_processing.Parametrizer as Parametrizer
import code.input_output.ReadTokensInfoForOptimization as ReadTokensInfoForOptimization
import code.input_output.InitModelsLoader as InitModelsLoader
import code.rule_simplification.PatternsCreator as PatternsCreator
import code.rule_simplification.ReplacementsCreator as ReplacementsCreator
import code.model_processing.DefConstructor as DefConstructor
import code.rule_simplification.RuleSimplifier as  RuleSimplifier
import time

import code.model_processing.Parametrizer as Parametrizer
import code.input_output.InitModelsLoader as InitModelsLoader
import code.input_output.ConstructScipyOptimizeAttributes as ConstructScipyOptimizeAttributes
import code.rule_simplification.RuleSimplifier as RuleSimplifier
import code.input_output.ReadTokensInfoForOptimization as ReadTokensInfoForOptimization
import code.structures.Population as Population
from datetime import date
import datetime

def creator():
    file_output = open("data/output.txt","a+")
    file_output.write(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + "\n")

    config           = MVRAttributesExtraction.extract_config()
    dict_tokens_info = ReadTokensInfoForOptimization.read_info_tokens_for_optimization(config)

    # load initial superpositions
    print("Start retrieving initial models")
    init_models_for_rules = model_preparation(InitModelsLoader.retrieve_init_models(config)[:])
    init_models_to_fit = init_population_preparation(config,dict_tokens_info)


    if config['rules_creation']['regime'] == "create_patterns":
        for model in init_models_for_rules:
            PatternsCreator.creator(model, dict_tokens_info)

    elif config['rules_creation']['regime'] == "create_replacements":
        processed_patterns = open("data/Rules_creation_files/init_patterns_proc.txt").readlines()
        processed_patterns = [item.strip() for item in processed_patterns]
        print(len(init_models_for_rules),'patterns are to be processed')

        for ind, model in enumerate(init_models_for_rules):
            file_output.write(model.handle + "\n")
            if ind < 0:
                continue
            start = time.time()
            prev = model.handle
            model = RuleSimplifier.rule_simplify(Population.Population([model]), config)[0]
            if not prev == model.handle:
                continue
            if filtering(model, init_models_for_rules, ind):
                file_output.write("start fitting\n")
                print_intro(model, ind)

                if ReplacementsCreator.creator(model, init_models_to_fit,  dict_tokens_info, config):
                    file_output.write("...Success...\n")
                else:
                    file_output.write("...Fail...\n")
                print("elapsed time:",time.time() - start)
            else:
                file_output.write("--> %s is not processed.\n" % model.handle)
                pass

def print_intro(pattern, ind):
    print("Iteration %d. Start processing pattern: %s" % (ind, pattern))


def init_population_preparation(config,dict_tokens_info):
    population = InitModelsLoader.retrieve_init_models(config, source_of_launching="DataFitting")
    ConstructScipyOptimizeAttributes.construct_info_population(population,dict_tokens_info)
    population = Parametrizer.parametrize_population(population)
    population = DefConstructor.add_def_statements_attributes(population)

    print(len(population), "initial models are retrieved")
    return population

def model_preparation(init_models_for_rules):
    """
    We set some attributes important for futher creation
    """

    init_models_for_rules = Parametrizer.parametrize_population(init_models_for_rules)
    DefConstructor.add_def_statements_attributes(init_models_for_rules)

    return init_models_for_rules

def filtering(model, init_models_for_rules, ind):
    #if model in init_models_for_rules[0:ind] or model.handle in processed_patterns:
    #    return False
    if model in init_models_for_rules[0:ind]:
        return False
    if model.handle.count("minu") == 0:
        return False
    if len(model) == 1:
        return False
    if (not model.tokens.count("X[0]")) and model.tokens.count("X[1]"):
        return False
    return True

creator()


# To remember: the total number of rules generated by the first run of algo is 936