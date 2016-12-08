/* 
 * File:   parse.h
 * Author: Peter
 */

#ifndef PARSE_H
#define	PARSE_H

#include "types.h"

#ifdef	__cplusplus
extern "C" {
#endif

/* Handle the theta input o to current position pos, returns err */
void handleO(pos_t* pos, float o, char* err);
/* Handle the radius input r to current position pos, returns err */
void handleR(pos_t* pos, float r, char* err);
/* Handle the elevation input z to current position pos, returns err */
void handleZ(pos_t* pos, float z, char* err);
/* Handle the claw input c to current position pos, returns err */
void handleC(pos_t* pos, float c, char* err);

/* Handle the X input x to current position pos, returns err */
void handleX(pos_t* pos, float x, char* err);
/* Handle the Y input y to current position pos, returns err */
void handleY(pos_t* pos, float y, char* err);
/* Handle the X-step input w to current position pos, returns err */
void handleW(pos_t* pos, float w, char* err);
/* Handle the Y-step input h to current position pos, returns err */
void handleH(pos_t* pos, float h, char* err);

/* Handle the request values command */
void handleV(pos_t* pos, char* out);

/* Updates the X and Y position to follow the radius and theta */
void updateXY(pos_t* pos);

#ifdef	__cplusplus
}
#endif

#endif	/* PARSE_H */

