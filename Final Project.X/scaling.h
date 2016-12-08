/* 
 * File:   scaling.h
 * Author: Peter
 */

#ifndef SCALING_H
#define	SCALING_H

#ifdef	__cplusplus
extern "C" {
#endif
	
/* Linearly Maps the float x from input space (i1,i2) to output space (o1,o2) */
float mapf(float x, float i1, float i2, float o1, float o2);
/* Truncates x to inclusive range defined by min and max */
float range(float x, float min, float max);

#ifdef	__cplusplus
}
#endif

#endif	/* SCALING_H */

