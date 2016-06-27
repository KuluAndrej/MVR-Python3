#include <math.h>
#include "mex.h"
#include <vector>
#include <algorithm>
#include <stdio.h>
#include <utility>
#include "print_operations.h"

using namespace std;  

int max_in_vector(const vector<int> & a) {
  int default_v = 0;
  for (int i = 0; i < a.size(); ++i) {
    default_v = max(default_v, a[i]);
  }
  return default_v;
}


vector<int> find_leaves(vector<vector<int> >& matr, vector<int> & encoding) {
    vector<pair<int, int> > labeled_leaves;
    for (int col = 0; col < matr.size(); ++col) {
      if (matr[col].size() == 0) {
        labeled_leaves.push_back(make_pair(encoding[col], col));
      }
    }
    
    sort(labeled_leaves.begin(), labeled_leaves.end());
    vector<int> leaves(labeled_leaves.size());
    for (int i = 0; i < leaves.size(); ++i) {
      leaves[i] = labeled_leaves[i].second;
    }

    return leaves;
}


void find_heights(vector<vector<int> >& matr, vector<int>& heights, int root) {  
  for (int i = 0; i < matr[root].size(); ++i) {
    find_heights(matr, heights, matr[root][i]);
    heights[root] = max(heights[root], 1 + heights[matr[root][i]]);
  }
  return;  
}


vector<int> fill_leaves_classes (int dim, vector<int>& equivalence_classes, vector<int>& leaves, int & counter_classes, vector<int>& encoding) {    
    
    
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


vector<int> fill_equivalence_classes (vector<vector<int> >& matr, vector<int>& encoding) {
  int counter_classes = 1;
  vector<int> equivalence_classes(matr.size());
  vector<int> leaves = find_leaves(matr, encoding);  

  vector<int> heights(matr.size());
  find_heights(matr, heights, 0);
  vector<vector<int> > llevels = level_divider(matr, heights); 

  fill_leaves_classes(matr.size(), equivalence_classes, leaves, counter_classes, encoding);
  
  int height_of_root = llevels.size() - 1;    
  vector<vector<int> > tuples;
  
  for (int level = 1; level < height_of_root + 1; ++level) {
    tuples.clear();
    tuples.resize(llevels[level].size());
    for (int vert_in_level = 0; vert_in_level < llevels[level].size(); ++vert_in_level ) {
      for (int adj_s = 0; adj_s < matr[llevels[level][vert_in_level]].size(); ++adj_s) {
        tuples[vert_in_level].push_back(equivalence_classes[matr[llevels[level][vert_in_level]][adj_s]]);
      }
      sort(tuples[vert_in_level].begin(), tuples[vert_in_level].end());
      tuples[vert_in_level].push_back(encoding[llevels[level][vert_in_level]]);
    }

    vector<pair< vector<int>, int> > vertex_vs_tuples(llevels[level].size());
    for (int i = 0; i < llevels[level].size(); ++i) {
      vertex_vs_tuples[i] = make_pair(tuples[i], llevels[level][i]);
    }
    sort(vertex_vs_tuples.begin(), vertex_vs_tuples.end());

    equivalence_classes[vertex_vs_tuples[0].second] = counter_classes;
    for (int i = 1; i < llevels[level].size(); ++i) {
      if (vertex_vs_tuples[i - 1].first == vertex_vs_tuples[i].first) {
        equivalence_classes[vertex_vs_tuples[i].second] = counter_classes;
      } else {
        counter_classes++;
        equivalence_classes[vertex_vs_tuples[i].second] = counter_classes;
      }
    }
    counter_classes++;
  }
  
  return equivalence_classes;
}

