#include <math.h>
#include <stdlib.h>
#include <vector>
#include <string>
#include <utility>
#include <stdio.h>
#include <sstream>
#include <fstream>
#include <ctype.h>
#include <set>

#include <map>
using namespace std;  

const int NUMBER_OF_TOKENS = 50;  




set<string> read_special_tokens(const string type) {
  set<string> linkers;
  string filename = string("data/Patterns Creation/tokens_") + type + string(".txt");
  ifstream input_stream(filename.c_str());

  string giglet_string;  
  string useless_feature;  

  while (true) {
    input_stream >> giglet_string >> useless_feature >> useless_feature >> useless_feature;
    linkers.insert(giglet_string);
    if(input_stream.eof()) break;
  }

  input_stream.close();
  return linkers;
}

vector<string> read_dummy_linkers() {
  vector<string> linkers;

  ifstream input_stream("data/Patterns Creation/tokens_linkers.txt");

  string giglet_string;  
  string useless_feature;  

  while (true) {
    input_stream >> giglet_string >> useless_feature >> useless_feature >> useless_feature;
    linkers.push_back(giglet_string);
    if(input_stream.eof()) break;
  }

  input_stream.close();
  return linkers;
}

pair<map<string, int>, int> read_info_primitives () {
  bool isset = false;
  ifstream input_stream("code/primitives/Primitives.txt");
  map<string, int> map_tokens;
  
  int useless_feature1;
  string token, last_token;
  int counter = 0;
  input_stream >> token >> token >> token >> token;
  while (true) {
    input_stream >> token >> useless_feature1 >> useless_feature1 >> useless_feature1;
    if (map_tokens.empty() or token != last_token) {
      map_tokens.insert(make_pair(token, counter));
      counter++;
      last_token = token;
    }
    if(input_stream.eof()) break;
  }
  map_tokens.insert(make_pair(string("X[0]"), counter));
  counter++;
  map_tokens.insert(make_pair(string("X[1]"), counter));
  counter++;

  input_stream.close();
  return make_pair(map_tokens, map_tokens.size()-2);
}


pair<map<string, int>, vector<int> > read_info_commutativenes () {
  ifstream input_stream("code/primitives/Primitives.txt");
  map<string, int> map_tokens;
  vector<int> commutativeness;
  
  int useless_feature1, is_commutative;
  int counter = 0;
  string token, last_token;
  input_stream >> token >> token >> token >> token;
  while (true) {
    input_stream >> token >> useless_feature1 >> useless_feature1 >> is_commutative;
    if (map_tokens.empty() or token != last_token) {
      commutativeness.push_back(is_commutative);
      map_tokens.insert(make_pair(token, counter));    
      counter++;
      last_token = token;
    }
    if(input_stream.eof()) break;
  }

  input_stream.close();
  return make_pair(map_tokens, commutativeness);
}


pair<vector<string>, vector<int> > retrieve_tokens() {
  ifstream input_stream("code/primitives/Primitives.txt");
  
  int useless_feature;
  vector<string> tokens;
  vector<int> number_parameters;

  string token_input;
  int number_of_parameters_input;
  input_stream >> token_input >> token_input >> token_input >> token_input;
  while (true) {
    input_stream >> token_input >> number_of_parameters_input >> useless_feature >> useless_feature;
    if (tokens.empty() or token_input != tokens.back()) {
      tokens.push_back(token_input);
      number_parameters.push_back(number_of_parameters_input);
    }
    if(input_stream.eof()) break;
  }
  tokens.push_back("X[0]");
  number_parameters.push_back(0);
  tokens.push_back("X[1]");
  number_parameters.push_back(0);
  
  input_stream.close();
  

  return make_pair(tokens, number_parameters);
}

vector<int> find_positions_of_tokens(const string& handle) {
  vector<int> positions;
  bool is_token_processed = false;
  for (int i = 0; i < handle.size(); ++i) {
    if ((i + 1 < handle.size()) && handle[i] == 'X' && handle[i + 1] == '[' ) {
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
      if (i < handle.size()-1 && handle[i] == 'X' && handle[i+1] == '[') {
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

