#ifndef _INCLUDE_SCADE_TYPES
	#include "scade/scade_types.h"
#endif

upmv_Z_T default_loop = {0};
wsk_segment_status_S wsk_segment_sta__default__ = {0};

real C_lon_spd_cruise = (real) 32.0;

bool D_lat_psi_is_wind_correction_active = true;

real D_lat_psi_fdb_gain = 1.0;
real D_lat_psi_dtk_gain = 1.0;
real D_lat_psi_xtk_gain = 1.0;

avidyne_abs_nav_out S_EmiNavMgt_ini = {0};