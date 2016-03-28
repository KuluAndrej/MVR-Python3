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
#include <boost/python/def.hpp>
#include <boost/python/module.hpp>

using namespace std;
namespace bp = boost::python;

// Each primitive function presented in the superposition denotes a subtree with root in this primitive function
// We find positions of the first and last characters corresponding to this subtree in the 'handle'
// Also we return the sizes of the subtrees (numbers of their vertices)

pair<vector<pair<int, int> >, vector<int> > find_tokens_positions_range(const string& handle) {
	vector<int> left_positions, right_positions;
	vector<int> sizes_subtrees;
	stack<int> stack_for_tokens;
	left_positions.push_back(0);
	// temporary value, set for convenience
	right_positions.push_back(0);
	stack_for_tokens.push(0);		
	// the following indicator is set to true if we traverse a token now
	bool is_smth_being_processed = true;
	for (size_t i = 0; i < handle.size(); ++i) {
		if (handle[i] == '(') {				
			is_smth_being_processed = false; 
		}

		if (handle[i] == ')') {				
			right_positions[stack_for_tokens.top()] = i;
			// +1 to count the root of a subtree
			sizes_subtrees[stack_for_tokens.top()] = right_positions.size() - stack_for_tokens.top() + 1;
			stack_for_tokens.pop();
			// no matter of what value does 'is_smth_being_processed' have, now it becomes 'false'
			is_smth_being_processed = false; 
		}

		if (!is_smth_being_processed) {
			// if we currently do not process any primitive, we are ready to store one more in stack			
			if (isalpha(handle[i])) {
				is_smth_being_processed = true;						
				left_positions.push_back(i);
				// 2 temporal values just to increase a capacity
				right_positions.push_back(i);
				sizes_subtrees.push_back(i);
				stack_for_tokens.push(left_positions.size() - 1);					
			}
		} 
	}
	vector<pair<int, int> > positions_range(left_positions.size());
	for (size_t i = 0; i < positions_range.size(); ++i) {
		positions_range[i] = make_pair(left_positions[i], right_positions[i]);
	}
	return make_pair(positions_range, sizes_subtrees);
}



//char const* mutation(const char* handle_char, int number_variables) {
char const* mutation(const char* handle_char, int number_variables) {
	
	
	string handle(handle_char);
	
	pair<vector<pair<int, int> >, vector<int> > tokens_info = find_tokens_positions_range(handle);
	vector<pair<int, int> > positions_range = tokens_info.first;
	vector<int> sizes_subtrees = tokens_info.second;
	// extract random subtree from the superposition and replace it with a random one
	// the root of a random subtree is
	int root_random_subtree = rand() % positions_range.size();
	string mutated_handle(handle.begin(), handle.begin() + positions_range[root_random_subtree].first);
	// choose the size of a replacement tree
	int required_size_replacement = rand() % (2 * sizes_subtrees[root_random_subtree]);
	mutated_handle += random_model_generator(number_variables, required_size_replacement);
	mutated_handle += string(handle.begin() + positions_range[root_random_subtree].second, handle.end());
	
	return mutated_handle.c_str();	
}


BOOST_PYTHON_MODULE(mutator) {
    bp::def("mutation", mutation);
}