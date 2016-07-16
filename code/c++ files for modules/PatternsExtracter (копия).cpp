/*

Author: Kulunchakov Andrei
*/

#include <iostream>
#include <vector>
#include <string>
#include <set>
#include <utility>
#include <fstream> 
#include <sstream>
#include <stdlib.h>
#include "tree_operations.h"
#include "create_data_by_handle.h"

using namespace std;

/*
#include <boost/python/def.hpp>
#include <boost/python/module.hpp>

namespace bp = boost::python;
*/

const int UNFILLED_SIBSTITUTION = -1;
const int USUAL_TOKEN = 0;
const int DUMMY_TOKEN = 1;
const int LINKER_TOKEN = 2;



vector<int> get_types_of_nodes(const set<string>& linkers, const set<string>& dummy_tokens, 
                        const map<string, int>& map_tokens, const vector<int> encodings) {
  vector<int> type_of_nodes(encodings.size());
  pair<vector<string>, vector<int> > info_tokens = retrieve_tokens();
  vector<string> token_names = info_tokens.first;
  for (int i = 0; i < type_of_nodes.size(); ++i) {
    string token_name = token_names[encodings[i]];
    if (dummy_tokens.count(token_name) == DUMMY_TOKEN) {
      type_of_nodes[i] = 1;  
    } else {
      if (linkers.count(token_name)) {
        type_of_nodes[i] = LINKER_TOKEN;
      } else {
        type_of_nodes[i] = USUAL_TOKEN;
      }
    }
  }
  return type_of_nodes;
}

bool retrieve_patterns_ranges( const vector<vector<int> >& matr, const vector<int>& type_of_nodes, const vector<int>& right_bounds,
                        bool is_parent_set,
                        int pos_current_parent, int pos_parents_child, 
                        int pos_current_root, vector<pair<int, int> >& patterns_range) {
  bool is_child_linker_encountered = false;

  if (!is_parent_set) {
    if (type_of_nodes[pos_current_root] == LINKER_TOKEN) {
        is_child_linker_encountered = true;
        if (pos_current_root != 0) {
          patterns_range.push_back(make_pair(0,pos_current_root));
        }
        vector<bool> is_child_subtree_contain_linker(matr[pos_current_root].size());
        for (int i = 0; i < matr[pos_current_root].size(); ++i) {
          is_child_subtree_contain_linker[i] = retrieve_patterns_ranges(matr, type_of_nodes, right_bounds, true, 
                                                                        pos_current_root, matr[pos_current_root][i], 
                                                                        matr[pos_current_root][i], patterns_range);
        }
        bool should_whole_subtree_be_extracted = true;
        for (int i = 0; i < matr[pos_current_root].size(); ++i) {
          should_whole_subtree_be_extracted &= !is_child_subtree_contain_linker[i];
          if (!is_child_subtree_contain_linker[i]) {
            patterns_range.push_back(make_pair(matr[pos_current_root][i],right_bounds[matr[pos_current_root][i]]));
          }
        }
        if (should_whole_subtree_be_extracted) {
          patterns_range.push_back(make_pair(pos_current_root,right_bounds[matr[pos_current_root].back()]));
        }
    }
    if (type_of_nodes[pos_current_root] == 1 || type_of_nodes[pos_current_root] == 0) {
      bool should_whole_subtree_be_extracted = true;
                
      for (int i = 0; i < matr[pos_current_root].size(); ++i) {
        is_child_linker_encountered |= retrieve_patterns_ranges(matr, type_of_nodes, right_bounds, false, 
                                                                pos_current_parent, pos_parents_child, 
                                                                matr[pos_current_root][i], patterns_range);
        should_whole_subtree_be_extracted &= !is_child_linker_encountered;        
      }
      if (should_whole_subtree_be_extracted) {
        if (matr[pos_current_root].size() > 0) {
          patterns_range.push_back(make_pair(pos_current_root,right_bounds[matr[pos_current_root].back()]));
        }
      }
    }
  }
  if (is_parent_set) {
    if (type_of_nodes[pos_current_root] == LINKER_TOKEN) {
        is_child_linker_encountered = true;
        if (pos_current_root != pos_parents_child) {
          patterns_range.push_back(make_pair(pos_parents_child, pos_current_root));
        }
                
        vector<bool> is_child_subtree_contain_linker(matr[pos_current_root].size());
        for (int i = 0; i < matr[pos_current_root].size(); ++i) {
          is_child_subtree_contain_linker[i] = retrieve_patterns_ranges(matr, type_of_nodes, right_bounds, true, 
                                                                        pos_current_root, matr[pos_current_root][i], 
                                                                        matr[pos_current_root][i], patterns_range);
        }
        bool is_current_subtree_fully_extracted = true;
        for (int i = 0; i < is_child_subtree_contain_linker.size(); ++i) {
          is_current_subtree_fully_extracted &= !is_child_subtree_contain_linker[i];
        }

        if (is_current_subtree_fully_extracted) {
          patterns_range.push_back(make_pair(pos_current_root,right_bounds[pos_current_root]));
        } else {
          for (int i = 0; i < matr[pos_current_root].size(); ++i) {
            if (!is_child_subtree_contain_linker[i]) {
              patterns_range.push_back(make_pair(matr[pos_current_root][i],right_bounds[matr[pos_current_root][i]]));
            }
          }
        }
    }
    if (type_of_nodes[pos_current_root] == DUMMY_TOKEN || type_of_nodes[pos_current_root] == USUAL_TOKEN) {
      for (int i = 0; i < matr[pos_current_root].size(); ++i) {
        is_child_linker_encountered |= retrieve_patterns_ranges(matr, type_of_nodes, right_bounds, true, 
                                                                pos_current_parent, pos_parents_child, 
                                                                matr[pos_current_root][i], patterns_range);
      }
    }
  }
  return is_child_linker_encountered;
}

