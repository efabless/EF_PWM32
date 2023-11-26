#ifndef EF_PWM32_C
#define EF_PWM32_C

#include <EF_PWM32.h>


void EF_PWM32_writeCompareA(uint32_t pwm32_base, int data){

    EF_PWM32_TYPE* pwm32 = (EF_PWM32_TYPE*)pwm32_base;
    pwm32->cmpA = data;
}

void EF_PWM32_writeCompareB(uint32_t pwm32_base, int data){

    EF_PWM32_TYPE* pwm32 = (EF_PWM32_TYPE*)pwm32_base;
    pwm32->cmpB = data;
}

void EF_PWM32_writeCounterTop(uint32_t pwm32_base, int data){

    EF_PWM32_TYPE* pwm32 = (EF_PWM32_TYPE*)pwm32_base;
    pwm32->top = data;
}

void EF_PWM32_writeClockDiv(uint32_t pwm32_base, int data){

    EF_PWM32_TYPE* pwm32 = (EF_PWM32_TYPE*)pwm32_base;
    pwm32->clkdiv = data;
}

void EF_PWM32_enablePWM(uint32_t pwm32_base, bool is_enable){
    
    EF_PWM32_TYPE* pwm32 = (EF_PWM32_TYPE*)pwm32_base;
    if (is_enable == true)
        pwm32->control |= 0x1;
    else
        pwm32->control &= ~0x1;
}

void EF_PWM32_enablePWMA(uint32_t pwm32_base, bool is_disable){

    EF_PWM32_TYPE* pwm32 = (EF_PWM32_TYPE*)pwm32_base;
    if (is_disable == true)
        pwm32->control |= 0x3;
    else
        pwm32->control &= ~0x2;
    
}

void EF_PWM32_enablePWMB(uint32_t pwm32_base, bool is_disable){

    EF_PWM32_TYPE* pwm32 = (EF_PWM32_TYPE*)pwm32_base;
    if (is_disable == true)
        pwm32->control |= 0x5;
    else
        pwm32->control &= ~0x4;
}

void EF_PWM32_invChA(uint32_t pwm32_base, bool is_invert){

    EF_PWM32_TYPE* pwm32 = (EF_PWM32_TYPE*)pwm32_base;
    if (is_invert == true)
        pwm32->control |= 0x8;
    else
        pwm32->control &= ~0x8;
}
void EF_PWM32_invChB(uint32_t pwm32_base, bool is_invert){

    EF_PWM32_TYPE* pwm32 = (EF_PWM32_TYPE*)pwm32_base;
    if (is_invert == true)
        pwm32->control |= 0x10;
    else
        pwm32->control &= ~0x10;
}

void EF_PWM32_setMode(uint32_t pwm32_base, enum pwm32_mode mode){
    EF_PWM32_TYPE* pwm32 = (EF_PWM32_TYPE*)pwm32_base;
    if (mode == PWM_UP_DOWN)
        pwm32->control |= 0x20;
    else
        pwm32->control &= ~0x20;
}

void EF_PWM32_setActionsA(uint32_t pwm32_base, enum pwm32_action_condition condition, enum pwm32_action action){

    EF_PWM32_TYPE* pwm32 = (EF_PWM32_TYPE*)pwm32_base;
    int action_A = pwm32->GENA;
    action_A &= ~(0x3<<condition); // mask the action bits with 0 
    action_A |= (action << condition);
    pwm32->GENA = action_A;
}

void EF_PWM32_setActionsB(uint32_t pwm32_base, enum pwm32_action_condition condition, enum pwm32_action action){

    EF_PWM32_TYPE* pwm32 = (EF_PWM32_TYPE*)pwm32_base;
    int action_B = pwm32->GENB;
    action_B &= ~(0x3<<condition); // mask the action bits with 0 
    action_B |= (action << condition);
    pwm32->GENB = action_B;
}
void EF_PWM32_writeActoinRegA(uint32_t pwm32_base, int data){

    EF_PWM32_TYPE* pwm32 = (EF_PWM32_TYPE*)pwm32_base;
    pwm32->GENA = data;
}
void EF_PWM32_writeActoinRegB(uint32_t pwm32_base, int data){

    EF_PWM32_TYPE* pwm32 = (EF_PWM32_TYPE*)pwm32_base;
    pwm32->GENA = data;
}
#endif // EF_PWM32_H