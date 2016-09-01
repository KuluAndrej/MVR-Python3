/*

Add parameters to the handle of a superposition

As some primitive functions have parameters, we should add them into the handle of a superposition containing them
Example:

	initial model:
	exp_(sqrta_(lnl_(frac2_(x1,x2))))

	parametered_model:
	exp_(sqrta_(w0, w1, lnl_(w2, w3, frac2_(x1,x2))))

Input:

	handle 				- string name of an unparametered superposition

Output
	
	parametered_handle 	- string name of the parametered version of the 'handle'


Author: Kulunchakov Andrei
*/

#include <string>
#include <vector>
#include "create_data_by_handle.h"

using namespace std;



int main() {
	string s = "hvs_(X[0])";
	vector<string> v = create_tokens_of_model(s);
	cout << "term\n";
	cout << v[0] << " " << v[1] << '\n';
}