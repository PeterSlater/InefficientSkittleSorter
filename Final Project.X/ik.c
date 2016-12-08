/* 
 * File:   ik.c
 * Author: Peter
 */

#include "ik.h"
#include "limits.h"
#include "scaling.h"
#include "types.h"
#include <math.h>

/* Returned if input position is out of bounds */
ang_t IK_OOB = {0.0,0.0,0.0,0.0};

/* Bicep length constants, in mm */
#define BCP_LEN (81.0)
#define BCP_LEN_SQ (81.0 * 81.0)

/* Forearm length constants, in mm */
#define FRM_LEN (81.0)
#define FRM_LEN_SQ (81.0 * 81.0)

/* If position is in bounds define by limits returns the angle outputs or 
 * IK_OOB if position is out of bounds */
void ik_solve(pos_t* pos, ang_t* ang){
	/* test if pos is inbounds */
	if(checkAll(pos) == INBOUNDS){
		/* set the easy angles */
		ang->bs = pos->o;
		ang->cw = pos->c;
		
		/* calculate the difficult angles */
		float b = sqrt((pos->r * pos->r) + (pos->z * pos->z));
		float P = atan2(pos->z, pos->r);
		float A = acos((-FRM_LEN_SQ + BCP_LEN_SQ + (b * b))/(2.0 * BCP_LEN * b));
		float B = acos((FRM_LEN_SQ + BCP_LEN_SQ - (b * b)) / (2.0 * BCP_LEN * FRM_LEN));

		float sh_rad = A + P;
		float el_rad = M_PI - B - A - P;
		
		/* set the difficult angles */
		ang->sh = (180.0 / M_PI) * sh_rad;
		ang->el = (180.0 / M_PI) * el_rad;
	} else ang = &IK_OOB;
}
