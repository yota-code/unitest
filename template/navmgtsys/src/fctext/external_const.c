#ifndef _INCLUDE_SCADE_TYPES
	#include "scade/scade_types.h"
#endif

const upmv_Z_T default_loop = {0};
const wsk_segment_status_S wsk_segment_sta__default__ = {0};

const real C_lon_spd_cruise = (real) 32.0;

const bool C_lat_psi_is_wind_correction_active = true;

const bool C_lat_psi_is_integral_mode = false;
const bool C_lat_phi_is_active_mode = false;

const real C_lat_psi_dtk_gain = (real) 0.10;
const real C_lat_psi_fdb_gain = (real) 20.0;
const real C_lat_psi_xtk_gain = (real) 0.05;

const real C_lat_psi_direct_dtk_gain = (real) 0.10;
const real C_lat_psi_direct_xtk_gain = (real) 0.25;
const real C_lat_psi_direct_integral_gain = (real) 0.25;
