/**********************************************************************
** Copyright Eurocopter France 2010
** Author : F. RUYSSEN
** Date of creation : 29/05/2009
** Module name : lint1
** Description : Linear interpolation 1 input
** Requirements : LLR-LINT1-001
**                LLR-LINT1-002 
***********************************************************************
** History of modification :
** 
***********************************************************************/

#ifndef _AFCS_LINT1_H
#define _AFCS_LINT1_H

/* Includes */
#ifndef _INCLUDE_SCADE_TYPES
#include "scade_types.h"
#endif

#define _INCLUDE_lint1
#define C_int_pol_vec_size 20

/* ============== */
/*  CONTEXT TYPE  */
/* ============== */
typedef struct {
real 	_I0_The_Input;
table1 	*_I1_The_Table;
real 	_O0_The_Output;
/* Memories */
_int 	Last_Index;
} _C_lint1;

/* ============== */
/* INITIALISATION */
/* ============== */
extern void lint1_init (_C_lint1 *lint1Struct);


/* =============== */
/* CYCLIC FUNCTION */
/* =============== */
/*  Linear interpolation extract */
extern void lint1 (_C_lint1 *lint1Struct);

#endif
