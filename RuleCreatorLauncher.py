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
import code.ReadTokensInfoForOptimization as ReadTokensInfoForOptimization
import code.InitModelsLoader as InitModelsLoader
import code.PatternsCreator as PatternsCreator
import code.ReplacementsCreator as ReplacementsCreator
import CutSegmentStoreToFile
import time
import matplotlib.pyplot as plt

config           = MVRAttributesExtraction.extract_config()
dict_tokens_info = ReadTokensInfoForOptimization.read_info_tokens_for_optimization(config)

init_models_for_rules = Parametrizer.parametrize_population(InitModelsLoader.retrieve_init_models(config))


if config['rules_creation']['regime'] == "create_patterns":
    for model in init_models_for_rules:
        PatternsCreator.creator(model, dict_tokens_info)

elif config['rules_creation']['regime'] == "create_replacements":
    for model in init_models_for_rules:
        ReplacementsCreator.creator(model, dict_tokens_info, config)