int find_right_bounds_of_rooted_subtrees(const vector<vector<int> >& matr, 
                                        int current_root, vector<int>& right_bounds) {
  int current_right_bound = current_root;
  for (int i = 0; i < matr[current_root].size(); ++i) {
    current_right_bound = find_right_bounds_of_rooted_subtrees(matr, matr[current_root][i], right_bounds);
  }
  right_bounds[current_root] = current_right_bound;
  return current_right_bound;
}

vector<pair<int, int> > process_ranges(const vector<vector<int> >& matr,
                                      const vector<pair<int, int> >& patterns_range, 
                                      const vector<int>& type_of_nodes){

  vector<pair<int, int> > patterns_range_cleaned;
  for (int i = 0; i < patterns_range.size(); ++i) {
    pair<int, int> cur_pair = patterns_range[i];
    
    if (type_of_nodes[cur_pair.second] == 2) {
      cur_pair.second -= 1;      
    }
    if (type_of_nodes[cur_pair.first] != 2 and matr[cur_pair.second].size() == 0) {
      cur_pair.second -= 1;      
    }
    if (cur_pair.first != cur_pair.second) {
      int num_tokens_non_dummy_nonvars = 0;
      for (int i = cur_pair.first; i <= cur_pair.second; ++i) {
        if (matr[i].size() > 0 and type_of_nodes[i] != 1) {
          num_tokens_non_dummy_nonvars++;
        }
      }      
      if (num_tokens_non_dummy_nonvars > 1) {
          patterns_range_cleaned.push_back(cur_pair);        
      }
    }
  }
  return patterns_range_cleaned;
}

string extract_pattern_substring(const vector<vector<int> >& matr, const vector<int>& encodings,
                                const vector<string>& tokens_names, const vector<int>& type_of_nodes,
                                int end, int current_root) {
  if (type_of_nodes[current_root] == 1) {
    if (matr[current_root].size() > 0) {
      return extract_pattern_substring(matr, encodings, tokens_names, type_of_nodes, end, matr[current_root][0]);
    } else {
      return "";
    }
  }
  
  string this_token = tokens_names[encodings[current_root]];
  if (current_root == end) {
    return this_token;
  } 
  if (matr[current_root].size() == 0) {
    return string("");
  }

  this_token += string("(");
  for (int i = 0; i < int(matr[current_root].size()) - 1; ++i) {
    if (matr[matr[current_root][i]].size() > 0) {
      this_token += extract_pattern_substring(matr, encodings, tokens_names, type_of_nodes, end, matr[current_root][i]);
    }    
    this_token += string(",");
  }  
  if (matr[current_root].size() > 0) {
    this_token += extract_pattern_substring(matr, encodings, tokens_names, type_of_nodes, end, matr[current_root].back());
    this_token += string(")");
  }
  return this_token;
}

