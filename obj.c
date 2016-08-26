#include <stdlib.h>
#include <stdio.h>



double f( double x)  {
	return( x * x );
}



int main( int argc, char** argv ) {
    if( argc != 2 ) {
		printf("Invalid number of arguments\n");
    }
    else {
		double val = f(atof(argv[1]));
		printf("%f\n", val);
    }

}
