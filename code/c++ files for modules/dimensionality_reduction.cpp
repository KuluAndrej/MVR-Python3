#include <math.h>
#include "mex.h"
#include <stdlib.h>
#include <vector>
#include <utility>
#include <string>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <sstream>
#include "tree_operations.h"
#include "string_operations.h"
#include "string_constructors.h"

using namespace std;  

/*
bool tuple_comparator (int first, int second) { 
    return tuples[first] < tuples[second]; 
}
*/

mxArray * getMexArray(const std::vector<int>& v){
    mxArray * mx = mxCreateDoubleMatrix(1, v.size(), mxREAL);
    std::copy(v.begin(), v.end(), mxGetPr(mx));
    return mx;
}




void read_data(int dim, vector<int>& encoding, vector<vector<int> >& matr, const mxArray *prhs[]) {
    double *P;
    P = mxGetPr(prhs[0]);
    encoding.resize(dim);
    
    dim = matr.size();
    for (int col = 0; col < dim; ++col) {
      encoding[col] = P[col * (dim + 1)];
    }
    for (int row = 1; row < dim + 1; ++row) {
      for (int col = 0; col < dim; ++col) {
        int index_in_P = col * (dim + 1) + row;
        if (P[index_in_P] == 1) {
          matr[row - 1].push_back(col);      
        }
      }
    }
    return;
}




pair<string, string> Solver(vector<vector<int> >& matr, int dim,  vector<int> & n_parameter_tokens, 
                            vector<int>& encoding, mxArray *plhs[]) {
 

  vector<int> equivalence_classes = fill_equivalence_classes(matr, encoding);  
  pair<vector<string>, vector<int> > tokens_data = retrieve_tokens();
  
  vector<string> tokens = tokens_data.first;
  vector<int> number_parameters = tokens_data.second;

  for (int i = 0; i < dim; ++i) {
    n_parameter_tokens[i] = number_parameters[encoding[i] - 1];
  }

  
  int current_bound = 1;
  vector<pair<int, int> > range_parameters(dim, make_pair(-1,-1));// = parameter_range_constructor(matr, current_bound, number_parameters, equivalence_classes, encoding);
  for (int i = 0; i < dim; ++i) {
    if (n_parameter_tokens[i] != 0) {
      range_parameters[i] = make_pair(current_bound, current_bound + n_parameter_tokens[i] - 1);
      current_bound = current_bound + n_parameter_tokens[i];
    }
  }


  plhs[3] = mxCreateDoubleMatrix(1, 1, mxREAL);
  double *y = mxGetPr(plhs[3]);
  int mx = -1;
  for (int i = 0; i < range_parameters.size(); ++i) {
    if (range_parameters[i].second > mx) {
      mx = range_parameters[i].second;
    }
  }
  y[0] = mx;
  string model = string_constructor(matr, tokens, range_parameters, number_parameters, encoding, 0);
  for (int i = 0; i < encoding.size(); ++i){
    --encoding[i];
  }
  string unparametred_model = string_constructor_unparametred(matr, tokens, encoding, 0);
  
  
  return make_pair(model, unparametred_model);        
}

void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[]) {
  int dim = mxGetM(prhs[0]) - 1;
  vector<int> n_parameter_tokens(dim);
  vector<vector<int> > matr(dim); 
  vector<int> encoding;
  read_data(dim, encoding, matr, prhs);  
  
  
  pair<string, string> models =  Solver(matr, dim, n_parameter_tokens, encoding, plhs);
  
  models.first = "@(w,x)" + models.first;
  
  plhs[0] = mxCreateString(models.first.c_str());
  plhs[1] = mxCreateString(models.second.c_str());
  plhs[2] = getMexArray(n_parameter_tokens);
  
  return;
}
