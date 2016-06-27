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

#define SSTR( x ) static_cast< std::ostringstream & >( \
        ( std::ostringstream() << std::dec << x ) ).str()


using namespace std;  

vector<int> encoding;
vector<vector<int> > tuples;


bool label_comparator (int first, int second) { 
    return encoding[first] < encoding[second]; 
}

bool tuple_comparator (int first, int second) { 
    return tuples[first] < tuples[second]; 
}



void vprint(const vector<int>& a) {
    for(int i = 0; i < a.size(); ++i) {
      mexPrintf("%d ", a[i]);
    }
    mexPrintf("\n");
    return;
}

void pvprint(const vector<pair<int, int> >& a) {
    for(int i = 0; i < a.size(); ++i) {
      mexPrintf("%d %d\n", a[i].first, a[i].second);
    }
    mexPrintf("\n");
    return;
}

void nprint(int a) {
    mexPrintf("%d\n", a);
    return;
}

int max_in_vector(const vector<int> & a) {
  int default_v = 0;
  for (int i = 0; i < a.size(); ++i) {
    default_v = max(default_v, a[i]);
  }
  return default_v;
}



void read_data(int dim, vector<int>& encoding, vector<vector<int> >& matr, const mxArray *prhs[]) {
    double *P;
    P = mxGetPr(prhs[0]);

    encoding.clear();
    tuples.clear();
    encoding.resize(dim);
    tuples.resize(dim);

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



vector<int> find_leaves(vector<vector<int> >& matr) {
    vector<int> leaves;
    for (int col = 0; col < matr.size(); ++col) {
      if (matr[col].size() == 0) {
        leaves.push_back(col);
      }
    }
    
    sort(leaves.begin(), leaves.end(), label_comparator);
    return leaves;
}



void find_heights(vector<vector<int> >& matr,vector<int>& heights, int root) {  
  for (int i = 0; i < matr[root].size(); ++i) {
    find_heights(matr, heights, matr[root][i]);
    heights[root] = max(heights[root], 1 + heights[matr[root][i]]);
  }
  return;  
}



vector<int> fill_leaves_classes (int dim, vector<int>& equivalence_classes, vector<int>& leaves, int & counter_classes) {    
    equivalence_classes[leaves[0]] = counter_classes;
    for (int leaf = 1; leaf < leaves.size(); ++leaf) {
      if (encoding[leaves[leaf - 1]] == encoding[leaves[leaf]]) {
          equivalence_classes[leaves[leaf]] = counter_classes;        
      } else {
        counter_classes++;
        equivalence_classes[leaves[leaf]] = counter_classes;
      }
    }    
    counter_classes++;
    return equivalence_classes;
}




vector<vector<int> > level_divider (vector<vector<int> >& matr, vector<int>& heights) {
  int dim  = matr.size();
  
  find_heights(matr, heights, 0);
  int height_of_root = max_in_vector(heights);
  
  vector<vector<int> > llevels(height_of_root + 1);
  for (int i = 0; i < dim; ++i) {
    llevels[heights[i]].push_back(i);    
  }
  return llevels;
}


void fill_equivalence_classes (vector<vector<int> >& llevels, vector<vector<int> >& matr,
                              vector<int>& equivalence_classes, int & counter_classes) {
  int height_of_root = llevels.size() - 1;    
  for (int level = 1; level < height_of_root + 1; ++level) {
    for (int vert_in_level = 0; vert_in_level < llevels[level].size(); ++vert_in_level ) {
      for (int adj_s = 0; adj_s < matr[llevels[level][vert_in_level]].size(); ++adj_s) {
        tuples[llevels[level][vert_in_level]].push_back(equivalence_classes[matr[llevels[level][vert_in_level]][adj_s]]);
      }
      sort(tuples[llevels[level][vert_in_level]].begin(), tuples[llevels[level][vert_in_level]].end());
      tuples[llevels[level][vert_in_level]].push_back(encoding[llevels[level][vert_in_level]]);
    }
    sort(llevels[level].begin(), llevels[level].end(), tuple_comparator);
    equivalence_classes[llevels[level][0]] = counter_classes;
    for (int tuple = 1; tuple < llevels[level].size(); ++tuple) {
      if (tuples[llevels[level][tuple - 1]] == tuples[llevels[level][tuple]]) {
        equivalence_classes[llevels[level][tuple]] = counter_classes;
      } else {
        counter_classes++;
        equivalence_classes[llevels[level][tuple]] = counter_classes;
      }
    }
    counter_classes++;
  }
  return;
}


string string_constructor(vector<vector<int> >& matr, vector<string>& tokens, 
                        vector<pair<int, int> >& range_parameters, vector<int>& number_parameters,
                        int root) {
  if (tokens[encoding[root] - 1][0] == 'x' && (tokens[encoding[root] - 1][1] >= '1' ) && 
      tokens[encoding[root] - 1][1] <= '9') {
    string s = "x(:," + SSTR( tokens[encoding[root] - 1][1] - '0') + ")";
    return s;
  }
  string s = tokens[encoding[root] - 1] + "(";
  if (number_parameters[encoding[root]-1] == 0) {
    s = s + "[],";
  } else {
    s = s + "w(" + SSTR( range_parameters[root].first ) + ":" + 
                   SSTR( range_parameters[root].second ) + "),";
  }
  for (int i = 0; i < matr[root].size() - 1; ++i) {
    s = s + string_constructor(matr, tokens, range_parameters, number_parameters, matr[root][i]) + ",";
  }
  s = s + string_constructor(matr, tokens, range_parameters, number_parameters, matr[root][matr[root].size() - 1]);
  s = s + ")";
  return s;
}


string string_constructor_unparametred(vector<vector<int> >& matr, vector<string>& tokens, int root) {
  if (tokens[encoding[root] - 1][0] == 'x' && (tokens[encoding[root] - 1][1] >= '1' ) && 
      tokens[encoding[root] - 1][1] <= '9') {    
    return tokens[encoding[root] - 1];
  }
  string s = tokens[encoding[root] - 1] + "(";
  for (int i = 0; i < matr[root].size() - 1; ++i) {
    s = s + string_constructor(matr, tokens, matr[root][i]) + ",";
  }
  s = s + string_constructor(matr, tokens, matr[root][matr[root].size() - 1]);
  s = s + ")";
  return s;
}



vector<pair<int, int> >  parameter_range_constructor(vector<vector<int> >& matr, 
                      vector<int>& number_parameters, vector<int>& equivalence_classes) {
  int dim = matr.size();
  int current_bound = 1;

  vector<pair<int, int> > range_parameters(dim, make_pair(-1,-1));  
  vector<int> first_representatives_of_classes(max_in_vector(equivalence_classes) + 1, -1);

  for (int j = 0; j < dim; ++j) {
    if (first_representatives_of_classes[equivalence_classes[j]] == -1) {
      first_representatives_of_classes[equivalence_classes[j]] = j;
    }
  }

  for (int i = 0; i < dim; ++i) {    
    if (number_parameters[encoding[i]-1] != 0) {
      if (first_representatives_of_classes[equivalence_classes[i]] != i) {
        range_parameters[i].first = range_parameters[first_representatives_of_classes[equivalence_classes[i]]].first;
        range_parameters[i].second = range_parameters[first_representatives_of_classes[equivalence_classes[i]]].second;
      } else {
        range_parameters[i].first = current_bound;
        range_parameters[i].second = current_bound + number_parameters[encoding[i]-1] - 1;
        current_bound = range_parameters[i].second + 1;         
      }
    }
  }
  return range_parameters;
}

pair<string, string> Solver(vector<vector<int> >& matr, int& counter_classes, int dim) {
  vector<int> equivalence_classes(dim), heights(dim);
  vector<vector<int> > llevels = level_divider(matr, heights);  
  vector<int> leaves = find_leaves(matr);
  fill_leaves_classes(dim, equivalence_classes, leaves,  counter_classes);
  fill_equivalence_classes(llevels, matr, equivalence_classes, counter_classes);
  
  ifstream input_stream("numbParam.txt");
  

  const int NUMBER_OF_TOKENS = 33;
  int useless_feature;
  vector<string> tokens(NUMBER_OF_TOKENS);
  vector<int> number_parameters(NUMBER_OF_TOKENS);
  for (int i = 0; i < NUMBER_OF_TOKENS; ++i) {
    input_stream >> tokens[i] >> number_parameters[i] >> useless_feature;
  }
  input_stream.close();
  

  vector<pair<int, int> > range_parameters = 
              parameter_range_constructor(matr, number_parameters, equivalence_classes);
  
  string model = string_constructor(matr, tokens, range_parameters, number_parameters, 0);
  string unparametred_model = string_constructor_unparametred(matr, tokens, 0);
  //mexPrintf("%s", model.c_str());
  
  return make_pair(model, unparametred_model);
}

void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[]) {
  double * y;
  int counter_classes = 1;
  int dim = mxGetM(prhs[0]) - 1;

  vector<vector<int> > matr(dim); 

  read_data(dim, encoding, matr, prhs);  
  pair<string, string> models =  Solver(matr, counter_classes, dim);
  
  mexPrintf("%s", models[0].c_str());

  //plhs[0] = mxCreateDoubleMatrix(1, 1, mxREAL);
  plhs[0] = mxCreateString(models[0].c_str());
  plhs[1] = mxCreateString(models[1].c_str());
  //y = mxGetPr(plhs[0]);
  
  //*y = a; 
  return;
}
