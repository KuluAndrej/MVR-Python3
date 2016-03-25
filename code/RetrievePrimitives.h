/*
Parse the file 'Primitives.py' to retrieve the following information about tokens:

  token's name          - string
  number of parameters  - int
  number of arguments   - int

Input:
  
  empty

Output:
  
  vector< PrimitiveFunction > 

Author: Kulunchakov Andrei
*/

#include <cctype>
#include <fcntl.h>
#include <errno.h>

#include <stdlib.h>
#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <stdio.h>
#include "structures/PrimitiveFunction.h"

#include <boost/filesystem.hpp>
#include <boost/regex.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/algorithm/string/predicate.hpp>


using namespace std;  

// Search for the 'number' in a string of the following format
// 		name.NumParam = number
//
// Input:
// 	'name'
// Output
//  'number'

int extract_parameter (ifstream& input_file, const string& name) {
	boost::smatch matching_results;
	string line;
	
	getline(input_file , line);
	while ( !boost::regex_match(line, matching_results, boost::regex("[\t ]+[\\w_]+.[\\w]+[ ]+=[ ]+(\\d+)[ ]*" ) ) ) {		
    	getline(input_file , line);
    }
    // extract the 'number' from the found occurence
	boost::regex_search(line,  matching_results, boost::regex("[0-9]+") ); 
	
	return boost::lexical_cast<int>(matching_results[0]);
}


vector< PrimitiveFunction > retrieve_primitives() {
	
	string FILE_PRIMITIVES = "Primitives.py";
	
	// check if the file with primitives is presented in the current directory
	bool if_exists = boost::filesystem::exists( FILE_PRIMITIVES );
	if (if_exists) {
		// now process the file and extract the information about primitive functions
		ifstream file_primitives;
  		file_primitives.open ( FILE_PRIMITIVES.c_str() );
  		
  		// read the file line by line and check if the string is started with 'def'
  		// further information is retrieved as stated in the following template:
  		// 		def name( ... )
  		//			name.NumParam = numberParameters
        //			name.NumVars  = numberArguments
		// 			
		//			return ...

  		vector< PrimitiveFunction > primitives; 
  		string line;
  		while ( getline(file_primitives , line) ) {
  			if (boost::starts_with(line, "def ")) {						    	
  				PrimitiveFunction primitive;
	    		boost::smatch matching_results;
				
				boost::regex_search(line,  matching_results, boost::regex("[ ]+([\\w_]+)") ); 
				primitive.name = matching_results[1];
				
		        // now extract 'numberParameters' and 'numberArguments'
		        
				primitive.numberParameters = extract_parameter( file_primitives, primitive.name);
				primitive.numberArguments = extract_parameter( file_primitives, primitive.name);
				
				primitives.push_back(primitive);
			} 
		}
  		for (int i = 0; i < primitives.size(); ++i)	{
  			cout << primitives[i].name << "\n";
  		}		
		return primitives;
	} else {
		string error_message = "File '" + FILE_PRIMITIVES + "' does'not exist\n";
		throw error_message;
	}
}
