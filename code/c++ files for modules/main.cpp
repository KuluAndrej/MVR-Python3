/*

Perform a crossover operation
It takes two superpositions, in each of them chooses a random subtree, and swaps them.
It produces two new superpositions

Input:
	handle_char_first				- handle of the first superposition (char array)
	handle_char_second				- handle of the second superposition (char array)
Output

	string 'crossed_handle_first#crossed_handle_second', where 

	crossed_handle_first 			- handle of the first superposition produced by crossing (char array)
	crossed_handle_second 			- handle of the second superposition produced by crossing (char array)

Author: Kulunchakov Andrei
*/

#include <iostream>
#include <stack>
#include <utility>
#include <fstream> 
#include <stdlib.h>
#include "FindTokensPositionsRange.h"

using namespace std;


//char const* mutation(const char* handle_char, int number_variables) {
pair<string, string> crossing(const char* handle_char_first, const char* handle_char_second) {
	
	// Retyped inputs
	string handle_first(handle_char_first);
	string handle_second(handle_char_second);
	
	// Retrieve information about subtrees positions and sizes for each of two inputs
	pair<vector<pair<int, int> >, vector<int> > tokens_first_info = find_tokens_positions_range(handle_first);
	pair<vector<pair<int, int> >, vector<int> > tokens_second_info = find_tokens_positions_range(handle_second);

	vector<pair<int, int> > positions_range_first = tokens_first_info.first;
	vector<pair<int, int> > positions_range_second = tokens_second_info.first;

	// extract random subtrees from the superpositions
	// int root_random_subtree_first = rand() % positions_range_first.size();

	// int root_random_subtree_second = rand() % positions_range_second.size();
	int root_random_subtree_first = 2;
	int root_random_subtree_second = 1;
	
	// extract random subtrees
	string string_random_subtree_first(handle_first.begin() + positions_range_first[root_random_subtree_first].first, 
									   handle_first.begin() + positions_range_first[root_random_subtree_first].second + 1);

	string string_random_subtree_second(handle_second.begin() + positions_range_second[root_random_subtree_second].first, 
									   handle_second.begin() + positions_range_second[root_random_subtree_second].second + 1);

	// now construct the outputs
	string crossed_handle_first(handle_first.begin(), handle_first.begin() + positions_range_first[root_random_subtree_first].first);
	crossed_handle_first += string_random_subtree_second;
	crossed_handle_first += string(handle_first.begin() + positions_range_first[root_random_subtree_first].second + 1, handle_first.end());

	string crossed_handle_second(handle_second.begin(), handle_second.begin() + positions_range_second[root_random_subtree_second].first);
	crossed_handle_second += string_random_subtree_first;
	crossed_handle_second += string(handle_second.begin() + positions_range_second[root_random_subtree_second].second + 1, handle_second.end());

	return make_pair(crossed_handle_first, crossed_handle_second);
}

int main() {
	srand(time(NULL));
	ofstream ofs("gang.txt", std::ofstream::out);

	string str1 = "frac2_(X[1],X[1])";
	string str2 = "frac2_(sqrt_(X[0]),X[0])";
	for (int i = 0; i < 1000; ++i){
		pair<string, string> info = crossing(str1.c_str(), str2.c_str());
		ofs << info.first << "\n" << info.second << "\n\n";
	}
	ofs.close();
	return 0;
}