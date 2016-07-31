class Primitive:
    def __init__(self, handle, number_params, number_args):
        # name of a model
        self.handle = handle
        self.number_params = number_params
        self.number_args   = number_args

    def __repr__(self):
        return self.handle

    def __str__(self):
        return self.handle
    def __add__(self, x):
        if not (isinstance(x,str) or isinstance(x,Primitive)):
            return NotImplemented

        if isinstance(x,str):
            return self.handle + x
        if isinstance(x,self.__class__):
            return self.handle + x.handle

        return self.handle + x