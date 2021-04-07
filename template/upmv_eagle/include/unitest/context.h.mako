#ifndef INCLUDE_unitest_context_H
#define INCLUDE_unitest_context_H

#ifndef _INCLUDE_SCADE_TYPES
	#include "scade_types.h"
#endif

#ifndef _INCLUDE_${node_name}
	#include "${node_name}.h"
#endif

#include "scade/${node_name}_extern.h"

extern _C_${node_name} unitest_context;

int unitest_init(_C_${node_name} * _C_) ;
int unitest_loop(_C_${node_name} * _C_) ;

#endif /* INCLUDE_unitest_context_H */