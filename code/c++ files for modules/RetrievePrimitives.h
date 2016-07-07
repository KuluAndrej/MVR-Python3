/*
Retrieve the set of primitive functions
Each function contain the the following information:

  token's name          - string
  number of parameters  - int
  number of arguments   - int

If 'Primitives.py' is newer than 'Primitives.txt', it parses 'Primitives.py' and store extracted primitives in 'Primitives.txt'
The format for the storage is as follows

#Name #NumPar #NumArg
name1 numPar1 numArg1
...   ...     ...
nameN numParN numArgN
...   ...     ...


NOTE: Each type of filesystem differs slightly in the details and resolution of how times are recorded. 
The resolution is as low as one hour on some filesystems. It could be a problem with checking what file is newer.

Input:
  
  empty

Output:
  
  vector< PrimitiveFunction > 

Author: Kulunchakov Andrei
*/

#include <cctype>
#include <ctime> 
#include <time.h>  
#include <fcntl.h>
#include <errno.h>

#include <stdlib.h>
#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <stdio.h>
#include "../structures/PrimitiveFunction.h"

#include <boost/filesystem.hpp>
#include <boost/regex.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/algorithm/string/predicate.hpp>


using namespace std;  

// Search for a string of the following format
// 		name.NumParam = number
// Extract the 'number' from this string

int extract_parameter (ifstream& input_file, const string& name) {
	boost::smatch matching_results;
	string line;
	
	getline(input_file , line);
	while ( !boost::regex_match(line, matching_results, boost::regex("[\t ]+[\\w_]+.[\\w]+[ ]+=[ ]+(\\d+)[ ]*" ) ) ) {		
    	getline(input_file , line);
    }
    // extract the 'number' from the found occurence
	boost::regex_search(line,  matching_results, boost::regex("=[ ]+[0-9]+") ); 
	string pattern = matching_results[0];
	boost::regex_search(pattern,  matching_results, boost::regex("[0-9]+") ); 
	
	return boost::lexical_cast<int>(matching_results[matching_results.size() - 1]);
}


// Search for a string of the following format
// 		name.InitParams = [numbers]
// Extract 'numbers' from this string.
// Note that these parameters will be treated in Py-files, so we read them only for
// storing in file, providing the future work of these Py-files
string extract_vector_init_params (ifstream& input_file, const string& name) {
	boost::smatch matching_results;
	string line;
	
	getline(input_file , line);
	while ( !boost::regex_match(line, matching_results, boost::regex("[\t ]+[\\w_]+.[\\w]+[ ]+=[ ]*\\[[-\\d. ,]*\\][ ]*" ) ) ) {		
    	getline(input_file , line);
    }
    boost::regex_search(line,  matching_results, boost::regex("\\[[-\\d. ,]*\\]") ); 
	string output_string = matching_results[0];

	size_t found = output_string.find(" ");
	if (found != string::npos) {
		throw name + string(" token contains excessive blank spaces in the InitParams field\n");
	}
	return matching_results[0];
}

// Search for a string of the following format
// 		name.BoundsParams = ([numbers_1],[numbers_2])
// Extract the tuple ([numbers_1],[numbers_2]) from this string.
// Note that these parameters will be treated in Py-files, so we read them only for
// storing in file, providing the future work of these Py-files
string extract_vector_bounds_params (ifstream& input_file, const string& name) {
	boost::smatch matching_results;
	string line;
	
	getline(input_file , line);
	while ( !boost::regex_match(line, matching_results, boost::regex("[\t ]+[\\w_]+.[\\w]+[ ]+=[ ]*\\(\\[[-\\d\\w. ,]*\\][ ]*,[ ]*\\[[-\\d\\w. ,]*\\]\\)[ ]*" ) ) ) {		
    	getline(input_file , line);
    }
    boost::regex_search(line,  matching_results, boost::regex("\\(\\[[-\\d\\w. ,]*\\][ ]*,[ ]*\\[[-\\d\\w. ,]*\\]\\)") ); 
    string output_string = matching_results[0];

	size_t found = output_string.find(" ");
	if (found != string::npos) {
		throw name + string(" token contains excessive blank spaces in the BoundsParams field\n");
	}
	return matching_results[0];
}

// Check is the version of 'Primitives.py' is newer than 'Primitives.txt'

