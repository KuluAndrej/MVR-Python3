#include <math.h>
#include <stdlib.h>
#include <vector>
#include <string>
#include <utility>
#include <stdio.h>
#include <sstream>
#include <fstream>
#include <ctype.h>
#include <map>
using namespace std;  

const int NUMBER_OF_TOKENS = 33;  

pair<map<string, int>, int> read_info_primitives () {
  int minimum_code_for_var;
  bool isset = false;
  ifstream input_stream("data/numbParam.txt");
  map<string, int> map_tokens;
  
  int useless_feature1;
  string token;
  vector<int> number_parameters(NUMBER_OF_TOKENS);
  for (int i = 0; i < NUMBER_OF_TOKENS; ++i) {
    input_stream >> token >> useless_feature1 >> useless_feature1 >> useless_feature1;
    map_tokens.insert(make_pair(token, i));
    if (!isset && token[0] == 'x' && (token.size() > 1) &&  isdigit(token[1])) {
      minimum_code_for_var = i;
      isset = true;
    }
  }

  input_stream.close();
  return make_pair(map_tokens, minimum_code_for_var);
}


pair<map<string, int>, vector<int> > read_info_commutativenes () {
  ifstream input_stream("data/numbParam.txt");
  map<string, int> map_tokens;
  vector<int> commutativeness(NUMBER_OF_TOKENS);
  
  int useless_feature1;
  
  string token;
  for (int i = 0; i < NUMBER_OF_TOKENS; ++i) {
    input_stream >> token >> useless_feature1 >> useless_feature1 >> commutativeness[i];
    map_tokens.insert(make_pair(token, i));    
  }

  input_stream.close();
  return make_pair(map_tokens, commutativeness);
}


pair<vector<string>, vector<int> > retrieve_tokens() {
  ifstream input_stream("data/numbParam.txt");
  
  int useless_feature;
  vector<string> tokens(NUMBER_OF_TOKENS);
  vector<int> number_parameters(NUMBER_OF_TOKENS);
  for (int i = 0; i < NUMBER_OF_TOKENS; ++i) {
    input_stream >> tokens[i] >> number_parameters[i] >> useless_feature >> useless_feature;
  }
  input_stream.close();
  return make_pair(tokens, number_parameters);
}

vector<int> find_positions_of_tokens(const string& handle) {
  vector<int> positions;
  bool is_token_processed = false;
  for (int i = 0; i < handle.size(); ++i) {
    if ((i + 1 < handle.size()) && (handle[i] == 'x') && (isdigit(handle[i + 1])) ) {
      positions.push_back(i);
      continue;
    }
    if (!is_token_processed && isalpha(handle[i])) {
      positions.push_back(i);
      is_token_processed = true;
      continue;
    }
    if (handle[i] == '_') {
      is_token_processed = false;
    }
  }
  return positions;
}


pair<int, int> find_number_of_tokens(const string& handle) {
  int counter_tokens = 0;
  int counter_variables = 0;
  
  for (int i = 0; i < handle.size(); ++i) {
    if (handle[i] == '_') {
      counter_tokens++;
    } else {
      if (i < handle.size()-1 && handle[i] == 'x' && (handle[i+1] >= '0') && (handle[i+1] <= '9')) {
        counter_variables++;
      }
    }
  }
  return make_pair(counter_tokens, counter_variables);
}

string eraser(const string& s, int pos, int number_of_deletions) {
  string t(s.size() - number_of_deletions, '_');
  copy( s.begin(), s.begin() + pos, t.begin() );
  copy( s.begin() + pos + number_of_deletions, s.end(), t.begin() + pos );
  return t;
}

