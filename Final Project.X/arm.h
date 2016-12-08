/* 
 * File:   arm.h
 * Author: Peter
 */

#ifndef ARM_H
#define	ARM_H

#include "types.h"

#ifdef	__cplusplus
extern "C" {
#endif

/* Initializes the PWM output channels for each joint */
void arm_init(void);

/* Moves the arm to the given angles */
void arm_move(ang_t* ang);
/* Sets each of the joints to the given pwm values */
void arm_set(pwm_t* pwm);

/* Converts the angles to PWM duty cycles using the calibration data */
void ang_to_pwm(ang_t* ang, pwm_t* pwm);


#ifdef	__cplusplus
}
#endif

#endif	/* ARM_H */

