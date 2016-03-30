/*
Generate a random superposition constructed from primitive functions and variables

Input:
  
  vector< PrimitiveFunction > 	- list of primitives used in the construction of a random superposition
  number_variables 				- maximum number of variables presented in the superposition
  required_size					- number of tokens + variables in the constructed superposition

Output:
  
  superposition 				- generated superposition of the primitive functions

Author: Kulunchakov Andrei
*/

#include <stdlib.h>
#include <time.h>  
#include <set>  
// #include <random>
#include "RetrievePrimitives.h"
#include "boost/lexical_cast.hpp"
#include "../structures/Superposition.h"

#include <boost/python/def.hpp>
#include <boost/python/module.hpp>
#include <boost/lexical_cast.hpp>

namespace bp = boost::python;
using namespace std;  

// return sorted vector of unique values of 'initial_vector'
vector<int> unique_values(vector<int> initial_vector) {
	std::vector<int>::iterator outrunning, lagging ;

	std::set<int> tmpset;

	for (outrunning = initial_vector.begin(), lagging = initial_vector.begin(); outrunning != initial_vector.end(); 
		++outrunning ) {
		if (tmpset.insert(*outrunning).second) {
			*lagging++ = *outrunning;
		}
	}

	initial_vector.erase( lagging , initial_vector.end());
	sort(initial_vector.begin(), initial_vector.end());
	return initial_vector;
}



/*
	Class providing split of a set of primitives on bunches according to their arities
	Private fields:
		primitives_bunches	- set of bunches of primitives; each bunch contains primitives of equal arities
		arities 			- vector of arities of primitives in corresponding bunches
*/

class Primitives_Split_by_Arities {
public:
	Primitives_Split_by_Arities(const vector<PrimitiveFunction>& primitives) {
		// store all arities (repeated entries is allowed) in 'arities'
		arities.resize(primitives.size());
		for (size_t i = 0; i < primitives.size(); ++i) {
			arities[i] = primitives[i].numberArguments;
		}		
		// remove repetitions from 'arities'
		arities = unique_values(arities);

		primitives_bunches.resize(arities.size());
		for (size_t i = 0; i < primitives.size(); ++i) {
			// find the position corresponding to the processed primitive in vector of bunches; store the primitive
			int position_of_primitive;  			
  			position_of_primitive = (std::lower_bound (arities.begin(), arities.end(), primitives[i].numberArguments) - arities.begin());
			primitives_bunches[position_of_primitive].push_back(primitives[i]);
		}
	}
	int maximum_arity() const {
		return arities.back();
	}
	// return primitive function of arity at most 'maximum_possible_arity'
	PrimitiveFunction random_primitive_bounded_arity(int maximum_possible_arity) const{
		// we form a subvector of 'arities', which will produce random allowable arity of the future primitive
		int right_pos_allowable_arities;
		if (maximum_possible_arity < maximum_arity()) {
			right_pos_allowable_arities = 
						(std::lower_bound (arities.begin(), arities.end(), maximum_possible_arity) - arities.begin());
		} else {
			right_pos_allowable_arities = arities.size() - 1;
		}
		int index_of_random_arity = rand() % (right_pos_allowable_arities + 1);
		// search for a random primitive from primitives_bunches[index_of_random_arity]
		int index_of_random_primitive = rand() % primitives_bunches[index_of_random_arity].size();
		return primitives_bunches[index_of_random_arity][index_of_random_primitive];
	}
private:
	// 'primitives_bunches' is a list of primitives split according to their arities
	vector<vector<PrimitiveFunction> >	primitives_bunches;
	// vector storing arities of children of the root	
	vector<int>	arities;
};

/*
	Recursive algorithm of generation of a superposition.
	The probabilities of a primitive function appearance are equal

*/
string recursive_model_generator(const Primitives_Split_by_Arities& split_primitives, int number_variables, 
								int required_size) {
	string handle;

	// if the 'required_size' == 1, we have to simply create a random variable
	if (required_size == 1) {
		return "X[" + boost::lexical_cast<string>(rand() % number_variables) + string("]");
	}

	// generate the random number denoting the arity of the root primitive of the current processed subtree
	// note that one place in the superposition have already reserved for this primitive
	PrimitiveFunction root_primitive = split_primitives.random_primitive_bounded_arity(required_size - 1);
	// create random tuple of sizes of the subtrees rooted in children of 'root_primitive'
	int size_of_random_tuple = root_primitive.numberArguments;
	// reserve 'root_primitive.numberArguments + 1' positions from 'required_size'
	// distribute the remaining positions between the children
	vector<int> random_tuple(size_of_random_tuple, 1);
	int number_of_free_positions = required_size - 1 - root_primitive.numberArguments;
	for (int i = 0; i < size_of_random_tuple; ++i) {
		random_tuple[i] += rand() % (number_of_free_positions + 1); 
		number_of_free_positions -= (random_tuple[i] - 1);
	}
	random_shuffle (random_tuple.begin(), random_tuple.end());

	// recursively construct the handle of the current subtree-superposition
	handle = root_primitive.name;
	// cout << "handle = root_primitive.name; " << root_primitive.name << "\n";
	handle += '(';
	for (int i = 0; i < size_of_random_tuple; ++i) {
		handle += recursive_model_generator(split_primitives, number_variables, random_tuple[i]);
		handle += (i == size_of_random_tuple - 1) ? "" : ",";
	}	
	handle += ')';

	return handle;
}



string random_model_generation(int number_variables, int required_size) {
	
	vector<PrimitiveFunction> primitives;
	primitives = retriever();

	Primitives_Split_by_Arities split_primitives(primitives);
	
	return recursive_model_generator(split_primitives, number_variables, required_size);
}


BOOST_PYTHON_MODULE(random_model_generator) {
    bp::def("random_model_generation", random_model_generation);
    	
}