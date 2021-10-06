#ifndef INCLUDE_fctext_signal_lib_H
#define INCLUDE_fctext_signal_lib_H

/*
int s_tbX_average(real * cmd_lst, real * dur_lst, real jm, size_t n, real * average);
int s_tbX_total(real * cmd_lst, real * dur_lst, real jm, real a0, real s0, size_t n, real * duration, real * distance);

real s_tbX_duration(real * cmd_lst, real * dur_lst, size_t n);

#define m_s_tb3_average(res, jm, average) ( s_tbX_average((real *) & res.cmd, (real *) & res.dur, jm, 8, (real *) & average) )
#define m_s_tb3_total(res, a0, s0, jm, duration, distance) ( s_tbX_total((real *) & res.cmd, (real *) & res.dur, jm, a0, s0, 8, (real *) & duration, (real *) & distance ) )

#define m_s_tb3_duration(result, duration) { duration = s_tbX_duration((real *) & result.cmd, (real *) & result.dur, 8); }
*/
#endif /* INCLUDE_fctext_signal_lib_H */