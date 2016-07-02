import code.RandomPopulation as RandomPopulation
import code.MVRAttributesExtraction as MVRAttributesExtraction
import code.ReadTokensInfoForOptimization as ReadTokensInfoForOptimization

config = MVRAttributesExtraction.attributes_extraction()
dicto = ReadTokensInfoForOptimization.read_info_tokens_for_optimization(config)
print(dicto["minus2_"])
