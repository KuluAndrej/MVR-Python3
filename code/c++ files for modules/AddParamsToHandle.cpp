/*

Add parameters to the handle of a superposition

As some primitive functions have parameters, we should add them into the handle of a superposition containing them
Example:

	initial model:
	exp_(sqrta_(lnl_(frac2_(x1,x2))))

	parametered_model:
	exp_(sqrta_(w0, w1, lnl_(w2, w3, frac2_(x1,x2))))

Input:

	handle 				- string name of an unparametered superposition

Output
	
	parametered_handle 	- string name of the parametered version of the 'handle'


Author: Kulunchakov Andrei
*/

#include <string>
#include <vector>
#include "ExtractTokensFromHandle.h"
#include "FindTokensPositionsRange.h"
#include <boost/lexical_cast.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/implicit.hpp>

#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
namespace bp = boost::python;

using namespace std;
pair<string, int> parametrizing(const char* handle_char) {
	string handle(handle_char);

	// extract tokens presented in the superposition	
	pair<vector<PrimitiveFunction>, vector<int> > info_tokens = extract_tokens_from_handle(handle);
	vector<PrimitiveFunction> tokens_from_handle = info_tokens.first; 

	vector<int> first_positions = info_tokens.second;

	// if the superposition is a simple variable, we are nothing to do
	if (tokens_from_handle.size() == 1 and tokens_from_handle[0].name.size() and tokens_from_handle[0].name[1]=='[') {		
		return make_pair(handle, 0);
	}
	
	// number of parameters inserted in the superposition 'handle' yet
	int number_inserted_params = 0;
	string parametered_handle = "";
	for (int i = 0; i < first_positions.size(); ++i) {
		parametered_handle += tokens_from_handle[i].name;
		parametered_handle += handle[first_positions[i] + tokens_from_handle[i].name.size()];
		if (tokens_from_handle[i].numberParameters > 0) {
			// insert parameters
			for (int j = number_inserted_params + 1; 
				j <= number_inserted_params + tokens_from_handle[i].numberParameters; 
				++j) {
			 	parametered_handle += "w";
			 	parametered_handle += boost::lexical_cast<string>(j);
			 	if (j < (number_inserted_params + tokens_from_handle[i].numberParameters) or tokens_from_handle[i].numberArguments > 0){
			 		parametered_handle += ",";			 	
	 			}
			 } 
			// renew variable
			number_inserted_params += tokens_from_handle[i].numberParameters;
		}
		if (i < first_positions.size() - 1) {
			parametered_handle += string(handle.begin() + first_positions[i] + tokens_from_handle[i].name.size() + 1, 
										handle.begin() + first_positions[i + 1]);
		} else {
			parametered_handle += string(handle.begin() + first_positions[i] + tokens_from_handle[i].name.size() + 1, 
										handle.end());
		}		
	}
	return make_pair(parametered_handle, number_inserted_params);
}



BOOST_PYTHON_MODULE(parametrizer) {
	bp::class_<pair<string, int> >("StringIntPair")
    	.def_readwrite("first", &pair<string, int>::first)
    	.def_readwrite("second", &pair<string, int>::second);
    bp::def("parametrizing", parametrizing);
    	
}