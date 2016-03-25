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
#include "RetrievePrimitives.h"
#include "structures/Superposition.h"


using namespace std;  

/*
	Recursive algorithm of generation of a superposition.
	The probabilities of a primitive function appearance are equal

	'primitives_splitted' is a list of primitives split according to their arities
*/
string recursive_model_generator(vector<vector<PrimitiveFunction> > primitives_splitted, int number_variables, int required_size) {
	string handle;
	// generate the random number denoting the arity of the root primitive of the current processed subtree
	// note that one place in the superposition have already reserved for this primitive
	int random_arity = rand() % (min(primitives_splitted.size(), required_size) - 1);
	// extract a primitive of arity 'random_arity' from the corresponding bunch
	int random_primitive_index = rand() % (primitives_splitted[random_arity].size);
	handle = primitives_splitted[random_arity][random_primitive_index].name;
	
	// vector storing arities of children of the root
	vector<int> children_arities(random_arity);
	for (int i = 0; i < random_arity; ++i) {
		int random_arity_child = rand() % (min(primitives_splitted.size(), required_size - 1));;
	}

	shuffle (foo.begin(), foo.end(), std::default_random_engine(seed));
	return handle;
}

Superposition random_model_generator(vector< PrimitiveFunction > primitives, int number_variables, int required_size) {
	Superposition superposition;
	srand (time(NULL));
	// split the list of primitives on bunches according to the value of 'numberArguments' field
	// a 'PrimitiveFunction' lies in 'primitives_splitted[PrimitiveFunction.numberArguments]'
	vector<vector<PrimitiveFunction> > primitives_splitted;
	for (int i = 0; i < primitives.size(); ++i) {
		// check if the capacity of the list of bunches is appropriate for loading our primitive function
		if (primitives_splitted.size() <= primitives[i].numberArguments) {
			primitives_splitted.resize(primitives[i].numberArguments + 1);		
		}
		primitives_splitted[primitives[i].numberArguments].push_back(primitives[i]);
	}
	return superposition;
}

int main() {

	vector<PrimitiveFunction> primitives;
	primitives = retrieve_primitives();
	return 0;
}