#include "mex.h"
#include <stdlib.h>
#include <vector>
#include <string>
#include <utility>
#include <algorithm>
#include <stdio.h>
using namespace std;  




mxArray * getMexArray(const std::vector<int>& v){
    mxArray * mx = mxCreateDoubleMatrix(1, v.size(), mxREAL);
    std::copy(v.begin(), v.end(), mxGetPr(mx));
    return mx;
}

vector<pair<string, int> > read_data(const mxArray *prhs[]) {
  const mwSize *dims; 
  dims = mxGetDimensions(prhs[0]);
  
  
  // process the rules
  vector<pair<string, int> > models(max(dims[0], dims[1]));
  for (int ind = 0; ind < max(dims[0], dims[1]); ++ind) {
    models[ind] = make_pair(mxArrayToString(mxGetCell(prhs[0], ind )), ind);    
  }
  return models; 
}


void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[]) {
  
  vector<pair<string, int> > models = read_data(prhs);  
  sort(models.begin(), models.end());
  vector<int> indeces_of_unique(1, models[0].second);
  int index_last_new_model = 0;
  for (int i = 1; i < models.size(); ++i) {
    if (models[i].first != models[index_last_new_model].first) {
      indeces_of_unique.push_back(models[i].second);
      index_last_new_model = models[i].second;
    }
  }

  sort(indeces_of_unique.begin(), indeces_of_unique.end());
  plhs[0] = getMexArray(indeces_of_unique);
  
  return;
}
