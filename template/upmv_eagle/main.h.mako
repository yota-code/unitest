<%
import re
%>\
#ifndef INCLUDE_unitest_main_H
#define INCLUDE_unitest_main_H

#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>

#include "scade_types.h"
#include "${node_name}.h"

#include "unitest/interface.h"

int unitest_init(_C_${node_name} * _C_) ;
int unitest_loop(_C_${node_name} * _C_);

#endif /* INCLUDE_unitest_main_H */
