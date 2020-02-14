/*$************* SCADE_KCG KCG Version 5.1.1 (build i10) **************
** Command :
** l2C        autopilot.lus -node q_traj2_bang
**     -noexp @ALL@
**     -keep_named_var
**     -const
**     -name_length 63
**     -loc_ctx
**     -split
**     -no_copy_mem
**     -debug
** date of generation (MM/DD/YYYY): 05/16/2019 16:59:03
** last modification date for autopilot.lus (MM/DD/YYYY): 05/16/2019 
********************************************************************$*/

#include "scade_types.h"

#include "q_traj2_bang_extern.h"

#include "math.h"

/*$************************************** 
NAME : q_Traj2_bang_
INPUTS :
spd_delta : real
jrk_lim : real
OUPUTS :
jrk_cmd : real
***************************************$*/

void q_Traj2_bang_ (real spd_delta, real acc_cur, real jrk_lim, real * jrk_cmd) {
   
   real c = fabsf(spd_delta);
   real b = 0.5 * jrk_lim * R_Period * R_Period;
   real d = (b * b) + (4 * b * c);
   real x = (sqrtf(d) - b) / (2 * b);
   real n = floorf(x);
   real g = (c - (b * n * (n+1))) / ((n+1) * R_Period);
   real f = (n * jrk_lim * R_Period) + g;
   real w = copysignf(f, spd_delta);
   real q = (w - acc_cur) / R_Period;
   
   (* jrk_cmd) = q;
   
}


/*$************* SCADE_KCG KCG Version 5.1.1 (build i10) **************
** End of file q_Traj2_bang__fctext.dc
** End of generation (MM/DD/YYYY) : 05/16/2019 16:59:03
********************************************************************$*/
