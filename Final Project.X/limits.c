/* 
 * File:   limits.c
 * Author: Peter
 */

#include "limits.h"
#include "scaling.h"
#include "types.h"

/* Checks that the given theta is in the limits */
int checkO(float o){
	return (o == range(o, LIM_O_MIN, LIM_O_MAX)) ? INBOUNDS : OUTOFBOUNDS;
}

/* Checks that the given radius is in the limits */
int checkR(float r){
	return (r == range(r, LIM_R_MIN, LIM_R_MAX)) ? INBOUNDS : OUTOFBOUNDS;
}

/* Checks that the given elevation is in the limits */
int checkZ(float z){
	return (z == range(z, LIM_Z_MIN, LIM_Z_MAX)) ? INBOUNDS : OUTOFBOUNDS;
}

/* Checks that the given claw position is in the limits */
int checkC(float c){
	return (c == range(c, LIM_C_MIN, LIM_C_MAX)) ? INBOUNDS : OUTOFBOUNDS;
}

/* Checks that all positions are in their limits */
int checkAll(pos_t* pos){
	return (checkO(pos->o) == INBOUNDS && checkR(pos->r) == INBOUNDS && \
			checkZ(pos->z) == INBOUNDS && checkC(pos->c) == INBOUNDS)\
			? INBOUNDS : OUTOFBOUNDS;
}