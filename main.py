import code.DataLoader as DataLoader
import code.MVRAttributesExtraction as MVRAttributesExtraction
import code.DataFitting as DataFitting
import  code.DataPreprocesser as DataPreprocesser


# get a data structure with the MVR attributes
config = MVRAttributesExtraction.attributes_extraction()


data_to_fit = DataLoader.retrieve_data(config)
data_to_fit = DataPreprocesser.data_preprocesser(data_to_fit)

best_fitting_models = DataFitting.data_fitting(data_to_fit, config)





# after your program ends
#pr.print_stats(sort="calls")