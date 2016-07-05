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

#include <boost/python/def.hpp>
#include <boost/python/module.hpp>

namespace bp = boost::python;





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


BOOST_PYTHON_MODULE(extract_model_tokens_encodings) {
	bp::def("extract_tokens", extract_tokens);
    	
}