/*

In this file we implement the functionality for reconstructuring of superpositions handles.
This means that we represent each superposition as a tree and for each node of it having primitive corresponding to commutative 
function, we order the child subtrees according to the root labels.

Example:

plus2_(lnl(x0), atana_(linear_(x0)))

Here we have a commutative function plus2_ and two child subtrees: 1) lnl(x0) 2) atana_(linear_(x0)). We rearrange them in 
the alphabetic order:

plus2_(atana_(linear_(x0)), lnl(x0))

Author: Kulunchakov Andrei
*/

#include <math.h>
#include <stdlib.h>
#include <vector>
#include <string>
#include <utility>
#include <stdio.h>
#include <ctype.h>
#include <map>
#include "create_data_by_handle.h"

using namespace std;

/*
#include <boost/python/def.hpp>
#include <boost/python/module.hpp>

namespace bp = boost::python;
*/

using namespace std;  
const int UNFILLED_INT = -1;


void exchange_subtrees(string& handle, const vector<int>& positions_of_tokens, int root) {
  int counter = -1;
  int first_arg = positions_of_tokens[root + 1];
  int second_arg = UNFILLED_INT;
  int end_of_second_arg = UNFILLED_INT;  
  for (int i = positions_of_tokens[root]; i < handle.size(); ++i) {
    if (handle[i] == '(') counter++;
    if (handle[i] == ')') counter--;  
    if ((counter == 0) && (handle[i] == ',')) {
      second_arg = i;      
    }
    if (second_arg != UNFILLED_INT && counter == -1) {
      end_of_second_arg = i;
      break;
    }
  }  
  
  string first_submodel(second_arg - first_arg, '_');
  copy(handle.begin() + first_arg, handle.begin() + second_arg, first_submodel.begin());
  string second_submodel(end_of_second_arg - 1 - second_arg, '_');
  copy(handle.begin() + second_arg + 1, handle.begin() + end_of_second_arg, second_submodel.begin());
  handle = eraser(handle, first_arg, first_submodel.size() + 1 + second_submodel.size());
  
  handle.insert(first_arg, second_submodel + "," + first_submodel);
  
  return;
}


void Solver(string& handle, const vector<int> commutativeness){
  pair<map<string, int>, int> tokens_info = read_info_primitives ();
  map<string, int> map_tokens = tokens_info.first;

  pair<vector<vector<int> >, vector<int> > model_data = create_incid_matrix_tokens(map_tokens, handle);
  vector<vector<int> > matr = model_data.first;
  vector<int> encoding = model_data.second;
  int dim = matr.size();

  vector<int> positions_of_tokens = find_positions_of_tokens(handle);
  
  for (int i = dim - 1; i >= 0; --i) {
    if (commutativeness[i] == 1) {
      bool is_wrong_order = (encoding[matr[i][0]] > encoding[matr[i][1]]);
      if (is_wrong_order) {
        exchange_subtrees(handle, positions_of_tokens, i);
      }      
    }
  }

}


string model_reconstruct(string modelhandle) {
  
  vector<int> commutativeness;
  
  pair<map<string, int>, vector<int> > tokens_data = read_info_commutativenes();
  vector<int> vectorOfCommutativeness = tokens_data.second;

  pair<vector<vector<int> >, vector<int> > model_data = create_incid_matrix_tokens(tokens_data.first,  modelhandle);
  commutativeness.resize(model_data.first.size());
  vector<int> encoding = model_data.second;
  for (int i = 0; i < encoding.size(); ++i) {
    if (vectorOfCommutativeness[encoding[i]]) {
      commutativeness[i] = vectorOfCommutativeness[encoding[i]];
    }
  }
  
  Solver(modelhandle, commutativeness);
  return modelhandle;
}

/*
BOOST_PYTHON_MODULE(model_reconstructer) {
	bp::def("model_reconstruct", model_reconstruct);
    	
}*/

int main(){
  //string s = "plus2_(minus2_(x0,x0),hyperbola_(linear_(parabola_(x0))))";
  //string s = "inv_(hyperbola_(hyperbola_(linear_(parabola_(x0))))))";
  string s = "bump_(normal_(times2_(frac2_(plus_(x0),plus_(plus2_(sqrtl_(x0),frac2_(plus_(x0),plus_(plus2_(expl_(bump_(x0)),x0)))))),x0)))";
  cout << s << "-->\n" << model_reconstruct(s) << '\n';
  return 0;
}
