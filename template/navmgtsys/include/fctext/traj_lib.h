#ifndef INCLUDE_traj_lib_H
#define INCLUDE_traj_lib_H

#include "traj_lib_tb3.h"

#define m_t_tb3_distance(tb3_obj, distance) { distance = ( (tb3_C *)(& (tb3_obj)) )->poly.p[8][3]; }
#define m_t_tb3_duration(tb3_obj, duration) { duration = ( (tb3_C *)(& (tb3_obj)) )->poly.t[7]; }

#define m_t_tb3_spd_at_pos(pos, tb3_obj, spd) ( tb3_spd_at_pos((tb3_C *)(& (tb3_obj)), pos, & spd) )
#define m_t_tb3_at_time(t, tb3_obj, spd, acc, jrk) ( tb3_at_time((tb3_C *)(& (tb3_obj)), t, & spd, & acc, & jrk) )

#endif /* INCLUDE_traj_lib_H */