/* 
 * File:   config.h
 * Author: Peter Slater
 */

#ifndef CONFIG_H
#define	CONFIG_H

#define _SUPPRESS_PLIB_WARNING 1
#define _DISABLE_OPENADC10_CONFIGPORT_WARNING 

#include <plib.h>

/* Disable Primary and Secondary oscillator, Debugging, and JTAG */
#pragma config POSCMOD = OFF, FSOSCEN = OFF
#pragma config FWDTEN = OFF, JTAGEN = OFF, DEBUG = OFF

/* Configure SYSCLK to be 8 MHz /2 *20 /2 = 40MHz */
#pragma config FNOSC = FRCPLL, FPLLIDIV = DIV_2, FPLLMUL = MUL_20, FPLLODIV = DIV_2
#define sys_clock 40000000

/* Enable Serial Debugging with 9600 Baudrate */
#define use_uart_serial
#define BAUDRATE 9600

/* Configure PBCLK to be SYSCLK /1 = 40MHz */
#pragma config FPBDIV = DIV_1
#define pb_clock sys_clock

#endif	/* CONFIG_H */