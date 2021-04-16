#ifndef INCLUDE_fctext_config_types_H
#define INCLUDE_fctext_config_types_H

#include <stdlib.h>
#include <inttypes.h>
#include <limits.h>

#ifdef SCADE_64BIT_INT
	typedef int64_t _int;

	#define SCADE_INT_MIN LLONG_MIN
	#define SCADE_INT_MAX LLONG_MAX

#else
	typedef int32_t _int;

	#define SCADE_INT_MIN INT_MIN
	#define SCADE_INT_MAX INT_MAX
#endif

typedef int32_t bool;

#ifdef SCADE_64BIT_REAL

	#define SCADE_REAL_MIN DBL_MIN
	#define SCADE_REAL_MAX DBL_MAX

	typedef double real;
#else

	#define SCADE_REAL_MIN FLT_MIN
	#define SCADE_REAL_MAX FLT_MAX

	typedef float real;
#endif

#define false (0)
#define true (1)

#endif /* INCLUDE_fctext_config_types_H */
