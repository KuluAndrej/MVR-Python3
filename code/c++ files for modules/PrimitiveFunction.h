/*

Structure storing all necessary info about a primitive function

Author: Kulunchakov Andrei
*/

#include <string>

struct PrimitiveFunction {
    std::string name;
    int numberParameters;
    int numberArguments;
    string initParams;
    string boundsParams;

    
    PrimitiveFunction& operator =(const PrimitiveFunction& a) {
	    name = a.name;
	    numberParameters = a.numberParameters;
	    numberArguments  = a.numberArguments;
	    initParams 		 = a.initParams;
	    boundsParams     = a.boundsParams;
    return *this;
}
};

