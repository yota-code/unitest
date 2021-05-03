
#include "fctext/config_types.h"
#include "scade/model_extern.h"

#include "fctext/math_lib.h"
#include "fctext/signal_lib.h"

// #include <stdio.h>

#define period_ms ((real)(80))

const real T_CYCLE = period_ms / 1000.0 ;
const real F_CYCLE = 1000.0 / period_ms ;

int s_tbX_average(real * cmd_lst, real * dur_lst, real jm, size_t n, real * average) {

	real t = 0.0;
	real j = 0.0;

	for (size_t i=0 ; i<n ; i++) {
		real cmd = cmd_lst[i];
		real dur = dur_lst[i];
		if ( (t + dur) <= T_CYCLE ) {
			j += cmd * dur;
		} else {
			j += cmd * m_BOUND((T_CYCLE - t), 0.0, T_CYCLE);
		}
		t += dur;
	}

	(* average) = j * F_CYCLE * jm;

	return EXIT_SUCCESS;

}

int s_tbX_total(real * cmd_lst, real * dur_lst, real jm, real a0, real s0, size_t n, real * duration, real * distance) {

	real a_prev = 0.0;
	real s_prev = 0.0;
	real d_prev = 0.0;

	real a = 0.0;
	real s = 0.0;
	real d = 0.0;

	(* duration) = 0.0;

	// printf("\n---  cmd // [");
	// for (size_t i=0 ; i<n ; i++) {
	// 	printf("%f, ", cmd_lst[i]);
	// }
	// printf("]\n---  dur // [");
	// for (size_t i=0 ; i<n ; i++) {
	// 	printf("%f, ", dur_lst[i]);
	// }
	// printf("]\n");


	for (size_t i=0 ; i<n ; i++) {
		real t = dur_lst[i];
		real j = cmd_lst[i] * jm;

		(* duration) += t;

		a = a_prev + j*t;
		s = s_prev + a_prev*t + j*t*t/2.0;
		d = d_prev + s_prev*t + a_prev*t*t/2.0 + j*t*t*t/6.0;

		// printf("%ld :: t=%f j=%f a=%f s=%f d=%f\n", i, t, j, a, s, d);

		a_prev = a;
		s_prev = s;
		d_prev = d;

	}

	(* distance) = d;

	return EXIT_SUCCESS;

}


real s_tbX_duration(real * cmd_lst, real * dur_lst, size_t n) {

	real total_duration = 0.0;

	for (size_t i=0 ; i<n ; i++) {
		total_duration += dur_lst[i];
	}

	return total_duration;

}