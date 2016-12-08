/* 
 * File:   scaling.c
 * Author: Peter
 */

#include "scaling.h"

/* Linearly Maps the float x from input space (i1,i2) to output space (o1,o2) */
float mapf(float x, float i1, float i2, float o1, float o2){
	return (x - i1) * (o2 - o1) / (i2 - i1) + o1;
}

/* Truncates x to inclusive range defined by min and max */
float range(float x, float min, float max){
	return (x < min) ? min : ((x > max) ? max : x);
}
