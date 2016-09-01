from code.structures.Model import Model

class Population:
    class __Population:
        def __init__(self, models):
            self.Models = models
        def __str__(self):
            return (repr(self) + self.val)



    def __init__(self, models):
        if not isinstance(models, list):
            return NotImplemented
        if not all(isinstance(x, Model) for x in models):
            return NotImplemented


        self.Models = models

    def __len__(self):
        return len(self.Models)

    def __repr__(self):
        final_str = ''
        for ind, model in enumerate(self.Models):
            final_str += repr(ind) + ". " + repr(model) + "\n"
            #final_str += repr(model.MSE) + " " + repr(len(model)) + repr(model.number_of_parameters) + "\n"
            if hasattr(model, 'optimal_params'):
                final_str += str([item for item in model.optimal_params])[1:-1]
            final_str += "\n"
            if hasattr(model, 'MSE'):
                final_str += str(model.MSE)
            final_str += "\n"

        return final_str

    def __setitem__(self, index, model):
        if index >= len(self):
            raise IndexError
        self.Models[index] = model

    def sort(self):
        self.Models = sorted(self.Models, key=lambda model: model.MSE)

    def sort(self,type_of_selection,structural_penalty=0):
        if type_of_selection == 'MSE':
            self.Models = sorted(self.Models, key=lambda model: (model.MSE, len(model), model.number_of_parameters))
        elif type_of_selection == 'Error_structural':
            self.Models = sorted(self.Models, key=lambda model: model.MSE * (1 + structural_penalty * len(model)) )
        elif type_of_selection == 'Penalize_params':
            self.Models = sorted(self.Models, key=lambda model: model.Penalized_error)
        elif type_of_selection == 'len':
            self.Models = sorted(self.Models, key=lambda model: (len(model), len(model.handle)))
        elif type_of_selection == 'len_param':
            self.Models = sorted(self.Models, key=lambda model: (len(model), model.number_of_parameters, len(model.handle)))

    def __getitem__(self, key):
        if isinstance (key, slice):
            return Population([self.Models[ii] for ii in range(*key.indices(len(self)))])
        elif isinstance (key, int):
            return self.Models[key]
        else:
            raise (TypeError, "Invalid argument type.")
    def __bool__(self):
        return bool(self.Models)

    def append(self,listOfModels):
        if isinstance(listOfModels, Model):
            self.Models.append(listOfModels)
        if isinstance(listOfModels, list) and all(isinstance(model, Model) for model in listOfModels):
            self.Models.extend(listOfModels)

    def unique_models_selection(self):
        self.Models = list(set(self.Models))


    """
    Piece for implementing the class as singleton



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

    """
