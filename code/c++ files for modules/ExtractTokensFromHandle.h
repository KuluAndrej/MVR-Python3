/* 

Returns the list of tokens presented in a superposition and the positions of their first symbols.
The order of tokens in list corresponds to their order in the string 'handle'
Example:
	sqrt_(ln_(frac2_(x1,x2))) -> ['sqrt_', 'ln_', 'frac2_', 'x1', 'x2']


If the 'handle' corresponds to an invalid function, it raises an error

Input:
	
	handle 			- string name of the superposition

Output:

	tokens 			- the list of tokens presented in the superposition (vector<PrimitiveFunction>)
	first_positions	- the list of first positions of tokens

Author: Kulunchakov Andrei
*/


#include <utility>
#include <stack>
#include <map>
#include <stdio.h>
#include <vector>
#include <string>
#include "RetrievePrimitives.h"
#include <boost/regex.hpp>

using namespace std;

pair<vector<PrimitiveFunction>, vector<int> > extract_tokens_from_handle(const string& handle) {
	
	// create a map from primitives names to corresponding objects
	map<string, PrimitiveFunction> mapNamePrimitive;
	
	// If handle is a simple variable, return answer immediately
	boost::smatch matching_results;
	if (boost::regex_match(handle, matching_results, boost::regex("X\\[(\\d+)\\]"))) {
		vector<PrimitiveFunction> tokens_from_handle;
		PrimitiveFunction variable;
		variable.name = handle;	
		variable.numberArguments = 0;
		variable.numberParameters = 0;
		tokens_from_handle.push_back(variable);
		return make_pair(tokens_from_handle, vector<int>(1,0));
	}
	
	// retrieve valid primitives from 'Primitives.py' file
	vector<PrimitiveFunction> primitives;
	primitives = retriever();	

	// load them into the map

	for (int i = 0; i < primitives.size(); ++i) {
		mapNamePrimitive.insert(make_pair(primitives[i].name, primitives[i]));
	}
	
	// now traverse the 'handle'; extract tokens and their positions
	vector<PrimitiveFunction> tokens_from_handle;
	vector<int> first_positions;
	// position of the first character of a processed token
	int fetched_position;
	bool is_smth_being_processed = false;
	for (size_t i = 0; i < handle.size(); ++i) {
		if (handle[i] == '(') {			
			// the case of a primitive function appearance
			is_smth_being_processed = false; 
			string name_of_token(handle.begin() + fetched_position, handle.begin() + i);
			// check if a token with the 'name_of_token' is presented in the map
			if (mapNamePrimitive.find(name_of_token) != mapNamePrimitive.end()) {
				tokens_from_handle.push_back(mapNamePrimitive[name_of_token]);	
			} else {
				string error_message = "Token '" + name_of_token + "' is not presented in Primitives.py. \nOr presented in a wrong format\n";
				perror(error_message.c_str());
				throw error_message;
			}			
			continue;
		}

		if (is_smth_being_processed && (handle[i] == ',' || handle[i] == ')')) {
			is_smth_being_processed = false; 			
			// the case of a variable appearance
			PrimitiveFunction variable;
			variable.name = string(handle.begin() + fetched_position, handle.begin() + i);	
			// check if it is a valid variable
			
			if (boost::regex_match(variable.name, matching_results, boost::regex("X\\[(\\d+)\\]"))) {
				variable.numberArguments = 0;
				variable.numberParameters = 0;
				tokens_from_handle.push_back(variable);
			} else {
				string error_message = "Token '" + variable.name + "' is not presented in Primitives.py. \nOr presented in a wrong format\n";
				perror(error_message.c_str());
				throw error_message;
			}					
			continue; 
		}

		if (!is_smth_being_processed) {
			// if we currently do not process any token, we are ready to process a new one			
			if (isalpha(handle[i])) {
				is_smth_being_processed = true;						
				fetched_position = i;		
				first_positions.push_back(i);		
			}
		} 
	}

	return make_pair(tokens_from_handle, first_positions);
}
