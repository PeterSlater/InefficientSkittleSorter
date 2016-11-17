#include "config.h"
#include "tft_master.h"
#include "tft_gfx.h"
#include "pt_cornell_1_2_1.h"

static struct pt_sem print_sem;
static struct pt pt_cmd, pt_input, pt_output, pt_DMA_output;

static char cmd[16];
static int value;
static int count;

static PT_THREAD(protothread_cmd(struct pt* pt)){
	PT_BEGIN(pt);
	
	while(1){
		sprintf(PT_send_buffer, "cmd>");
		PT_SPAWN(pt, &pt_DMA_output, PT_DMA_PutSerialBuffer(&pt_DMA_output));
		
		PT_SPAWN(pt, &pt_input, PT_GetSerialBuffer(&pt_input));
		sscanf(PT_term_buffer, "%s %d", cmd, &value);
		
		if(cmd[0] == 'd' && cmd[1] == '1'){
			SetDCOC1PWM(value);
		}
		
		if(cmd[0] == 'd' && cmd[1] == '2'){
			SetDCOC2PWM(value);
		}
		
		if(cmd[0] == 'd' && cmd[1] == '3'){
			SetDCOC3PWM(value);
		}
		
		if(cmd[0] == 'd' && cmd[1] == '4'){
			SetDCOC4PWM(value);
		}
		
		if(cmd[0] == 't'){
			sprintf(PT_send_buffer, "%d\r\n", count);
			count++;
			PT_SPAWN(pt, &pt_DMA_output, PT_DMA_PutSerialBuffer(&pt_DMA_output));
		}
	}
	
	PT_END(pt);
}

int main(int argc, char** argv) {
	OpenTimer2(T2_ON | T2_SOURCE_INT | T2_PS_1_16, 50000);
	
	OpenOC1(OC_ON | OC_TIMER2_SRC | OC_PWM_FAULT_PIN_DISABLE, 5000, 5000);
	PPSOutput(1, RPB4, OC1);
	OpenOC2(OC_ON | OC_TIMER2_SRC | OC_PWM_FAULT_PIN_DISABLE, 5000, 5000);
	PPSOutput(2, RPB5, OC2);
	OpenOC3(OC_ON | OC_TIMER2_SRC | OC_PWM_FAULT_PIN_DISABLE, 5000, 5000);
	PPSOutput(4, RPA3, OC3);
	OpenOC4(OC_ON | OC_TIMER2_SRC | OC_PWM_FAULT_PIN_DISABLE, 5000, 5000);
	PPSOutput(3, RPA4, OC4);
	
	PT_setup();
	INTEnableSystemMultiVectoredInt();
	
	tft_init_hw();
	tft_begin();
	tft_fillScreen(ILI9340_BLACK);
	tft_setRotation(0);
	
	PT_INIT(&pt_cmd);
	
	while(1){
		PT_SCHEDULE(protothread_cmd(&pt_cmd));
	}
	
	return 0;
}

