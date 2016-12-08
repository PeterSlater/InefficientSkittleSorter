/* 
 * File:   types.h
 * Author: Peter
 */

#ifndef TYPES_H
#define	TYPES_H

#ifdef	__cplusplus
extern "C" {
#endif

/* Datatype for coordinate position inputs */
typedef struct pos_s {
	/* Theta */
	float o;
	/* Radius */
	float r;
	/* Elevation */
	float z;
	/* Claw */
	float c;
	/* X (secondary) */
	float x;
	/* Y (secondary) */
	float y;
}pos_t;

/* Datatype for arm angle outputs */
typedef struct ang_s {
	/* Base Angle */
	float bs;
	/* Shoulder Angle */
	float sh;
	/* Elbow Angle */
	float el;
	/* Claw Angle */
	float cw;
}ang_t;

/* Datatype for motor pwm duty-cycle outputs */
typedef struct pwm_s {
	/* Base duty-cycle */
	unsigned short bs;
	/* Shoulder duty-cycle */
	unsigned short sh;
	/* Elbow duty-cycle */
	unsigned short el;
	/* Claw duty-cycle */
	unsigned short cw;
}pwm_t;


#ifdef	__cplusplus
}
#endif

#endif	/* TYPES_H */

