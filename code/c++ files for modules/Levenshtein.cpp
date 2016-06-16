/*
Find Levenshtein distance between two strings

Input:
  
  	s1		- the first string
  	s2		- the second string

Output:
  
  	distance

Taken from 'https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#C.2B.2B'
*/

#include <stdlib.h>
#include <string>
#include <vector>
// #include <random>

#include <boost/python/def.hpp>
#include <boost/python/module.hpp>


namespace bp = boost::python;
using namespace std;  

unsigned int levenshtein_distance(const string s1, const string s2) 
{
	const size_t len1 = s1.size(), len2 = s2.size();
	vector<unsigned int> col(len2+1), prevCol(len2+1);
	
	for (unsigned int i = 0; i < prevCol.size(); i++)
		prevCol[i] = i;
	for (unsigned int i = 0; i < len1; i++) {
		col[0] = i+1;
		for (unsigned int j = 0; j < len2; j++)
                        // note that min({arg1, arg2, arg3}) works only in C++11,
                        // for C++98 use min(min(arg1, arg2), arg3)
			col[j+1] = min({ prevCol[1 + j] + 1, col[j] + 1, prevCol[j] + (s1[i]==s2[j] ? 0 : 1) });
		col.swap(prevCol);
	}
	return prevCol[len2];
}


BOOST_PYTHON_MODULE(levenshtein) {
    bp::def("levenshtein_distance", levenshtein_distance);
    	
}