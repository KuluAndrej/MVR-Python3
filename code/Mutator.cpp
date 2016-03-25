#include <iostream>
#include "create_data_by_handle.h"
#include "print_operations.h"
#include <boost/python/def.hpp>
#include <boost/python/module.hpp>

using namespace std;
namespace bp = boost::python;


char const* Solve(const char* handle) {

  pair<vector<vector<int> >, vector<int> > info_handle;
  pair<map<string, int>, int> tokens_info = read_info_primitives ();

  map<string, int> map_tokens = tokens_info.first;
  info_handle = create_incid_matrix_tokens(map_tokens, handle);
  vector<vector<int> > incidence_matrix = info_handle.first;
    vprintf(info_handle.second);
    char encodings[incidence_matrix.size()];
    for (int i = 0 ; i < info_handle.second.size(); i++) {
        encodings[i] = '0' + info_handle.second[i];
    }

    return encodings;
}

BOOST_PYTHON_MODULE(reconstructer) {
    bp::def("say_greeting", Solve);
}
