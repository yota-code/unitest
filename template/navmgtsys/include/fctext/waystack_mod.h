#ifndef INCLUDE_fctext_waystack_mod_H
#define INCLUDE_fctext_waystack_mod_H

#ifndef _INCLUDE_SCADE_TYPES
	#include "scade_types.h"
#endif

#include "fctext/math_lib.h"

#define WSK_loop_right_ROUTE

#ifdef WSK_loop_right_ROUTE
	#define wsk_qnd_line_LEN 8
#endif

#ifdef WSK_official_01_ROUTE
	#define wsk_qnd_line_LEN 22
#endif

extern _int wsk_qnd_line_cur;
extern _int wsk_qnd_line_len;

extern wsk_qnd_point_T wsk_qnd_line_arr[wsk_qnd_line_LEN];

#define m_wsk_qnd_get(n, point) { point = wsk_qnd_line_arr[m_MOD_N(wsk_qnd_line_cur + n, wsk_qnd_line_LEN)]; }

#define m_wsk_qnd_next(increment, n) { wsk_qnd_line_cur = m_MOD_N(wsk_qnd_line_cur + ((increment) ? (1) : (0)), wsk_qnd_line_LEN); n = wsk_qnd_line_cur; }

#define m_wsk_qnd_init(n) { wsk_qnd_line_cur = (n); } 

#endif /* INCLUDE_fctext_waystack_mod_H */
