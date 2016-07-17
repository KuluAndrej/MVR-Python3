from code.modules.extract_model_tokens_encodings import extract_tokens
import re

print(re.sub(r'X\[(\d+)\]', r'x\1', 'normal_(X[0])'))
print(extract_tokens('normal_(X[0])'))