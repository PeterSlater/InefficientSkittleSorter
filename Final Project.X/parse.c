/* 
 * File:   parse.c
 * Author: Peter
 */

#include "parse.h"
#include "types.h"
#include <math.h>
#include <stdio.h>
#include "limits.h"

/* Handle the theta input o to current position pos, returns err */
void handleO(pos_t* pos, float o, char* err){
	if(checkO(o) == INBOUNDS){
		pos->o = o;
		updateXY(pos);
	}else sprintf(err, "ERROR: o = %3.2f not in [%3.2f:%3.2f]\r\n", o, LIM_O_MIN, LIM_O_MAX);
}

/* Handle the radius input r to current position pos, returns err */
void handleR(pos_t* pos, float r, char* err){
	if(checkR(r) == INBOUNDS){
		pos->r = r;
		updateXY(pos);
	}else sprintf(err, "ERROR: r = %3.2f not in [%3.2f:%3.2f]\r\n", r, LIM_R_MIN, LIM_R_MAX);
}

/* Handle the elevation input z to current position pos, returns err */
void handleZ(pos_t* pos, float z, char* err){
	if(checkZ(z) == INBOUNDS) pos->z = z;
	else sprintf(err, "ERROR: z = %3.2f not in [%3.2f:%3.2f]\r\n", z, LIM_Z_MIN, LIM_Z_MAX);
}

/* Handle the claw input c to current position pos, returns err */
void handleC(pos_t* pos, float c, char* err){
	if(checkC(c) == INBOUNDS) pos->c = c;
	else sprintf(err, "ERROR: c = %3.2f not in [%3.2f:%3.2f]\r\n", c, LIM_C_MIN, LIM_C_MAX);
}

/* Handle the X input x to current position pos, returns err */
void handleX(pos_t* pos, float x, char* err){
	float o_tmp = atan2(pos->y, x) * 180.0 / M_PI;
	float r_tmp = sqrt((x * x) + (pos->y * pos->y));
	
	if(checkO(o_tmp) == INBOUNDS && checkR(r_tmp) == INBOUNDS){
		pos->x = x;
		pos->o = o_tmp;
		pos->r = r_tmp;
	} else {
		if(pos->y < LIM_R_MIN){
			float limO = sqrt((LIM_R_MAX * LIM_R_MAX) - (pos->y * pos->y));
			float limI = sqrt((LIM_R_MIN * LIM_R_MIN) - (pos->y * pos->y));
			
			sprintf(err, "ERROR: x = %3.2f not in [%3.2f:%3.2f] or [%3.2f:3.2f]\r\n", \
					x, -limO, -limI, limI, limO);
		} else {
			float limO = sqrt((LIM_R_MAX * LIM_R_MAX) - (pos->y * pos->y));
			
			sprintf(err, "ERROR: x = %3.2f not in [%3.2f:%3.2f]\r\n", x, -limO, limO);
		}
	}
}

/* Handle the Y input y to current position pos, returns err */
void handleY(pos_t* pos, float y, char* err){
	float o_tmp = atan2(y, pos->x) * 180.0 / M_PI;
	float r_tmp = sqrt((pos->x * pos->x) + (y * y));
	
	if(checkO(o_tmp) == INBOUNDS && checkR(r_tmp) == INBOUNDS){
		pos->y = y;
		pos->o = o_tmp;
		pos->r = r_tmp;
	} else {
		float limO = sqrt((LIM_R_MAX * LIM_R_MAX) - (pos->x * pos->x));
		float limI = sqrt((LIM_R_MIN * LIM_R_MIN) - (pos->x * pos->x));
			
		sprintf(err, "ERROR: y = %3.2f not in [%3.2f:%3.2f]\r\n", y, limI, limO);
	}
}

/* Handle the X-step input w to current position pos, returns err */
void handleW(pos_t* pos, float w, char* err){
	handleX(pos, w + pos->x, err);
}

/* Handle the Y-step input h to current position pos, returns err */
void handleH(pos_t* pos, float h, char* err){
	handleY(pos, h + pos->y, err);
}

/* Handle the request values command */
void handleV(pos_t* pos, char* out){
	sprintf(out, "o: %3.2f r: %3.2f z: %3.2f c: %3.2f --> x: %3.2f y: %3.2f\r\n", \
			pos->o, pos->r, pos->z, pos->c, pos->x, pos->y);
}

/* Updates the X and Y position to follow the radius and theta */
void updateXY(pos_t* pos){
	pos->x = pos->r * cos(pos->o * M_PI / 180.0);
	pos->y = pos->r * sin(pos->o * M_PI / 180.0);
}
