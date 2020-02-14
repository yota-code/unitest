#include "linear_interpolation.h"

#ifdef UNITEST

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char * argv[]) {
	
	lint20_C table = {
		{0.0, 1.0, 2.0, 3.0, 5.0, 8.0, 13.0, 21.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
		{1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
		8
	};
	
	printf("%f :: %f\n", -4.0, lint20(& table, -4.0));
	printf("%f :: %f\n", 0.0, lint20(& table, 0.0));
	printf("%f :: %f\n", 3.5, lint20(& table, 3.5));
	printf("%f :: %f\n", 4.0, lint20(& table, 4.0));
	printf("%f :: %f\n", 4.5, lint20(& table, 4.5));
	printf("%f :: %f\n", 4.5, lint20(& table, 4.5));
	printf("%f :: %f\n", 17.0, lint20(& table, 17.0));
	printf("%f :: %f\n", 21.0, lint20(& table, 21.0));
	printf("%f :: %f\n", 24.0, lint20(& table, 24.0));
	
}

#endif

real lint20(lint20_C * self, real x) {

	_int count = self->count;

	if ( x < self->m_x.m_array[0] ) {
		// printf("underflow! %f < %f\n", x, self->m_x.m_array[0]);
		return self->m_y.m_array[0];
	}
	if ( self->m_x.m_array[count-1] <= x ) {
		// printf("overflow! %f <= %f\n", self->m_x.m_array[count-1], x);
		return self->m_y.m_array[count-1];
	}
	
	for (_int i=0 ; i <= count-1 ; i++) {
		real x_low = self->m_x.m_array[i];
		real x_high = self->m_x.m_array[i+1];
		if ( (x_low <= x) && (x < x_high) ) {
			real y_low = self->m_y.m_array[i];
			real y_high = self->m_y.m_array[i+1];
			
			return y_low + ((y_high - y_low) / (x_high - x_low) * (x - x_low));
		}
	}
	
	return 0.0;
	
}

