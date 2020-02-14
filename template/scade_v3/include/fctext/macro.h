#include <math.h>

#ifndef m_Kalman_3s4o
extern void Kalman_3s4o (const S_3x3Mx_T * Pprv, const S_3x3Mx_T * F, const S_4x3Mx_T * H, const S_3x3Mx_T * Q, const S_4x4Mx_T * R, bool B_OL, S_3x4Mx_T * K, S_3x3Mx_T * P, bool * B_Singular);
#define m_Kalman_3s4o(Pprv,F,H,Q,R,B_OL,K,P,B_Singular) ( Kalman_3s4o (  &Pprv, &F, &H, &Q, &R,B_OL,&K,&P,&B_Singular ) ) 
#endif /* m_Kalman_3s4o */

#ifndef m_SAOatan
#define m_SAOatan(The_Input, The_Output) ( The_Output = tanf( The_Input ) ) 
#endif /* m_SAOatan */

#ifndef m_SAOsqrt
#define m_SAOsqrt(The_Input, The_Output) ( The_Output = sqrtf( The_Input ) ) 
#endif /* m_SAOsqrt */

#ifndef m_SAOcos
#define m_SAOcos(The_Input, The_Output) ( The_Output = cosf( The_Input ) ) 
#endif /* m_SAOcos */

#ifndef m_SAOsin
#define m_SAOsin(The_Input, The_Output) ( The_Output = sinf( The_Input ) ) 
#endif /* m_SAOsin */
