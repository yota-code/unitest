#ifndef INCLUDE_fctext_macro_H
#define INCLUDE_fctext_macro_H

#include <math.h>

#ifndef m_SAOsqrt
// extern void SAOsqrt(real The_Input, real * The_Output);
#define m_SAOsqrt(The_Input, The_Output) { The_Output = sqrtf(The_Input); }
#endif /* m_SAOsqrt */

#endif /* INCLUDE_fctext_macro_H */
