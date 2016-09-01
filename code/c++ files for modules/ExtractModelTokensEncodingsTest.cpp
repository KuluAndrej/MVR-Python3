/*

Author: Kulunchakov Andrei
*/

#include <iostream>
#include <vector>
#include <string>
#include <utility>
#include <fstream> 
#include <stdlib.h>
#include "create_data_by_handle.h"

using namespace std;


string extract_tokens(const string handle){
  vector<string> model_tokens = create_tokens_of_model(handle);  
  string unite_tokens("");
  for (int i = 0; i < int(model_tokens.size()) - 1; ++i) {
    unite_tokens += model_tokens[i];
    unite_tokens += string("&");
  }
  if (model_tokens.size() > 0) {
    unite_tokens += model_tokens.back();
  }
  return unite_tokens;
}

int main() {
  string s = "expl_(frac2_(X[0],parameter_()))";
  string s1 = extract_tokens(s);
  cout << s1 << '\n';
}