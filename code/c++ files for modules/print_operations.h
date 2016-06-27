#include "mex.h"
#include <math.h>
#include <stdlib.h>
#include <vector>
#include <utility>
#include <stdio.h>

using namespace std;  

void vprint(const vector<int>& a) {
    for(int i = 0; i < a.size(); ++i) {
      mexPrintf("%d ", a[i]);
    }
    mexPrintf("\n");
    return;
}

void sprint(const string& s) {
    mexPrintf("%s\n", s.c_str());
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