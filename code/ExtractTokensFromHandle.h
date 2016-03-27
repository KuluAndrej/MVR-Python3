/* 

Returns the list of tokens presented in a superposition.
The order of tokens in list corresponds to their order in the string 'handle'
Example:
	sqrt_(ln_(frac2_(x1,x2))) -> ['sqrt_', 'ln_', 'frac2_', 'x1', 'x2']

Input:
	
	handle 			- string name of the superposition

Output:

	tokens 			- the list of tokens presented in the superposition

Author: Kulunchakov Andrei
*/


#include <utility>
#include <stack>
#include <map>
#include <vector>
#include <string>

using namespace std;

vector<Primitives> extract_tokens_from_handle(const string& handle) {

	// create a map from primitives names to corresponding objects


	vector<int> left_positions, right_positions;
	vector<int> sizes_subtrees;
	stack<int> stack_for_tokens;
	left_positions.push_back(0);
	right_positions.push_back(handle.size() - 1);
	stack_for_tokens.push(0);		
	// the following indicator is set to true if we traverse a token now
	bool is_smth_being_processed = true;
	for (size_t i = 0; i < handle.size(); ++i) {
		if (handle[i] == '(') {				
			is_smth_being_processed = false; 
			continue;
		}
		if (is_smth_being_processed && handle[i] == ',') {				
			right_positions[stack_for_tokens.top()] = i - 1;
			// +1 to count the root of a subtree
			sizes_subtrees[stack_for_tokens.top()] = right_positions.size() - stack_for_tokens.top() + 1;
			stack_for_tokens.pop();
			// no matter of what value does 'is_smth_being_processed' have, now it becomes 'false'
			is_smth_being_processed = false; 
			continue; 
		}

		if (handle[i] == ')') {				
			right_positions[stack_for_tokens.top()] = i;
			// +1 to count the root of a subtree
			sizes_subtrees[stack_for_tokens.top()] = right_positions.size() - stack_for_tokens.top() + 1;
			// if we've processed a variable, then it does not include ')' symbol
			right_positions[stack_for_tokens.top()]--;
			stack_for_tokens.pop();
			// no matter of what value does 'is_smth_being_processed' have, now it becomes 'false'
			is_smth_being_processed = false; 
			continue;
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
