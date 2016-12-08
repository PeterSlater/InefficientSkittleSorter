/* 
 * File:   ik.h
 * Author: Peter
 */

#ifndef IK_H
#define	IK_H

#include "types.h"

#ifdef	__cplusplus
extern "C" {
#endif

/* Returned if input position is out of bounds */
extern ang_t IK_OOB;

/* If position is in bounds define by limits returns the angle outputs or 
 * IK_OOB if position is out of bounds */
void ik_solve(pos_t* pos, ang_t* ang);


#ifdef	__cplusplus
}
#endif

#endif	/* IK_H */

