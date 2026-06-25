#pragma once

#include <Arduino.h>
#include "timer.h"

#define SERIAL_COM_FREQ 50


class HapticController {
public:
    enum class Pattern {
        Constant = 0,
        SinePulse = 1,
        SawUp = 2,
        SawDown = 3,
        HeavyShot = 4
    };
    HapticController(uint8_t pin1, uint8_t pin2);

    
    void update_position(float pos);
    void update_intensity(float intens);
    void update_pattern(HapticController::Pattern p, int period, bool oneShot);
    
    void process();
    
    private:
    uint8_t motor1_pin;
    uint8_t motor2_pin;
    
    float position = 0.5f;
    float intensity = 0.0;
    bool one_shot = false;
    
    HapticController::Pattern pattern = HapticController::Pattern::Constant;
    uint8_t pattern_idx = 0;
    int pattern_period_ms = 100;

    Timer loop_tim;
    Timer t;
    
    void off();
    float pattern_bias();
};
