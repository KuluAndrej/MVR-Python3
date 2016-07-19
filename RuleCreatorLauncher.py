"""
Main file responsible for launching rules creation.
Rule is a pair of models, one is called *pattern* model, the other is *replacement*.
Rules are used for models simplification.

Author: Kulunchakov Andrei
"""

def creator():

    import code.input_output.MVRAttributesExtraction as MVRAttributesExtraction
    import code.input_output.DataLoader as DataLoader
    import code.model_processing.Parametrizer as Parametrizer
    import code.DataFitting as DataFitting
    import code.data_processing.DataPreprocesser as DataPreprocesser
    import code.data_processing.SegmentatorTS as SegmentatorTS
    import code.ObserverTheBestFunction as ObserverTheBestFunction
    import code.input_output.SavePopulationToFile as SavePopulationToFile
    import code.input_output.ReadTokensInfoForOptimization as ReadTokensInfoForOptimization
    import code.input_output.InitModelsLoader as InitModelsLoader
    import code.rule_simplification.PatternsCreator as PatternsCreator
    import code.rule_simplification.ReplacementsCreator as ReplacementsCreator
    import code.model_processing.DefConstructor as DefConstructor
    import time
    import matplotlib.pyplot as plt
    import code.model_processing.SetModelRandomParameters as CreateModelRandomParameters


    config           = MVRAttributesExtraction.extract_config()
    print(type(config))
    dict_tokens_info = ReadTokensInfoForOptimization.read_info_tokens_for_optimization(config)

    init_models_for_rules = Parametrizer.parametrize_population(InitModelsLoader.retrieve_init_models(config))

    DefConstructor.add_def_statements_attributes(init_models_for_rules)
    if config['rules_creation']['regime'] == "create_patterns":
        for model in init_models_for_rules:
            PatternsCreator.creator(model, dict_tokens_info)

    elif config['rules_creation']['regime'] == "create_replacements":
        for model in init_models_for_rules:
            ReplacementsCreator.creator(model, dict_tokens_info, config)

creator()