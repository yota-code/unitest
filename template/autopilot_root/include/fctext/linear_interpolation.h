#ifndef INCLUDE_fctext_linear_interpolation_H
#define INCLUDE_fctext_linear_interpolation_H

#include "fctext/config_types.h"

typedef real lint20_array_20_T[20];

typedef struct {
	real _F0;
	real _F1;
	real _F2;
	real _F3;
	real _F4;
	real _F5;
	real _F6;
	real _F7;
	real _F8;
	real _F9;
	real _F10;
	real _F11;
	real _F12;
	real _F13;
	real _F14;
	real _F15;
	real _F16;
	real _F17;
	real _F18;
	real _F19;
} lint20_struct_20_T;

typedef union {
	lint20_array_20_T m_array;
	lint20_struct_20_T m_struct;
} lint20_union_20_T;

typedef struct {
	lint20_union_20_T m_x;
	lint20_union_20_T m_y;
	_int count;
} lint20_C;

extern real lint20(lint20_C * self, real x);

#endif
