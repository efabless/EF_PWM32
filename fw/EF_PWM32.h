#ifndef EF_PWM32_H
#define EF_PWM32_H

#include <stdint.h>
#include <stdbool.h>
#include <EF_PWM32_regs.h>

enum pwm32_mode {PWM_UP = 0, PWM_UP_DOWN = 1};
enum pwm32_action_condition {PWM32_COUNT_ZERO = 0, PWM32_COUNT_CMPA_UP = 2, PWM32_COUNT_CMPB_UP = 4, PWM32_COUNT_TOP = 6, PWM32_COUNT_CMPB_DOWN = 8, PWM32_COUNT_CMPA_DOWN = 10};
enum pwm32_action {PWM32_NONE = 0, PWM32_HIGH = 1, PWM32_LOW = 2, PWM32_INVERT = 3};

void EF_PWM32_writeCompareA(uint32_t pwm32_base, int data);

void EF_PWM32_writeCompareB(uint32_t pwm32_base, int data);

void EF_PWM32_writeCounterTop(uint32_t pwm32_base, int data);

void EF_PWM32_writeClockDiv(uint32_t pwm32_base, int data);

void EF_PWM32_enablePWM(uint32_t pwm32_base, bool is_enable);

void EF_PWM32_enablePWMA(uint32_t pwm32_base, bool is_disable);

void EF_PWM32_enablePWMB(uint32_t pwm32_base, bool is_disable);

void EF_PWM32_invChA(uint32_t pwm32_base, bool is_invert);

void EF_PWM32_invChB(uint32_t pwm32_base, bool is_invert);

void EF_PWM32_setMode(uint32_t pwm32_base, enum pwm32_mode mode);

void EF_PWM32_setActionsA(uint32_t pwm32_base, enum pwm32_action_condition condition, enum pwm32_action action);

void EF_PWM32_setActionsB(uint32_t pwm32_base, enum pwm32_action_condition condition, enum pwm32_action action);

void EF_PWM32_writeActoinRegA(uint32_t pwm32_base, int data);

void EF_PWM32_writeActoinRegB(uint32_t pwm32_base, int data);

#endif