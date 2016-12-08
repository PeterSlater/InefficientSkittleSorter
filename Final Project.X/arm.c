/* 
 * File:   arm.c
 * Author: Peter
 */

#include <plib.h>
#include "arm.h"
#include "types.h"
#include "calibration.h"
#include "scaling.h"

/* Initializes the PWM output channels for each joint */
void arm_init(void){
	OpenTimer2(T2_ON | T2_SOURCE_INT | T2_PS_1_16, 50000);
	
	OpenOC1(OC_ON | OC_TIMER2_SRC | OC_PWM_FAULT_PIN_DISABLE, 0, 0);
	PPSOutput(1, RPB4, OC1);
	OpenOC2(OC_ON | OC_TIMER2_SRC | OC_PWM_FAULT_PIN_DISABLE, 0, 0);
	PPSOutput(2, RPB5, OC2);
	OpenOC3(OC_ON | OC_TIMER2_SRC | OC_PWM_FAULT_PIN_DISABLE, 0, 0);
	PPSOutput(4, RPA3, OC3);
	OpenOC4(OC_ON | OC_TIMER2_SRC | OC_PWM_FAULT_PIN_DISABLE, 0, 0);
	PPSOutput(3, RPA2, OC4);
}

/* Moves the arm to the given angles */
void arm_move(ang_t* ang){
	pwm_t pwm;
	
	/* Convert the angles then set the pwm values */
	ang_to_pwm(ang, &pwm);
	arm_set(&pwm);
}

/* Sets each of the joints to the given pwm values */
void arm_set(pwm_t* pwm){
	SetDCOC1PWM(pwm->bs);
	SetDCOC2PWM(pwm->sh);
	SetDCOC3PWM(pwm->el);
	SetDCOC4PWM(pwm->cw);
}

/* Converts the angles to PWM duty cycles using the calibration data */
void ang_to_pwm(ang_t* ang, pwm_t* pwm){
	pwm->bs = (unsigned short) mapf(ang->bs, CAL_BS_I1, CAL_BS_I2, CAL_BS_O1, CAL_BS_O2);
	pwm->sh = (unsigned short) mapf(ang->sh, CAL_SH_I1, CAL_SH_I2, CAL_SH_O1, CAL_SH_O2);
	pwm->el = (unsigned short) mapf(ang->el, CAL_EL_I1, CAL_EL_I2, CAL_EL_O1, CAL_EL_O2);
	pwm->cw = (unsigned short) mapf(ang->cw, CAL_CW_I1, CAL_CW_I2, CAL_CW_O1, CAL_CW_O2);
}

