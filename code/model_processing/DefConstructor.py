
def def_constructor(model):
    """
    Constructs a python def definition for 'model'.
    Inputs:
     model                  - structure storing a superposition of primitive functions and
        an information related with it

    Outputs:
     def_statement          - python def statement for 'model'
    """
    base_string = "lambda X"
    list_of_parameters = [ ",w" + str(i + 1) for i in range(model.number_of_parameters)]
    parameters_string = ''.join(list_of_parameters)
    base_string += parameters_string
    base_string += ": "
    base_string += model.param_handle

    def_statement = eval(base_string)

    return def_statement