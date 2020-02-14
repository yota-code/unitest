#ifndef INCLUDE_fctext_macro_H
#define INCLUDE_fctext_macro_H

#include <math.h>

#include "fctext/algebra.h"

#ifndef m_COS
#define m_COS(x, y) (y = cosf(x * M_PI / 180.0))
#endif 

#ifndef m_SIN
#define m_SIN(x, y) (y = sinf(x * M_PI / 180.0))
#endif

#ifndef m_SAOsind
#define m_SAOsind(x, y) (y = sinf(x * M_PI / 180.0))
#endif

#ifndef m_SAOasind
#define m_SAOasind(x, y) (y = asinf(x) * 180.0 / M_PI)
#endif

#ifndef m_SAOcosd
#define m_SAOcosd(x, y) (y = cosf(x * M_PI / 180.0))
#endif

#ifndef m_SAOacosd
#define m_SAOacosd(x, y) (y = acosf(x) * 180.0 / M_PI )
#endif

#ifndef m_SAOtand
#define m_SAOtand(x, y) (y = tanf(x * M_PI / 180.0))
#endif

#ifndef m_SAOatand
#define m_SAOatand(x, y) (y = atanf(x) * 180.0 / M_PI )
#endif

#ifndef m_SAOsqrt
#define m_SAOsqrt(x, y) (y = sqrtf(x))
#endif

#ifndef m_LnR
#define m_LnR(x, y) (y = logf(x))
#endif

#ifndef m_ExpR
#define m_ExpR(x, y) (y = expf(x))
#endif

#ifndef m_SAOexp
#define m_SAOexp(x, y) (y = expf(x))
#endif

#ifndef m_LibBoolToInt
#include "bool_packing.h"
#define m_LibBoolToInt(S_32bool, I_CompactBool) ( I_CompactBool = bool_to_uint32(& S_32bool) )
#endif

#ifndef m_lint1
#include "linear_interpolation.h"
#define m_lint1(x, table, y) (y = lint20((lint20_C * ) & table, x))
#endif

#ifndef m_math_sincos
#define m_math_sincos(alpha, sin_alpha, cos_alpha) { \
	sin_alpha = sinf(alpha); \
	cos_alpha = cosf(alpha); \
}
#endif

/*$************************************** 
NAME : matrix_product_6x4x1
INPUTS :
input : vector_4_T
app : matrix_6x4_T
OUPUTS :
output : vector_6_T
***************************************$*/
#ifndef m_matrix_product_6x4x1
#define m_matrix_product_6x4x1(input, app, output) algebra_matrix_product(6, 4, 1, (real *) & input, (real *) & app, (real *) & output)
#endif

/*$************************************** 
NAME : vector_6_minmax
INPUTS :
I0_input : vector_6_T
OUPUTS :
O0_max : real
O1_min : real
***************************************$*/
#ifndef m_vector_6_minmax
#define m_vector_6_minmax(I0_input, O0_max, O1_min) algebra_vector_minmax(6, (real *) & I0_input, (real *) & O0_max, (real *) & O1_min)
#endif

/*$************************************** 
NAME : emi_pwm_x6
INPUTS :
I0_input : vector_6_T
OUPUTS : none.
***************************************$*/
#ifndef m_emi_pwm_6
#include "fctext/emi_pwm.h"
#define m_emi_pwm_6(I0_input) emi_pwm_6(& I0_input)
#endif

/*$************************************** 
NAME : q_Traj2_bang_
INPUTS :
spd_delta : real
acc_cur : real
jrk_lim : real
OUPUTS :
jrk_cmd : real
***************************************$*/
#ifndef m_q_Traj2_bang_
extern void q_Traj2_bang_ (real spd_delta, real acc_cur, real jrk_lim, real * jrk_cmd);
#define m_q_Traj2_bang_(spd_delta,acc_cur,jrk_lim,jrk_cmd) ( q_Traj2_bang_ ( spd_delta,acc_cur,jrk_lim,&jrk_cmd ) ) 
#endif /* m_q_Traj2_bang_ */


#endif /* INCLUDE_fctext_macro_H */
