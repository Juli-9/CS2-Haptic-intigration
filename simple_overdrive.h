#pragma once

#include <Arduino.h>

class SimpleOverdrive {
private:
    uint8_t pin;

    uint8_t overdriveDuration = 0;
    uint8_t overdriveIntensity = 0;

public:
    SimpleOverdrive(uint8_t pin);

    void on(uint8_t intensity);
    void off();

    void setOverdrive(uint8_t intensity, uint16_t duration);
};
