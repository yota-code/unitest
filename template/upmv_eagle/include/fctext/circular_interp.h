#ifndef INCLUDE_fctext_circular_interp_H
#define INCLUDE_fctext_circular_interp_H

#include <inttypes.h>

#ifndef _INCLUDE_SCADE_TYPES
	#include "scade_types.h"
#endif

#define circular_interp_SIZE (5)

/*

	i = 0 dernier échantillon inséré
   i = 1 avant dernier échantillon
   i = -1 plus vieil échantillon
*/

#define circular_interp_SHIFT(self, i) (\
	( ( ( ((int)((self)->p_write + i)) % circular_interp_SIZE) + circular_interp_SIZE ) % circular_interp_SIZE ) \
)
#define circular_interp_AT(self, i) ( (self)->buffer[ circular_interp_SHIFT(self, i) ] )

typedef struct {
	Vec3 value;
	uint64_t time; // as integer in µs
} circular_interp_element_T;

typedef struct {
	circular_interp_element_T buffer[circular_interp_SIZE];
	size_t p_write;
} circular_interp_T;

void circular_interp__init__(circular_interp_T * self);
void circular_interp_push(circular_interp_T * self, int time, Vec3 * value);
int circular_interp_get(circular_interp_T * self, int time, Vec3 * value);
void circular_interp__debug__(circular_interp_T * self, int timeToInterp);

#ifdef NDEBUG
	#define circular_interp_DEBUG(self, time)
#else
	#define circular_interp_DEBUG(self, time) ( circular_interp__debug__(self, time) )
#endif

#endif /* INCLUDE_fctext_circular_interp_H */