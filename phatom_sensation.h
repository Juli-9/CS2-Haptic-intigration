#pragma once

#include <Arduino.h>

class PhatomSensation {
public:
    enum class Pattern {
        Constant = 0,
        SinePulse = 1,
        SawUp = 2,
        SawDown = 3,
        HeavyShot = 4
    };
    PhatomSensation(uint8_t pin1, uint8_t pin2);
    void off();

    void update_position(float pos);
    void update_intensity(float intens);
    void update_pattern(PhatomSensation::Pattern p);
    void update_pattern_period(int ms);

    void process();

private:
    uint8_t motor1_pin;
    uint8_t motor2_pin;

    float position = 0.5f;
    float intensity = 1.0;

    PhatomSensation::Pattern pattern = PhatomSensation::Pattern::Constant;
    uint8_t pattern_idx = 0;
    int pattern_period_ms = 100;
    
    float pattern_bias();
};
