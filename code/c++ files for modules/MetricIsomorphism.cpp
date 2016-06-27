/*

Given two handles of superpositions of primitives, it finds the distance between them
The metric used for this purpose is as follows:
	we represent superpositions as directed labeled trees T1 and T2, find the largest common subtree T between them
	then the metric equals to |T1| + |T2| - 2|T|, where |T| is the number of vertices in a tree T

Input:
	handle_char_first				- handle of the first superposition (char array)
	handle_char_second				- handle of the second superposition (char array)
Output

	distance			 			- distance between metric as described above

Author: Kulunchakov Andrei
*/

#include <iostream>
#include <algorithm>
#include "create_data_by_handle.h"
#include "tree_operations.h"

#include <boost/python/def.hpp>
#include <boost/python/module.hpp>

using namespace std;
namespace bp = boost::python;

vector<int> find_representatives_of_equivalence_classes(vector<int>& equivalence_classes) {
  vector<int> representatives(max_in_vector(equivalence_classes) + 1, -1);
  for (int i = 0; i < equivalence_classes.size(); ++i) {
    if (representatives[equivalence_classes[i]] == -1) {
      representatives[equivalence_classes[i]] = i;
    }
  }
  return representatives;
}

int isomorphism_distance(string handle_first, string handle_second) {	
	pair<int,int> counter_tokens = find_number_of_tokens(handle_first);
	int length_first = counter_tokens.first + counter_tokens.second;
	counter_tokens = find_number_of_tokens(handle_second);
	int length_second = counter_tokens.first + counter_tokens.second;
	

	string unite_handle = "plus2_(" + handle_first + "," + handle_second + ")";
	
	pair<map<string, int>, int> tokens_info = read_info_primitives ();
    map<string, int> map_tokens = tokens_info.first;
    
    // convert superposition from string representation to the tree 
	pair<vector<vector<int> >, vector<int> > tree_first = create_incid_matrix_tokens(map_tokens, unite_handle);
	
	vector<vector<int> > model_matr = tree_first.first;
	vector<int> model_encoding = tree_first.second;

	vector<int> equivalence_classes = fill_equivalence_classes (model_matr, model_encoding);
  	vector<int> representatives = find_representatives_of_equivalence_classes(equivalence_classes);
	vector<bool> presence(equivalence_classes.size() + 1);

	for (int i = 1; i <= length_first; ++i) {
		presence[equivalence_classes[i]] = true;		
	}
	
	vector<int> subtrees_sizes(equivalence_classes.size());
	find_subtrees_sizes(model_matr, subtrees_sizes, 0);
	int position_in_second_half_of_tree_array = 1 + length_first;
	int metric = -1;
	for (int i = 1 + length_first; i < equivalence_classes.size(); ++i) {
		if (presence[equivalence_classes[i]]) {
			metric = max(metric, subtrees_sizes[i]);
		}
	}
	return metric;
}


BOOST_PYTHON_MODULE(isomorphism_distance) {
	bp::def("isomorphism_distance", isomorphism_distance);
    	
}