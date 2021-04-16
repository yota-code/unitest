#ifndef INCLUDE_fctext_arinc_H
#define INCLUDE_fctext_arinc_H

/*
the data or the word must be cast to the proper signedness before calling ARINC_INSERT or ARINC_EXTRACT.

ie:
* sign bit -> cast with (int32_t)
* no sign bit -> cast with (unsigned int)

if in float, eng_data must be converted first to int, lsb value wise,
ARINC_INSERT expect an int/uint value

pos: the lowest bit number of the data in the arinc datagram
size: the total size of the data, including the sign

ex:
insert a 12 bit long (including the sign) signed integer 'data' into 'word'
starting at bit 14:

	word |= ARINC_INSERT((int32_t) (data), 14, 12);

insert a boolean 'bool' into 'word' at bit 17:

	word |= ARINC_INSERT((uint32_t) (bool), 17, 1);
  
insert a 16 bit long float 'data' of low significant value 'lsb' into 'word'
starting at bit 11:

	word |= ARINC_INSERT((int32_t) (data * lsb), 11, 16);
	
*/

#define ARINC_INSERT(data, pos, size) \
	((((data) << (32 - (size))) >> (33 - (size) - (pos))) & (((1 << (size)) - 1) << ((pos) - 1)))

#define ARINC_EXTRACT(word, pos, size) \
	((((word) & (((1 << (size)) - 1) << ((pos) - 1))) << (33 - (size) - (pos))) >> (32 - (size)))

#define ARINC_GET_SSM(word) ((int)(((uint32_t)((word) & 0x60000000)) >> 29))
#define ARINC_GET_VALIDITY(word) (((int) ((word) & 0x80000000)) != 0 )

#endif /* INCLUDE_fctext_arinc_H */

