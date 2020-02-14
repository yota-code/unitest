#ifndef INCLUDE_fctext_bool_packing_H
#define INCLUDE_fctext_bool_packing_H

#include "fctext/config_types.h"

typedef struct {
	
	bool b1 ;
	bool b2 ;
	bool b3 ;
	bool b4 ;
	bool b5 ;
	bool b6 ;
	bool b7 ;
	bool b8 ;
	bool b9 ;
	bool b10;
	bool b11;
	bool b12;
	bool b13;
	bool b14;
	bool b15;
	bool b16;
	bool b17;
	bool b18;
	bool b19;
	bool b20;
	bool b21;
	bool b22;
	bool b23;
	bool b24;
	bool b25;
	bool b26;
	bool b27;
	bool b28;
	bool b29;
	bool b30;
	bool b31;
	bool b32;

} S_32bool_T;

extern void bool32_to_uint(const S_32bool_T * S_32bool, _int * I_CompactBool) ;

#endif