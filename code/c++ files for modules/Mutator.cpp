/*

Perform a mutation operation
It takes one subtree of a superposition and replace it with another random one

Input:
	handle 				- handle of a superposition to be mutated
	number_variables	- maximum number of unique variables in a superposition
Output
	mutated_handle		- handle of the mutated superposition

Author: Kulunchakov Andrei
*/

#include <iostream>
#include <utility>
#include <stack>
#include "RandomModelGenerator.h"
#include "FindTokensPositionsRange.h"
#include <boost/python/def.hpp>
#include <boost/python/module.hpp>

using namespace std;
namespace bp = boost::python;




//char const* mutation(const char* handle_char, int number_variables) {
const string mutation(const string handle_char, int number_variables) {
	
	//srand(time(NULL));
	string handle = handle_char;
	
	pair<vector<pair<int, int> >, vector<int> > tokens_info = find_tokens_positions_range(handle);
	
	vector<pair<int, int> > positions_range = tokens_info.first;
	vector<int> sizes_subtrees = tokens_info.second;
	
	// extract random subtree from the superposition and replace it with a random one
	// the root of a random subtree is
	int root_random_subtree = rand() % positions_range.size();
	
	
	// choose the size of a replacement tree
	// avoid parameters producing an empty superposition
	// restrict the structural complexity of a replacement tree by the double size of the replaced tree
	int required_size_replacement =  1 + rand() % (2 * sizes_subtrees[root_random_subtree] - 1);

	string mutated_handle(handle.begin(), handle.begin() + positions_range[root_random_subtree].first);	
	mutated_handle += random_model_generation(number_variables, required_size_replacement);
	mutated_handle += string(handle.begin() + positions_range[root_random_subtree].second + 1, handle.end());
	
	return mutated_handle;	
}


BOOST_PYTHON_MODULE(mutator) {
    bp::def("mutation", mutation);
}