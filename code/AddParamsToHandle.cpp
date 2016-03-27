/*

Add parameters to the handle of a superposition

As some primitive functions have parameters, we should add them into the handle of a superposition containing them
Example:

	initial model:
	exp_(sqrta_(lnl_(frac2_(x1,x2))))

	parametered_model:
	exp_(sqrta_(w[1:2],lnl_(w[3:4],frac2_(x1,x2))))

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
/*
#include <boost/python/def.hpp>
#include <boost/python/module.hpp>
*/
#include <boost/lexical_cast.hpp>

string parametrizing(const char* handle_char) {
	string handle(handle_char);

	// extract tokens presented in the superposition	
	pair<vector<PrimitiveFunction>, vector<int> > info_tokens = extract_tokens_from_handle(handle);
	
	vector<PrimitiveFunction> tokens_from_handle = info_tokens.first; 
	vector<int> first_positions = info_tokens.second;

	// if the superposition is a simple variable, we are nothing to do
	if (tokens_from_handle.size() == 1) {
		return string(handle_char);
	}
	
	// number of parameters inserted in the superposition 'handle' yet
	int number_inserted_params = 0;
	string parametered_handle = "";
	for (int i = 0; i < first_positions.size(); ++i) {
		
		parametered_handle += tokens_from_handle[i].name;
		parametered_handle += handle[first_positions[i] + tokens_from_handle[i].name.size()];
		
		if (tokens_from_handle[i].numberParameters == 0) {
			// check if it is a variable 
			boost::smatch matching_results;
			if (!boost::regex_match(tokens_from_handle[i].name, matching_results, boost::regex("x(\\d+)" ))) {
				parametered_handle += "[],";
			}
		} else {
			// insert parameters
			parametered_handle += "w[";
			parametered_handle += boost::lexical_cast<string>(number_inserted_params + 1);
			parametered_handle += ':';
			parametered_handle += boost::lexical_cast<string>(number_inserted_params + tokens_from_handle[i].numberParameters);
			parametered_handle += "],";			
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
	return parametered_handle;
}

int main() {
	string str = "frac2_(ln_(frac2_(ln_(ln_(x1)),sqrt_(plus2_(x1,ln_(ln_(sqrt_(x1))))))),x2)";
	string answer = parametrizing(str.c_str());
	cout << answer << "\n";
}
/*
BOOST_PYTHON_MODULE(parametrizer) {
    bp::def("parametrizing", parametrizing);
    	
}*/