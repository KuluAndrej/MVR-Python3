#include <math.h>
#include <stdlib.h>
#include <vector>
#include <string>
#include <utility>
#include <stdio.h>
#include <stack>
#include <cctype>
#include "string_operations.h"
#include "string_constructors.h"


using namespace std;  

pair<vector<vector<int> >, vector<int> > create_incid_matrix_tokens(map<string, int>& map_tokens, const string& handle) {

  pair<int, int> counters = find_number_of_tokens(handle);
  int number_tokens = counters.first + counters.second;
  vector<vector<int> > matr(number_tokens);  
  vector<int> encodings(number_tokens);

  stack<int> waiting_tokens;
  int current_token = 0;
  bool is_a_token_processed_now = false;
  int left = 0, right = 0;
  //firsty, process the root specifically
  for (right = 0; right < handle.size(); ++right) {
    if (handle[right] == '_') {
      // the root is detected
      waiting_tokens.push(current_token);
      string token (handle.begin() + left, handle.begin() + right + 1);

      encodings[current_token] = map_tokens[token];          
      right++;
      break;  
    }
  }
  // now process the remaining vertices
  for (; right < handle.size(); ++right) {
    if (handle[right] == ')') {
      waiting_tokens.pop();
    }
    if (!is_a_token_processed_now && (handle[right] >= 'a') && (handle[right] <= 'z')) {
      is_a_token_processed_now = true;
      left = right;
    }
    // if a token is found
    if (handle[right] == '_') {
      // new token is detected
      current_token++;
      matr[waiting_tokens.top()].push_back(current_token);
      waiting_tokens.push(current_token);
      string token (handle.begin() + left, handle.begin() + right + 1);
      encodings[current_token] = map_tokens[token];
      is_a_token_processed_now = false;      
    }
    // if a variable is found
    if (right < handle.size()-1 && handle[right] == 'x' && 
        (handle[right+1] >= '0') && (handle[right+1] <= '9')) {
      // new variable is detected
      current_token++;
      matr[waiting_tokens.top()].push_back(current_token);
      //waiting_tokens.push(current_token);
      while (right < handle.size()-1 && handle[right] == 'x' && 
        (handle[right+1] >= '0') && (handle[right+1] <= '9')) {
        right++;
      }
      string token (handle.begin() + left, handle.begin() + right + 1);
      encodings[current_token] = map_tokens[token];
      is_a_token_processed_now = false;      
    }
  }
  
  return make_pair(matr, encodings);
}


pair<vector<vector<int> >, vector<string> > create_matrix_tokens(const string& handle) {
  
  pair<int, int> counters = find_number_of_tokens(handle);
  int number_tokens = counters.first + counters.second;

  vector<string> tokens(number_tokens); 
  vector<vector<int> > matr(number_tokens);
  for (int i = 0; i < number_tokens; ++i) {
    matr[i].resize(number_tokens);
  }
  
  //check if the handle is the only variable
  if (handle[0] == 'x' && isdigit(handle[1])) {
    tokens[0] = handle;
    return make_pair(matr, tokens);
  }

  stack<int> waiting_tokens;
  int current_token = 0;
  bool is_a_token_processed_now = false;
  int left = 0, right = 0;
  //firsty, process the root specifically

  for (right = 0; right < handle.size(); ++right) {
    if (handle[right] == '_') {
      // the root is detected
      waiting_tokens.push(current_token);
      string temp (handle.begin() + left, handle.begin() + right + 1);
      tokens[current_token] = temp;          
      right++;
      break;  
    }
  }
  // now process the remaining vertices
  for (; right < handle.size(); ++right) {
    if (handle[right] == ')') {
      waiting_tokens.pop();
    }
    if (!is_a_token_processed_now && (handle[right] >= 'a') && (handle[right] <= 'z')) {
      is_a_token_processed_now = true;
      left = right;
    }
    // if a token is found
    if (handle[right] == '_') {
      // new token is detected
      current_token++;
      matr[waiting_tokens.top()][current_token] = 1;
      waiting_tokens.push(current_token);
      string temp (handle.begin() + left, handle.begin() + right + 1);
      tokens[current_token] = temp;
      is_a_token_processed_now = false;      
    }
    // if a variable is found
    if (right < handle.size()-1 && handle[right] == 'x' && 
        (handle[right+1] >= '0') && (handle[right+1] <= '9')) {
      // new variable is detected
      current_token++;
      matr[waiting_tokens.top()][current_token] = 1;
      //waiting_tokens.push(current_token);
      while (right < handle.size()-1 && handle[right] == 'x' && 
        (handle[right+1] >= '0') && (handle[right+1] <= '9')) {
        right++;
      }
      string temp (handle.begin() + left, handle.begin() + right + 1);
      tokens[current_token] = temp;
      is_a_token_processed_now = false;      
    }
  }
  
  return make_pair(matr, tokens);
}

vector<string> create_tokens_of_model(const string& handle) {
  
  pair<int, int> counters = find_number_of_tokens(handle);
  int number_tokens = counters.first + counters.second;

  vector<string> tokens(number_tokens); 
  
  //check if the handle is the only variable
  if (handle[0] == 'x' && isdigit(handle[1])) {
    tokens[0] = handle;
    return tokens;
  }

  stack<int> waiting_tokens;
  int current_token = 0;
  bool is_a_token_processed_now = false;
  int left = 0, right = 0;
  //firsty, process the root specifically

  for (right = 0; right < handle.size(); ++right) {
    if (handle[right] == '_') {
      // the root is detected
      waiting_tokens.push(current_token);
      string temp (handle.begin() + left, handle.begin() + right + 1);
      tokens[current_token] = temp;          
      right++;
      break;  
    }
  }
  // now process the remaining vertices
  for (; right < handle.size(); ++right) {
    if (handle[right] == ')') {
      waiting_tokens.pop();
    }
    if (!is_a_token_processed_now && (handle[right] >= 'a') && (handle[right] <= 'z')) {
      is_a_token_processed_now = true;
      left = right;
    }
    // if a token is found
    if (handle[right] == '_') {
      // new token is detected
      current_token++;
      waiting_tokens.push(current_token);
      string temp (handle.begin() + left, handle.begin() + right + 1);
      tokens[current_token] = temp;
      is_a_token_processed_now = false;      
    }
    // if a variable is found
    if (right < handle.size()-1 && handle[right] == 'x' && 
        (handle[right+1] >= '0') && (handle[right+1] <= '9')) {
      // new variable is detected
      current_token++;
      //waiting_tokens.push(current_token);
      while (right < handle.size()-1 && handle[right] == 'x' && 
        (handle[right+1] >= '0') && (handle[right+1] <= '9')) {
        right++;
      }
      string temp (handle.begin() + left, handle.begin() + right + 1);
      tokens[current_token] = temp;
      is_a_token_processed_now = false;      
    }
  }
  
  return tokens;
}