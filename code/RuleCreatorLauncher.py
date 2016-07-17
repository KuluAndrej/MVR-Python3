"""
Main file responsible for launching rules creation.
Rule is a pair of models, one is called *pattern* model, the other is *replacement*.
Rules are used for models simplification.

Author: Kulunchakov Andrei
"""

import code.MVRAttributesExtraction as MVRAttributesExtraction
import code.DataLoader as DataLoader
import code.DataFitting as DataFitting
import code.DataPreprocesser as DataPreprocesser
import code.SegmentatorTS as SegmentatorTS
import code.ObserverTheBestFunction as ObserverTheBestFunction
import code.SavePopulationToFile as SavePopulationToFile
import code.PatternsCreator as PatternsCreator
import code.InitModelsRulesLoader as InitModelsRulesLoader
import code.ReplacementsCreator as ReplacementsCreator
import CutSegmentStoreToFile
import time
import matplotlib.pyplot as plt

config = MVRAttributesExtraction.extract_config(root = '../')

init_models_for_rules = InitModelsRulesLoader.loader(config)
if config['rules_creation']['regime'] == "from_replacements":

    for model in init_models_for_rules:
        # if we have fixed replacement model, we are to find a set of proper patterns
        PatternsCreator.creator(model)

elif config['rules_creation']['regime'] == "from_patterns":

    for model in init_models_for_rules:
        # if we have fixed replacement model, we are to find a set of proper patterns
        ReplacementsCreator.creator(model)

    # if we have fixed pattern model, we are to find a set of proper replacements
    PatternsCreator.creator(model)