vector<string> ranges_to_strings(const vector<vector<int> >& matr, const vector<int>& encodings,  
                                const vector<int>& type_of_nodes, const vector<string>& tokens_names,
                                vector<pair<int, int> >& patterns_range) {
  vector<string> patterns(patterns_range.size());

  for (int i = 0; i < patterns_range.size(); ++i) {
    patterns[i] = extract_pattern_substring(matr, encodings, tokens_names, type_of_nodes, 
                                            patterns_range[i].second, patterns_range[i].first);
  }
  return patterns;
}

string extract_patterns(string handle){
  vector<string> patterns;
  set<string> linkers      = read_special_tokens("linkers");
  set<string> dummy_tokens = read_special_tokens("dummy");
  

  pair<map<string, int>, int> tokens_info  = read_info_primitives ();
  map<string, int> map_tokens = tokens_info.first;

  pair<vector<string>, vector<int> > tokens_names_and_params = retrieve_tokens();
  vector<string> tokens_names = tokens_names_and_params.first;

  pair<vector<vector<int> >, vector<int> > model_info = create_incid_matrix_tokens(map_tokens, handle);
  vector<vector<int> > matr = model_info.first;
  vector<int> encodings     = model_info.second;


  vector<int> type_of_nodes = get_types_of_nodes(linkers, dummy_tokens, map_tokens, encodings);

  vector<int> right_bounds(encodings.size());
  find_right_bounds_of_rooted_subtrees(matr, 0, right_bounds);

  vector<pair<int, int> > patterns_range;   
  retrieve_patterns_ranges(matr, type_of_nodes, right_bounds, false, -1, -1, 0, patterns_range);
  patterns_range = process_ranges(matr, patterns_range, type_of_nodes);
  patterns = ranges_to_strings(matr, encodings, type_of_nodes, tokens_names, patterns_range);
  
  /*
  if (patterns.size() == 0 || (patterns.size() == 1 and patterns[0] == handle)) {
    patterns_range.clear();
    int start = 0;
    for (int i = 0; i < type_of_nodes.size(); ++i) {
      if (type_of_nodes[i] == DUMMY_TOKEN) {

        patterns_range.push_back(make_pair(start, i));
        start = i + 1;
      }
    }
    if (patterns_range.size() > 0 && start < type_of_nodes.size() - 1) {
      patterns_range.push_back(make_pair(start, type_of_nodes.size() - 1));
    }
    for (int i = 0; i < patterns_range.size(); ++i) {
      cout << patterns_range[i].first << ' ' << patterns_range[i].second << '\n';
    }
    patterns = ranges_to_strings(matr, encodings, type_of_nodes, tokens_names, patterns_range);
    if (patterns.size() == 1 and patterns[0] == handle) {
      patterns.clear();
    }
  }
  */
  string unite_patterns("");
  for (int i = 0; i < int(patterns.size()) - 1; ++i) {
    unite_patterns += patterns[i];
    unite_patterns += string("&");
  }
  if (patterns.size() > 0) {
    unite_patterns += patterns.back();
  }
  return unite_patterns;
} 

/*
BOOST_PYTHON_MODULE(patterns_extracter) {
	bp::def("extract_patterns", extract_patterns);
    	
}
*/

int main(){
  //string s = "times2_(lnl_(plus2_(x0,sina_(x0))),plus_(sina_(lnl_(times2_(sina_(x0),x0)))))";
  string s = "linear_(sina_(sina_(sina_(atana_(x0)))))";
  //string s = "times2_(tana_(hvs_(normal_(x0))),atana_(x0))";
  cout << "init_model = " << s <<'\n';
  cout << extract_patterns(s) << '\n';
  cout << s <<'\n';
  return 0;
}

