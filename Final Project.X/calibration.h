/* 
 * File:   calibration.h
 * Author: Peter
 */

#ifndef CALIBRATION_H
#define	CALIBRATION_H

#ifdef	__cplusplus
extern "C" {
#endif

/* Base Calibration Points */
#define CAL_BS_I1 (0.0)
#define CAL_BS_O1 (1850.0)
#define CAL_BS_I2 (90.0)
#define CAL_BS_O2 (4080.0)

/* Shoulder Calibration Points */
#define CAL_SH_I1 (0.0)
#define CAL_SH_O1 (6075.0)
#define CAL_SH_I2 (90.0)
#define CAL_SH_O2 (3625.0)

/* Elbow Calibration Points */
#define CAL_EL_I1 (0.0)
#define CAL_EL_O1 (3700.0)
#define CAL_EL_I2 (90.0)
#define CAL_EL_O2 (1500.0)
	
/* Claw Calibration Points */
#define CAL_CW_I1 (0.0)
#define CAL_CW_O1 (2400.0)
#define CAL_CW_I2 (50.0)
#define CAL_CW_O2 (1300.0)

#ifdef	__cplusplus
}
#endif

#endif	/* CALIBRATION_H */

