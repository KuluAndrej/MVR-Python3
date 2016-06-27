#include "mex.h"
#include <math.h>
#include <stdlib.h>
#include <vector>
#include <string>
#include <utility>
#include <stdio.h>
#include <ctype.h>
#include <map>
#include "string_constructors.h"  
#include "print_operations.h"  
#include "create_data_by_handle.h"

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
  
  if (second_arg == UNFILLED_INT || end_of_second_arg == UNFILLED_INT) {
    mexErrMsgIdAndTxt("MATLAB:MEX", "Does not fill the positions.");
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


void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[]) {
  
  string modelhandle = mxArrayToString(prhs[0]);
  vector<int> commutativeness;
  
  string unparametred_handle = from_parametred_to_unparametred(modelhandle);
  
  pair<map<string, int>, vector<int> > tokens_data = read_info_commutativenes();
  vector<int> vectorOfCommutativeness = tokens_data.second;

  pair<vector<vector<int> >, vector<int> > model_data = create_incid_matrix_tokens(tokens_data.first,  unparametred_handle);
  commutativeness.resize(model_data.first.size());
  vector<int> encoding = model_data.second;
  for (int i = 0; i < encoding.size(); ++i) {
    if (vectorOfCommutativeness[encoding[i]]) {
      commutativeness[i] = vectorOfCommutativeness[encoding[i]];
    }
  }
  
  Solver(unparametred_handle, commutativeness);
  plhs[0] = string2mxArray(modelhandle);
  /*
  string final_handle = Solver(rules, modelhandle);
  mexPrintf("%s\n", final_handle.c_str());
  */
  return;
}