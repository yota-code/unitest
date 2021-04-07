#include <stdlib.h>
#include <string.h>

#ifndef NDEBUG
	#include <stdio.h>

	#define dbg(...) printf(__VA_ARGS__)
#else
	#define dbg(...)
#endif

#include "fctext/circular_interp.h"

void circular_interp__init__(circular_interp_T * self) {

	memset(self, 0, sizeof(circular_interp_T));

	//circular_interp_DEBUG(self, 0);

}

void circular_interp_push(circular_interp_T * self, int time, Vec3 * value) {

	self->p_write = circular_interp_SHIFT(self, -1);

	circular_interp_AT(self, 0).time = time;
	circular_interp_AT(self, 0).value = * value;

	//circular_interp_DEBUG(self, time);

}

int circular_interp_get(circular_interp_T * self, int time, Vec3 * value) {

	dbg(">>> circular_interp_get(<%p>, %d, {?, ?, ?})\n", (void *) self, time);

	int t_before = circular_interp_AT(self, -1).time;
	int t_after = circular_interp_AT(self, 0).time;
	// printf("TOTAL t= %d <= %d <= %d KO\n", t_before, time, t_after);

	if (! ( (t_before <= time) && (time <= t_after) )) {
		// la valeur time demandée n'est même pas dans le range total du buffer circulaire
		return EXIT_FAILURE;
	}

	for ( size_t i=0 ; i<circular_interp_SIZE ; i++ ) {
		
		t_before = circular_interp_AT(self, i+1).time;

		if ( (t_before <= time) && (time <= t_after) ) {
			// printf("\tINTERVAL t= %d <= %d <%d OK\n", t_before, time, t_after);
			for ( size_t n=0 ; n<3 ; n++ ) {

				float v_before = ((real *)(&(circular_interp_AT(self, i).value)))[n];
				float v_after = ((real *)(&(circular_interp_AT(self, i+1).value)))[n];

				real v_interp = ((real)(time - t_before)) * ((v_after - v_before) / (real)(t_after - t_before)) + v_before;

				((real *)(value))[n] = v_interp;
				// printf("\t %ld: v_before=%f v_after=%f v_interp=%f\n", n, v_before, v_after, v_interp);

			}

			return EXIT_SUCCESS;
		} else {
			// printf("\tINTERVAL t= %d <= %d <%d KO\n", t_before, time, t_after);
		}

		t_after = t_before;
	}

	// aucun intervale ne semble répondre au problème
	return EXIT_FAILURE;
}


#ifndef NDEBUG

	void circular_interp__debug__(circular_interp_T * self, int time) {

		printf("--------\n");

		printf("+p =");
		int p_index[circular_interp_SIZE] = {0};
		for (int i=0 ; i<circular_interp_SIZE ; i++) {
			p_index[circular_interp_SHIFT(self, i)] = i;
		}
		for (int i=0 ; i<circular_interp_SIZE ; i++) {
			printf("%12d", p_index[i]);;
		}
		printf("\n");

		printf("-p =");
		int q_index[circular_interp_SIZE] = {0};
		for (int i=0 ; i<circular_interp_SIZE ; i++) {
			q_index[circular_interp_SHIFT(self, -i)] = -i;
		}
		for (int i=0 ; i<circular_interp_SIZE ; i++) {
			printf("%12d", q_index[i]);;
		}
		printf("\n");

		printf("t  =");
		for (int i=0 ; i<circular_interp_SIZE ; i++) {
			printf("%12ld", self->buffer[i].time);
		}
		printf("\n");

		for (int j=0 ; j<3 ; j++) {
			printf("v%d =", j);
			for (int i=0 ; i<circular_interp_SIZE ; i++) {
				printf("%12.3f", ((real *)(&( self->buffer[i].value)))[j]);
			}
			printf("\n");
		}

	}

#endif


#ifdef AUTOTEST

/*
gcc -DAUTOTEST -std=gnu99 -save-temps -I../../include -I../../include/fctext -I../../include/scade circular_interp.c -o circular_interp.exe && ./circular_interp.exe
*/

int main() {
	circular_interp_T u;
	circular_interp__init__(&u);

	Vec3 vr = {0.0, 0.0, 0.0};

	Vec3 va = {1.0, 2.0, 3.0};
	Vec3 vb = {2.0, 2.0, 2.0};
	Vec3 vc = {3.0, 2.0, 1.0};
	Vec3 vd = {4.0, 2.0, 0.0};
	Vec3 ve = {5.0, 2.0, -1.0};
	Vec3 vf = {6.0, 2.0, -2.0};

	circular_interp_push(&u, 42, & va);
	circular_interp_push(&u, 63, & vb);

	circular_interp_get(&u, 50, & vr);

	circular_interp_push(&u, 81, & vc);
	circular_interp_push(&u, 104, & vd);
	circular_interp_push(&u, 132, & ve);
	circular_interp_push(&u, 147, & vf);

	circular_interp_get(&u, 111, & vr);

}

#endif
