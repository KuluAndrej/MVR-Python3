import code.RandomPopulation as RandomPopulation
from code.modules.patterns_extracter import extract_patterns
import code.ReadTokensInfoForOptimization as ReadTokensInfoForOptimization

model = 'tana_(normal_(normal_(mult_(sina_(x0)))))'
print(extract_patterns(model).split('&'))