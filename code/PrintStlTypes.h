/*

Provides functions for printing basic STL types : 

    vector<int>
    vector<pair<int, int> >

Author: Kulunchakov Andrei
*/

#include "mex.h"
#include <math.h>
#include <stdlib.h>
#include <vector>
#include <utility>
#include <stdio.h>

using namespace std;  

void vprintf( const vector<int>& a ) {
    for (int i = 0; i < a.size(); i++) {
        std::cout << a[i] << " ";
    }
    std::cout << "\n";
}


void pvprint(const vector<pair<int, int> >& a) {
    for(int i = 0; i < a.size(); ++i) {
      std::cout << a[i].first << " " << a[i].second << "\n";
    }
    std::cout << "\n";
    return;
}

void nprint(int a) {
    std::cout << a << "\n";
    return;
}