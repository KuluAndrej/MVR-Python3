"""
Main file responsible for launching rules creation.
Rule is a pair of models, one is called *pattern* model, the other is *replacement*.
Rules are used for models simplification.

Author: Kulunchakov Andrei
"""

def creator():

    import code.input_output.MVRAttributesExtraction as MVRAttributesExtraction
    import code.model_processing.Parametrizer as Parametrizer
    import code.input_output.ReadTokensInfoForOptimization as ReadTokensInfoForOptimization
    import code.input_output.InitModelsLoader as InitModelsLoader
    import code.rule_simplification.PatternsCreator as PatternsCreator
    import code.rule_simplification.ReplacementsCreator as ReplacementsCreator
    import code.model_processing.DefConstructor as DefConstructor

    config           = MVRAttributesExtraction.extract_config()
    dict_tokens_info = ReadTokensInfoForOptimization.read_info_tokens_for_optimization(config)

    # load initial superpositions
    init_models_for_rules = InitModelsLoader.retrieve_init_models(config)
    init_models_for_rules = Parametrizer.parametrize_population(init_models_for_rules)
    DefConstructor.add_def_statements_attributes(init_models_for_rules)


    if config['rules_creation']['regime'] == "create_patterns":
        for model in init_models_for_rules:
            PatternsCreator.creator(model, dict_tokens_info)

    elif config['rules_creation']['regime'] == "create_replacements":
        for model in init_models_for_rules:
            ReplacementsCreator.creator(model, dict_tokens_info, config)

creator()