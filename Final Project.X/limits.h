/* 
 * File:   limits.h
 * Author: Peter
 */

#ifndef LIMITS_H
#define	LIMITS_H

#include "types.h"

#ifdef	__cplusplus
extern "C" {
#endif

/* Limits on Theta, degrees */
#define LIM_O_MIN (0.0)
#define LIM_O_MAX (200.0)

/* Limits on Radius, mm */
#define LIM_R_MIN (60.0)
#define LIM_R_MAX (160.0)
	
/* Limits on Elevation, mm */
#define LIM_Z_MIN (-30.0)
#define LIM_Z_MAX (50.0)

/* Limits on Claw Input, degrees */
#define LIM_C_MIN (0.0)
#define LIM_C_MAX (50.0)
	
/* Return constants for bounds checks */
#define INBOUNDS (1)
#define OUTOFBOUNDS (0);
	
/* Checks that the given theta is in the limits */
int checkO(float o);
/* Checks that the given radius is in the limits */
int checkR(float r);
/* Checks that the given elevation is in the limits */
int checkZ(float z);
/* Checks that the given claw position is in the limits */
int checkC(float c);
/* Checks that all positions are in their limits */
int checkAll(pos_t* pos);

#ifdef	__cplusplus
}
#endif

#endif	/* LIMITS_H */

