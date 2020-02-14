#ifndef INCLUDE_fctext_algrebra_H
#define INCLUDE_fctext_algrebra_H

#include <stdlib.h>

#include "fctext/config_types.h"

int algebra_matrix_product(
	size_t app_row, size_t app_col, size_t input_col,
	real * m_input, real * m_app, real * m_output
);

int algebra_vector_minmax(size_t n_item, real * I0_input, real * O0_max, real * O1_min);

#endif