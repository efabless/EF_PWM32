/*
	Copyright 2023 Mohamed Shalan


*/


#define EF_PWM32_BASE				0x00000000

#define	EF_PWM32_CMPA_REG_ADDR		(EF_PWM32_BASE+0x0)
#define	EF_PWM32_CMPB_REG_ADDR		(EF_PWM32_BASE+0x4)
#define	EF_PWM32_LOAD_REG_ADDR		(EF_PWM32_BASE+0x8)
#define	EF_PWM32_CLKDIV_REG_ADDR		(EF_PWM32_BASE+0xc)
#define	EF_PWM32_CONTROL_REG_ADDR		(EF_PWM32_BASE+0x10)
#define	EF_PWM32_GENA_REG_ADDR		(EF_PWM32_BASE+0x14)
#define	EF_PWM32_GENB_REG_ADDR		(EF_PWM32_BASE+0x18)

#define EF_PWM32_CLKDIV_REG_CLKDIV		0
#define EF_PWM32_CLKDIV_REG_CLKDIV_LEN	4
#define EF_PWM32_CONTROL_REG_EN		0
#define EF_PWM32_CONTROL_REG_EN_LEN	1
#define EF_PWM32_CONTROL_REG_PWMA_EN		1
#define EF_PWM32_CONTROL_REG_PWMA_EN_LEN	1
#define EF_PWM32_CONTROL_REG_PWMB_EN		2
#define EF_PWM32_CONTROL_REG_PWMB_EN_LEN	1
#define EF_PWM32_CONTROL_REG_PWMA_INV		3
#define EF_PWM32_CONTROL_REG_PWMA_INV_LEN	1
#define EF_PWM32_CONTROL_REG_PWMBINV		4
#define EF_PWM32_CONTROL_REG_PWMBINV_LEN	1
#define EF_PWM32_CONTROL_REG_CNTR_MODE		5
#define EF_PWM32_CONTROL_REG_CNTR_MODE_LEN	1
#define EF_PWM32_GENA_REG_ZERO		0
#define EF_PWM32_GENA_REG_ZERO_LEN	2
#define EF_PWM32_GENA_REG_AUP		2
#define EF_PWM32_GENA_REG_AUP_LEN	2
#define EF_PWM32_GENA_REG_BUP		4
#define EF_PWM32_GENA_REG_BUP_LEN	2
#define EF_PWM32_GENA_REG_LOAD		6
#define EF_PWM32_GENA_REG_LOAD_LEN	2
#define EF_PWM32_GENA_REG_BD		8
#define EF_PWM32_GENA_REG_BD_LEN	2
#define EF_PWM32_GENA_REG_AD		10
#define EF_PWM32_GENA_REG_AD_LEN	2
#define EF_PWM32_GENB_REG_ZERO		0
#define EF_PWM32_GENB_REG_ZERO_LEN	2
#define EF_PWM32_GENB_REG_AUP		2
#define EF_PWM32_GENB_REG_AUP_LEN	2
#define EF_PWM32_GENB_REG_BUP		4
#define EF_PWM32_GENB_REG_BUP_LEN	2
#define EF_PWM32_GENB_REG_LOAD		6
#define EF_PWM32_GENB_REG_LOAD_LEN	2
#define EF_PWM32_GENB_REG_BD		8
#define EF_PWM32_GENB_REG_BD_LEN	2
#define EF_PWM32_GENB_REG_AD		10
#define EF_PWM32_GENB_REG_AD_LEN	2

volatile unsigned int * ef_pwm32_cmpA	= (volatile unsigned int *) EF_PWM32_CMPA_REG_ADDR;
volatile unsigned int * ef_pwm32_cmpB	= (volatile unsigned int *) EF_PWM32_CMPB_REG_ADDR;
volatile unsigned int * ef_pwm32_load	= (volatile unsigned int *) EF_PWM32_LOAD_REG_ADDR;
volatile unsigned int * ef_pwm32_clkdiv	= (volatile unsigned int *) EF_PWM32_CLKDIV_REG_ADDR;
volatile unsigned int * ef_pwm32_control	= (volatile unsigned int *) EF_PWM32_CONTROL_REG_ADDR;
volatile unsigned int * ef_pwm32_GENA	= (volatile unsigned int *) EF_PWM32_GENA_REG_ADDR;
volatile unsigned int * ef_pwm32_GENB	= (volatile unsigned int *) EF_PWM32_GENB_REG_ADDR;
