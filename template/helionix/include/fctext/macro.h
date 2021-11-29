#ifndef INCLUDE_fctext_macro_H
#define INCLUDE_fctext_macro_H

#include <math.h>

#ifndef m_SAOsqrt
// extern void SAOsqrt(real The_Input, real * The_Output);
#define m_SAOsqrt(The_Input, The_Output) { The_Output = sqrtf(The_Input); }
#endif /* m_SAOsqrt */

#ifndef m_SAOasind
// extern void SAOasind(real The_Input, real * The_Output);
#define m_SAOasind(The_Input,The_Output) { The_Output  = 180.0 * asinf( The_Input ) / M_PI ; }
#endif /* m_SAOasind */

#ifndef m_SAOsind
// extern void SAOsind(real The_Input, real * The_Output);
#define m_SAOsind(The_Input,The_Output) { The_Output  = sinf( The_Input * M_PI /180 ); }
#endif /* m_SAOsind */

#endif /* INCLUDE_fctext_macro_H */
