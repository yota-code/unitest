#ifndef INCLUDE_fctext_math_lib_H
#define INCLUDE_fctext_math_lib_H

#include <math.h>

#ifndef _INCLUDE_SCADE_TYPES
	#include "scade_types.h"
#endif

#define m_BOUND_UP(x, upper_bound) ( ((upper_bound < x) ? (upper_bound) : (x)) )
#define m_BOUND_LOW(x, lower_bound) ( ((x < lower_bound) ? (lower_bound) : (x)) )

#define m_BOUND(x, lower_bound, upper_bound) ( \
	(lower_bound <= upper_bound) ? ( \
		m_BOUND_LOW( m_BOUND_UP(x, upper_bound), lower_bound ) \
	) : ((lower_bound + upper_bound) / 2.0) \
)

#define m_m_bound_up(x, upper_bound, y) { y = m_BOUND_UP(x, upper_bound); }
#define m_m_bound_low(x, lower_bound, y) { y = m_BOUND_LOW(x, lower_bound); }
#define m_m_bound(x, lower_bound, upper_bound, y) { y = m_BOUND(x, lower_bound, upper_bound); }
#define m_m_bound_S(x, symetric_bound, y) { y = m_BOUND(x, -symetric_bound, symetric_bound); }
#define m_m_bound_Z_sym(x, symetric_bound, y) { y = m_BOUND(x, -symetric_bound, symetric_bound); }

#define m_MOD_N(a, m) (((a % m) < 0) ? ((a % m) + m) : (a % m))
#define m_m_mod_N(a, m, n) { n = m_MOD_N(a, m); }

#ifdef SCADE_64BIT_INT
	#define m_m_abs_z(x, abs_x) { abs_x = labs(x); }
#else
	#define m_m_abs_z(x, abs_x) { abs_x = abs(x); }
#endif

#define m_m_bw_and(a, b, a_and_b) { a_and_b = ((a) & (b)); }
#define m_m_bw_or(a, b, a_or_b) { a_or_b = ((a) | (b)); }
#define m_m_bw_xor(a, b, a_xor_b) { a_xor_b = ((a) ^ (b)); }

#define m_m_istrue(input, output) { output = ((input) != 0); }

#ifdef SCADE_64BIT_REAL

	#define m_m_abs_r(x, abs_x) { abs_x = fabs(x); }
	#define m_m_sqrt(x, sqrt_x) { sqrt_x = sqrt(x); }

	#define m_m_cos(a, cos_a) { cos_a = cos(a); }
	#define m_m_acos(x, acos_x) { acos_x = acos(x); }
	#define m_m_sin(a, sin_a) { sin_a = sin(a); }
	#define m_m_asin(x, asin_x) { asin_x = asin(x); }
	#define m_m_tan(a, tan_a) { tan_a = tan(a); }
	#define m_m_atan(x, atan_x) { atan_x = atan(x); }

	#define m_m_atan2(y, x, atan2_y_x) { atan2_y_x = atan2(y, x); }

	#define m_m_sincos(a, sin_a, cos_a) { \
		sin_a = sin(a); \
		cos_a = cos(a); \
	}

	#define m_m_copysign(m, s, y) { y = copysign(m, s); }

	#define m_m_ceil(x, n) { n = (_int)( m_BOUND(ceil(x), SCADE_INT_MIN, SCADE_INT_MAX) ); }
	#define m_m_floor(x, n) { n = (_int)( m_BOUND(floor(x), SCADE_INT_MIN, SCADE_INT_MAX) ); }
	#define m_m_round(x, n) { n = (_int)( m_BOUND(round(x), SCADE_INT_MIN, SCADE_INT_MAX) ); }

	#define m_m_mod_R(a, m, n) { n = (_int)( fmod(a, m) ); }

#else

	#define m_m_abs_r(x, abs_x) { abs_x = fabsf(x); }
	#define m_m_sqrt(x, sqrt_x) { sqrt_x = sqrtf(x); }

	#define m_m_cos(a, cos_a) { cos_a = cosf(a); }
	#define m_m_acos(x, acos_x) { acos_x = acosf(x); }
	#define m_m_sin(a, sin_a) { sin_a = sinf(a); }
	#define m_m_asin(x, asin_x) { asin_x = asinf(x); }
	#define m_m_tan(a, tan_a) { tan_a = tanf(a); }
	#define m_m_atan(x, atan_x) { atan_x = atanf(x); }

	#define m_m_atan2(y, x, atan2_y_x) { atan2_y_x = atan2f(y, x); }

	#define m_m_sincos(a, sin_a, cos_a) { \
		sin_a = sinf(a); \
		cos_a = cosf(a); \
	}

	#define m_m_copysign(m, s, y) { y = copysignf(m, s); }

	#define m_m_ceil(x, n) { n = (_int)( m_BOUND(ceilf(x), SCADE_INT_MIN, SCADE_INT_MAX) ); }
	#define m_m_floor(x, n) { n = (_int)( m_BOUND(floorf(x), SCADE_INT_MIN, SCADE_INT_MAX) ); }
	#define m_m_round(x, n) { n = (_int)( m_BOUND(roundf(x), SCADE_INT_MIN, SCADE_INT_MAX) ); }

	#define m_m_mod_R(a, m, n) { n = (_int)( fmodf(a, m) ); }
#endif

#define m_m_div_zero(a, b, r) ( r = ( (b == 0.0) ? ((a >= 0) ? (INFINITY) : (-INFINITY)) : (a / b) ))

#define m_REAL_TO_BAM(x) ((_int)(((int64_t)((real)(x))) & 0xFFFFFFFF))
#define m_BAM_TO_REAL(b) ((real)(b))

#define m_BAM_TO_DEG ( ((double)(90.0)) / ((double)(1 << 30)) )
#define m_DEG_TO_BAM ( ((double)(1 << 30)) / ((double)(90.0)) )

#define m_BAM_TO_RAD ( ((double)(M_PI_2)) / ((double)(1 << 30)) )
#define m_RAD_TO_BAM ( ((double)(1 << 30)) / ((double)(M_PI_2)) )

#define m_RAD_TO_DEG ( ((double)(90.0)) / ((double)(M_PI_2)) )
#define m_DEG_TO_RAD ( ((double)(M_PI_2)) / ((double)(90.0)) )

#define m_m_bam_to_deg_U(bam, deg) { deg = m_BAM_TO_REAL((uint32_t)(bam)) * m_BAM_TO_DEG; }
#define m_m_bam_to_deg_S(bam, deg) { deg = m_BAM_TO_REAL((int32_t)(bam)) * m_BAM_TO_DEG; }
#define m_m_deg_to_bam(deg, bam) { bam = m_REAL_TO_BAM((deg) * m_DEG_TO_BAM); }

#define m_m_bam_to_rad_U(bam, rad) { rad = m_BAM_TO_REAL((uint32_t)(bam)) * m_BAM_TO_RAD; }
#define m_m_bam_to_rad_S(bam, rad) { rad = m_BAM_TO_REAL((int32_t)(bam)) * m_BAM_TO_RAD; }
#define m_m_rad_to_bam(rad, bam) { bam = m_REAL_TO_BAM((rad) * m_RAD_TO_BAM); }

#define m_m_deg_to_rad(deg, rad) ( rad = ( deg * m_DEG_TO_RAD ) ) 
#define m_m_rad_to_deg(rad, deg) ( deg = ( rad * m_RAD_TO_DEG ) )

#endif /* INCLUDE_fctext_math_lib_H */