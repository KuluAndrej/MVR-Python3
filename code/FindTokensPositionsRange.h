/* 

Each primitive function presented in the superposition denotes a subtree with root in this primitive function
We find positions of the first and last characters corresponding to this subtree in the 'handle'
Also we return the sizes of the subtrees (numbers of their vertices)

Input:
	
	handle 			- string name of the superposition

Output:

	positions_range - the first and the last positions of the characters corresponding for the subtree rooted in a token
	sizes_subtrees	- number of tokens presented in the subtree rooted in a token

Author: Kulunchakov Andrei
*/

#include <vector>
#include <string>
#include <utility>
#include <stack>

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