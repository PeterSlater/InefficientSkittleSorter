#include "config.h"
#include "tft_master.h"
#include "tft_gfx.h"
#include "pt_cornell_1_2_1.h"

#include "types.h"
#include "ik.h"
#include "arm.h"
#include "limits.h"
#include "scaling.h"
#include "parse.h"

static struct pt pt_cmd, pt_calc, pt_out, pt_input, pt_DMA_output;

static pos_t pos;
static ang_t ang;
static pwm_t pwm;

static PT_THREAD(protothread_cmd(struct pt* pt)){
	PT_BEGIN(pt);
	
	static char cmd[16];
	static char buf[256];
	static float value;
	
	while(1){
		/* prompt for input */
		//sprintf(PT_send_buffer, "cmd>");
		//PT_SPAWN(pt, &pt_DMA_output, PT_DMA_PutSerialBuffer(&pt_DMA_output));
		
		/* get the input as a command string and float value */
		PT_SPAWN(pt, &pt_input, PT_GetSerialBuffer(&pt_input));
		sscanf(PT_term_buffer, "%s %f", cmd, &value);
		
		/* clear the buffer */
		buf[0] = '\0';
		
		/* parse the command and value */
		if(cmd[0] == 'o') handleO(&pos, value, buf);
		else if(cmd[0] == 'r') handleR(&pos, value, buf);
		else if(cmd[0] == 'z') handleZ(&pos, value, buf);
		else if(cmd[0] == 'c') handleC(&pos, value, buf);
		else if(cmd[0] == 'x') handleX(&pos, value, buf);
		else if(cmd[0] == 'y') handleY(&pos, value, buf);
		else if(cmd[0] == 'w') handleW(&pos, value, buf);
		else if(cmd[0] == 'h') handleH(&pos, value, buf);
		else if(cmd[0] == 'v') handleV(&pos, buf);
		
		/* display any message */
		if(buf[0] != '\0'){
			sprintf(PT_send_buffer, "%s", buf);
			PT_SPAWN(pt, &pt_DMA_output, PT_DMA_PutSerialBuffer(&pt_DMA_output));
		}
		
		/* print out the duty cycles 
		if(cmd[0] == 'd'){
			sprintf(PT_send_buffer, "oc1:%d oc2:%d oc3:%d oc4:%d\r\n", ReadDCOC1PWM(), ReadDCOC2PWM(), ReadDCOC3PWM(), ReadDCOC4PWM());
			PT_SPAWN(pt, &pt_DMA_output, PT_DMA_PutSerialBuffer(&pt_DMA_output));
		}*/
	}
	
	PT_END(pt);
}

static PT_THREAD(protothread_calc(struct pt* pt)){
	PT_BEGIN(pt);
	
	while(1){
		if(checkAll(&pos) == INBOUNDS){
			ik_solve(&pos, &ang);
			ang_to_pwm(&ang, &pwm);
		}
		
		PT_YIELD(pt);
	}PT_END(pt);
}

static PT_THREAD(protothread_out(struct pt* pt)){
	PT_BEGIN(pt);
	
	while(1){
		arm_set(&pwm);
		PT_YIELD(pt);
	}PT_END(pt);
}
		
int main(int argc, char** argv) {
	/* Set the arm to the home position */
	pos.o = 90.0;
	pos.r = 75.0;
	pos.z = 0.0;
	pos.c = 50.0;
	updateXY(&pos);
	
	arm_init();
	
	PT_setup();
	INTEnableSystemMultiVectoredInt();
	
	tft_init_hw();
	tft_begin();
	tft_fillScreen(ILI9340_BLACK);
	tft_setRotation(0);
	
	PT_INIT(&pt_cmd);
	PT_INIT(&pt_calc);
	PT_INIT(&pt_out);
	
	while(1){
		PT_SCHEDULE(protothread_cmd(&pt_cmd));
		PT_SCHEDULE(protothread_calc(&pt_calc));
		PT_SCHEDULE(protothread_out(&pt_out));
	}
	
	return 0;
}

