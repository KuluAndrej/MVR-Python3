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
#include <stack>
#include "tree_operations.h"
#include "create_data_by_handle.h"

#define SSTR( x ) static_cast< std::ostringstream & >( \
        ( std::ostringstream() << std::dec << x ) ).str()


using namespace std;  

mxArray * getMexArray(const std::vector<int>& v){
    mxArray * mx = mxCreateDoubleMatrix(1, v.size(), mxREAL);
    std::copy(v.begin(), v.end(), mxGetPr(mx));
    return mx;
}


string read_data(const mxArray *prhs[]) {
    
    char * input_buf = mxArrayToString(prhs[0]);
    string handle(input_buf);
    
    return handle;
}


void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[]) {  
  
  string handle = read_data(prhs);
  pair<vector<vector<int> >, vector<string> > model_data  = create_matrix_tokens(handle);
  vector<vector<int> > matr = model_data.first;
  vector<string> tokens = model_data.second;


  int dim = tokens.size();
  plhs[0] = mxCreateDoubleMatrix(dim, dim, mxREAL);
  double *filler_output;
  filler_output = mxGetPr(plhs[0]);
  for (int row = 0; row < dim; ++row) {
    for (int col = 0; col < dim; ++col) {
      filler_output[ col * dim + row] = matr[row][col];
    } 
  }
  int dims[1];
  dims[0] = tokens.size();
  plhs[1] = mxCreateCellArray(1, dims);
  for (int i = 0; i < dim; ++i) {
    mxSetCell(plhs[1], i, mxCreateString(tokens[i].c_str()));
  }
  
  vector<int> encoding(dim);
  pair<map<string, int>, int> tokens_info = read_info_primitives ();
  map<string, int> map_tokens = tokens_info.first;
  for (int i = 0; i < dim; ++i) {
    encoding[i] = map_tokens[tokens[i]] + 1;
  }

  plhs[2] = getMexArray(encoding);

  return;
}
