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
#include "RandomModelGenerator.h"
#include <boost/python/def.hpp>
#include <boost/python/module.hpp>
//#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

using namespace std;
namespace bp = boost::python;


//char const* mutation(const char* handle_char, int number_variables) {
char const* crossing(const char* handle_char_first, const char* handle_char_second) {
	
	seed(time(NULL));
	// Retyped inputs
	string handle_first(handle_char_first);
	string handle_second(handle_char_second);
	
	// Retrieve information about subtrees positions and sizes for each of two inputs
	pair<vector<pair<int, int> >, vector<int> > tokens_first_info = find_tokens_positions_range(handle_first);
	pair<vector<pair<int, int> >, vector<int> > tokens_second_info = find_tokens_positions_range(handle_second);

	vector<pair<int, int> > positions_range_first = tokens_first_info.first;
	vector<pair<int, int> > positions_range_second = tokens_second_info.first;

	// extract random subtrees from the superpositions
	int root_random_subtree_first = rand() % positions_range_first.size();
	int root_random_subtree_second = rand() % positions_range_second.size();
	
	// extract random subtrees
	string string_random_subtree_first(handle_first.begin() + positions_range_first[root_random_subtree_first].first, 
									   handle_first.begin() + positions_range_first[root_random_subtree_first].second + 1);

	string string_random_subtree_second(handle_second.begin() + positions_range_second[root_random_subtree_second].first, 
									   handle_second.begin() + positions_range_second[root_random_subtree_second].second + 1);

	// now construct the outputs
	string crossed_handle_first(handle_first.begin(), positions_range_first[root_random_subtree_first].first);
	crossed_handle_first += string_random_subtree_second;
	crossed_handle_first += string(handle_first.begin() + positions_range_first[root_random_subtree_first].second, handle.end());

	string crossed_handle_second(handle_second.begin(), positions_range_second[root_random_subtree_second].first);
	crossed_handle_second += string_random_subtree_first;
	crossed_handle_second += string(handle_second.begin() + positions_range_second[root_random_subtree_second].second, handle.end());

	crossed_handle_first += "#";
	crossed_handle_first += crossed_handle_second;
	return crossed_handle_first.c_str();	
}

int main() {
	string str1 = "expl_(sqrt_(ln_(frac2_(x1,x2))))";
	string str1 = "sqrt_(ln_(frac2_(x1,x2)))";
	cout << crossing(str1.c_str(), str2.c_str()) << "\n";
}

/*
BOOST_PYTHON_MODULE(crosser) {
	//bp::class_<vector<string>>("MyList")
    //    .def(vector_indexing_suite<MyList>() );
    bp::def("crossing", crossing);
    	
}
*/