#include "t_tb3_fctext.h"

int main(int argc, char * argv[]) {

	tb3_C u = {0};
	t_tb3_C c = {0};

	uint64_t c_zero = (uint64_t)(&c);
	uint64_t u_zero = (uint64_t)(&u);

	printf("sizeof(tb3_C) = %d\n", sizeof(tb3_C));
	printf("sizeof(_C_t_tb3) = %d\n", sizeof(t_tb3_C));

	printf("& c.poly = %d <--> & u.poly = %d\n", (uint64_t)(&(c.poly)) - c_zero, (uint64_t)(&(u.poly)) - u_zero);
	
	printf("& c.poly.a = %d <--> & u.poly.a = %d\n", (uint64_t)(&(c.poly.a)) - c_zero, (uint64_t)(&(u.poly.a)) - u_zero);
	printf("& c.poly.s = %d <--> & u.poly.s = %d\n", (uint64_t)(&(c.poly.s)) - c_zero, (uint64_t)(&(u.poly.s)) - u_zero);
	printf("& c.poly.p = %d <--> & u.poly.p = %d\n", (uint64_t)(&(c.poly.p)) - c_zero, (uint64_t)(&(u.poly.p)) - u_zero);

	#ifdef TUTU

	tb3__init__(&u, 1, 2);
	tb3_compute(&u, 0, 10, 0, 0);
	tb3_integrate(&u);

	tb3__print__(&u);

	// double f = 0.0;
	// sscanf(argv[1], "%lf", &f);

	for (int i=0 ; i<100 ; i++) {
		double s = 0;
		double p = (i / 2.0) - 10.0;
		tb3_solve_spd_at_pos(&u, p, &s);
		printf("%f\t%f\n", p, s);
	}
	// double s = 0;
	// tb3_solve_spd_at_pos(&u, f, &s);
	// printf("%f\n", s);

	#endif
}