bool checker_version_of_py_file(const string& FILE_PRIMITIVES) {	
	boost::filesystem::path current_path = boost::filesystem::current_path();
	boost::filesystem::path current_path_copy = current_path;
	//boost::filesystem::path parent_path = current_path.parent_path();
	time_t time_py =  boost::filesystem::last_write_time(current_path.append(FILE_PRIMITIVES + string(".py")));
	time_t time_txt = boost::filesystem::last_write_time(current_path_copy.append(FILE_PRIMITIVES + string(".txt")));
	/*
	time_t time_py =  boost::filesystem::last_write_time(FILE_PRIMITIVES + string(".py"));
	time_t time_txt = boost::filesystem::last_write_time(FILE_PRIMITIVES + string(".txt"));
	*/
	return time_py > time_txt;	
}


// Load primitives retrived from .py file to .txt file
void loader_primitives(string FILE_PRIMITIVES_WITHOUT_EXTENSION, const vector<PrimitiveFunction>& primitives) {
	cout << "Entered loader_primitives\n";
	// construct the same filename, but with '.txt' extension
	string FILE_PRIMITIVES_TXT = FILE_PRIMITIVES_WITHOUT_EXTENSION + string(".txt");
	string FILE_PRIMITIVES_INFO_FOR_OPTIMIZATION_TXT = FILE_PRIMITIVES_WITHOUT_EXTENSION + string("InfoForOptimization.txt");
	// load primitive in txt-file
	ofstream file_primitives_txt;
	ofstream file_primitives_info_for_optimization_txt;
  	
  	file_primitives_txt.open ( FILE_PRIMITIVES_TXT.c_str() );
  	file_primitives_info_for_optimization_txt.open(FILE_PRIMITIVES_INFO_FOR_OPTIMIZATION_TXT.c_str());

	file_primitives_txt << "#Name #NumPar #NumArg\n";
	file_primitives_info_for_optimization_txt << "#Name #InitParams #BoundsParams\n";

	for (size_t i = 0; i < primitives.size(); ++i) {
		file_primitives_txt << primitives[i].name << " " << primitives[i].numberParameters << " " 
												  << primitives[i].numberArguments << "\n";
	}
	
	for (size_t i = 0; i < primitives.size(); ++i) {
		file_primitives_info_for_optimization_txt << primitives[i].name << " " << primitives[i].initParams << " " 
							<< primitives[i].boundsParams << "\n";
	}

	file_primitives_txt.close();  	
	file_primitives_info_for_optimization_txt.close();  	
	cout << "Exited loader_primitives\n";
}

// Parse 'Primitives.py' and store extracted primitives in the 'Primitives.txt'
vector< PrimitiveFunction > parse_py_file_with_primitives(const string& FILE_PRIMITIVES_WITHOUT_EXTENSION) {
	
	string FILE_PRIMITIVES = FILE_PRIMITIVES_WITHOUT_EXTENSION + string(".py");
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
		        // cout << primitive.name << '\n';
				primitive.numberParameters = extract_parameter( file_primitives, primitive.name);
				primitive.numberArguments  = extract_parameter( file_primitives, primitive.name);
				primitive.initParams 	   = extract_vector_init_params (file_primitives, primitive.name);
				primitive.boundsParams 	   = extract_vector_bounds_params(file_primitives, primitive.name);

				primitives.push_back(primitive);

			} 
		}
		loader_primitives(FILE_PRIMITIVES_WITHOUT_EXTENSION, primitives);
		file_primitives.close();  
		return primitives;
	} else {
		string error_message = "File '" + FILE_PRIMITIVES + "' does'not exist\n";
		throw error_message;
	}		

}




// Retrieve the list of primitives from one of the files: 'Primitives.py' or 'Primitives.txt'
vector< PrimitiveFunction > retriever() {
	string FILE_PRIMITIVES_WITHOUT_EXTENSION = "code/Primitives";
	//string FILE_PRIMITIVES_WITHOUT_EXTENSION = "Primitives";
	if (checker_version_of_py_file(FILE_PRIMITIVES_WITHOUT_EXTENSION)) {
		// if the .py file is newer than the .txt file, we parse it and return the extracted primitives
		return parse_py_file_with_primitives(FILE_PRIMITIVES_WITHOUT_EXTENSION);
	} else {
		// retrieve primitives from the table in .txt file
		string FILE_PRIMITIVES = FILE_PRIMITIVES_WITHOUT_EXTENSION + string(".txt");
		ifstream file_primitives;
  		file_primitives.open (FILE_PRIMITIVES.c_str());
  		
  		vector< PrimitiveFunction > primitives; 
  		PrimitiveFunction primitive;
  		// Skip the header of the table in .txt file
  		getline(file_primitives, primitive.name);
  		// retrieve primitives
  		
  		while (file_primitives >> primitive.name >> primitive.numberParameters >> primitive.numberArguments) {
  			primitives.push_back(primitive);
  		}
  		file_primitives.close();
  		return primitives;
	}
}