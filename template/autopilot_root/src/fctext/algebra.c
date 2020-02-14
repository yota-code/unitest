#include "fctext/algebra.h"

int algebra_matrix_product(
	size_t app_row, size_t app_col, size_t input_col,
	real * m_input, real * m_app, real * m_output
) {
	for (size_t r=0 ; r < app_row ; r++) {
		for (size_t c=0 ; c < input_col ; c++) {
			float s = 0.0;
			for (size_t i=0 ; i < app_col ; i++) {
				s += m_app[r * app_col + i] * m_input[i * input_col + c];
			}
			m_output[r * input_col + c] = s;
		}
	}
	return EXIT_SUCCESS;
}

int algebra_vector_minmax(size_t n_item, real * I0_input, real * O0_max, real * O1_min) {
	real r_min = 0.0;
	real r_max = 0.0;
	for (size_t i=0 ; i<n_item ; i++) {
		if (i == 0) {
			r_min = I0_input[i];
			r_max = I0_input[i];
		} else {
			r_min = (I0_input[i] < r_min) ? (I0_input[i]) : (r_min);
			r_max = (I0_input[i] > r_max) ? (I0_input[i]) : (r_max);
		}
	}
	* O0_max = r_max;
	* O1_min = r_min;
	return EXIT_SUCCESS;
}