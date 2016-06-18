from code.structures.Model import Model
from functools import wraps

class Population:
    class __Population:
        def __init__(self, models):
            self.Models = models
        def __str__(self):
            return (repr(self) + self.val)

    __instance = None


    def __init__(self, models):
        if not isinstance(models, list):
            return NotImplemented
        if not all(isinstance(x, Model) for x in models):
            return NotImplemented

        if not Population.__instance:
            Population.__instance = Population.__Population(models)
        else:
            # initialize with list of models
            self.__instance.Models = models

    def __len__(self):
        return len(self.__instance.Models)

    def __repr__(self):
        final_str = ''
        for ind, model in enumerate(self.__instance.Models):
            final_str += repr(ind) + ". " + repr(model) + "\n"
        return final_str

    def __setitem__(self, index, model):
        if index >= len(self):
            raise IndexError
        self.Models[index] = model

    def sort(self):
        self.__instance.Models = sorted(self.__instance.Models, key=lambda model: model.MSE)

    def sort(self,type_of_selection,structural_penalty):
        if type_of_selection == 'MSE':
            self.__instance.Models = sorted(self.__instance.Models, key=lambda model: model.MSE)
        elif type_of_selection == 'Error_structural':
            self.__instance.Models = sorted(self.__instance.Models, key=lambda model: model.MSE * (1 + structural_penalty * model.number_of_tokens) )


    def __getitem__(self, key):
        if isinstance (key, slice):
            return Population([self.__instance.Models[ii] for ii in range(*key.indices(len(self)))])
        elif isinstance (key, int):
            return self.__instance.Models[key]
        else:
            raise (TypeError, "Invalid argument type.")

    def append(self,listOfModels):
        if isinstance(listOfModels, Model):
            self.__instance.Models.extend(listOfModels)
        if isinstance(listOfModels, list) and all(isinstance(model, Model) for model in listOfModels):
            self.__instance.Models.extend(listOfModels)

    def unique_models_selection(self):
        self.__instance.Models = list(set(self.__instance.Models))
