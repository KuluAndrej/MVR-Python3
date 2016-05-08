from code.structures.Model import Model

class Population:
    def __init__(self, models):
        if not isinstance(models, list):
            return NotImplemented
        if not all(isinstance(x, Model) for x in models):
            return NotImplemented
        # initialize with list of models
        self.Models = models

    def __len__(self):
        return len(self.Models)

    def __repr__(self):
        final_str = ''
        for ind, model in enumerate(self.Models):
            final_str += repr(ind) + ". " + repr(model) + "\n"
        return final_str

    def __setitem__(self, index, model):
        if index >= len(self):
            raise IndexError
        self.Models[index] = model

    def sort(self):
        self.Models = sorted(self.Models, key=lambda model: model.MSE)


    def __getitem__(self, key):
        if isinstance (key, slice):
            #Get the start, stop, and step from the slice
            return Population([self.Models[ii] for ii in range(*key.indices(len(self)))])
        elif isinstance (key, int):
            return self.Models[key] #Get the data from elsewhere
        else:
            raise (TypeError, "Invalid argument type.")


    def __add__(self, obj):
        if isinstance(obj, Model):
            self.Models.append(obj)
            return self
        if isinstance(obj, Population):
            self.Models += obj.Models
            return self
        if not ( isinstance(obj, Model) or isinstance(obj, Population)):
            return NotImplemented