"""
Main file responsible for launching rules creation.
Rule is a pair of models, one is called *pattern* model, the other is *replacement*.
Rules are used for models simplification.

Author: Kulunchakov Andrei
"""

import code.MVRAttributesExtraction as MVRAttributesExtraction
import code.DataLoader as DataLoader
import code.Parametrizer as Parametrizer
import code.DataFitting as DataFitting
import code.DataPreprocesser as DataPreprocesser
import code.SegmentatorTS as SegmentatorTS
import code.ObserverTheBestFunction as ObserverTheBestFunction
import code.SavePopulationToFile as SavePopulationToFile
import code.InitModelsLoader as InitModelsLoader
import code.PatternsCreator as PatternsCreator
import code.ReplacementsCreator as ReplacementsCreator
import CutSegmentStoreToFile
import time
import matplotlib.pyplot as plt

config = MVRAttributesExtraction.extract_config(root = '../')

init_models_for_rules = Parametrizer.parametrize_population(InitModelsLoader.retrieve_init_models(config))
print(init_models_for_rules)
"""
if config['rules_creation']['regime'] == "create_patterns":

    for model in init_models_for_rules:
        # if we have fixed replacement model, we are to find a set of proper patterns
        PatternsCreator.creator(model)

elif config['rules_creation']['regime'] == "create_replacements":

    for model in init_models_for_rules:
        # if we have fixed replacement model, we are to find a set of proper patterns
        ReplacementsCreator.creator(model)

    # if we have fixed pattern model, we are to find a set of proper replacements
    PatternsCreator.creator(model)
"""