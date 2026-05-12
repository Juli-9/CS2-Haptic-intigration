#pragma once

#include <Arduino.h>

class PhatomSensation {
public:
    enum class Pattern {
        Constant = 0,
        PulseSlow = 1,
        PulseFast = 2,
        RampUp = 3,
        RampDown = 4
    };
    PhatomSensation(uint8_t pin1, uint8_t pin2);
    void off();

    void update_position(float pos);
    void update_intensity(float intens);
    void update_pattern(PhatomSensation::Pattern p);

    void process();

private:
    uint8_t motor1_pin;
    uint8_t motor2_pin;

    float position = 0.5f;
    float intensity = 1.0;
    PhatomSensation::Pattern pattern = PhatomSensation::Pattern::Constant;
    int pattern_idx = 0;
    float pattern_bias();
};
