from numpy import array
import re
from code.modules.extract_model_tokens_encodings import extract_tokens

class Model:
    def __init__(self, handle):
        # name of a model
        self.handle = handle
        self.second_handle = re.sub(r'X\[(\d+)\]', r'x\1', self.handle)
        self.tokens = extract_tokens(self.second_handle).split('&')
        self.number_of_terminals = len([item for item in self.tokens if re.match(r'x(\d+)', item)])

    def __len__(self):
        return len(self.tokens)

    def __repr__(self):
        return self.handle

    def __hash__(self):
        return hash(self.handle)

    def __eq__(self, other):
        if not isinstance(other, Model):
            return NotImplemented
        return self.handle == other.handle