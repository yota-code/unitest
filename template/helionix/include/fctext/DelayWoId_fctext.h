/**********************************************************************
** Copyright Eurocopter France 2009                                  
** Author : F. RUYSSEN
** Date of creation : 25/05/2009
** Module name : DelayWoId
** Description : Applies a DelayWoId of Time_constant/Time_period cycle on the input
** Requirements : LLR-DELAYWOID-001
**				  LLR-DELAYWOID-002                  
***********************************************************************
** History of modification :
** 
************************************************************************/


#ifndef _INCLUDE_DelayWoId
#define _INCLUDE_DelayWoId

#define C_sample_number  60
/* 60  is the optimum value for better execution speed of code generated in this case  */
/* because the size of the structure = 64 ie LSL 8   */
/* for calculating the displacement in DelayWoId_data  */

/* Includes */
#include "config_types.h"

/* Local Types: */

typedef struct {
	_int position_out;
	_int position_in;
	real sample[C_sample_number];
	real time_constant_p;
	bool first_run;
	_int DelayWoId_param_out_of_ranges;
} 
DelayWoId_data_T;

/* ============== */
/*  CONTEXT TYPE  */
/* ============== */
typedef struct {
	real _I0_Input;
	real _I1_Time_constant;
	bool _I2_Re_init;
	real _I3_Time_Period;
	real _I4_Output_Option;
	real _O0_Output;
	/* Memories */
	DelayWoId_data_T DelayWoId_data;
} _C_DelayWoId;

/* ============== */
/* INITIALISATION */
/* ============== */
extern void DelayWoId_init (_C_DelayWoId *DelayStruct);

/* =============== */
/* CYCLIC FUNCTION */
/* =============== */
extern int DelayWoId (_C_DelayWoId *DelayStruct);

#endif
