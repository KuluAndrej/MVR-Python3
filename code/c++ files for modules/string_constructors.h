#include <math.h>
#include <stdlib.h>
#include <vector>
#include <string>
#include <utility>
#include <stdio.h>
#include <sstream>
#include <ctype.h>
#include <iostream>
using namespace std;  


#define SSTR( x ) static_cast< std::ostringstream & >( \
        ( std::ostringstream() << std::dec << x ) ).str()

int self_max_in_vector(const vector<int> & a) {
  int default_v = 0;
  for (int i = 0; i < a.size(); ++i) {
    default_v = max(default_v, a[i]);
  }
  return default_v;
}

void print_vector(vector<string> to_print){
  for (int i = 0; i < to_print.size(); ++i) {
    cout << to_print[i] << " ";
  }
  cout << '\n';
}

void print_matrix(vector<vector<int> > to_print){
  for (int i = 0; i < to_print.size() - 1; ++i) {
    for (int j = 0; j < to_print[i].size(); ++j) {
      cout << to_print[i][j] << " ";
    }
    cout << '\n';
  } 
  for (int j = 0; j < to_print[to_print.size() - 1].size(); ++j) {
    cout << to_print[to_print.size() - 1][j] << " ";
  }
}

vector<pair<int, int> >  parameter_range_constructor(vector<vector<int> >& matr, int& current_bound,
                      vector<int>& number_parameters, vector<int>& equivalence_classes, vector<int>& encoding) {
  int dim = matr.size();
  
  vector<pair<int, int> > range_parameters(dim, make_pair(-1,-1));  
  vector<int> first_representatives_of_classes(self_max_in_vector(equivalence_classes) + 1, -1);

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


void print_vector(vector<int> to_print){
  for (int i = 0; i < to_print.size(); ++i) {
    cout << to_print[i] << " ";
  }
  cout << '\n';
}

string string_constructor_unparametred(vector<vector<int> >& matr, vector<string>& tokens, vector<int>& encoding, int root) {
  
  if (tokens[encoding[root]][0] == 'X' && tokens[encoding[root]][1] == '[') {    
    return tokens[encoding[root]];
  }
  string s = tokens[encoding[root]] + "(";
  for (int i = 0; i < int(matr[root].size()) - 1; ++i) {
    s = s + string_constructor_unparametred(matr, tokens, encoding, matr[root][i]) + ",";
  }
  if (matr[root].size() > 0) {
    s = s + string_constructor_unparametred(matr, tokens, encoding, matr[root][matr[root].size() - 1]);
  }
  s = s + ")";
  return s;
}


