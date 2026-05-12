#include "simple_overdrive.h"

SimpleOverdrive::SimpleOverdrive(uint8_t pin) {
    this->pin = pin;
    pinMode(this->pin, OUTPUT);

    off();
}

void SimpleOverdrive::on(uint8_t intensity) {
    if(this->overdriveDuration && this->overdriveIntensity) {
      analogWrite(pin, this->overdriveIntensity);
      delay(this->overdriveDuration);
    }
    analogWrite(pin, intensity);
}

void SimpleOverdrive::off() {
    analogWrite(pin, LOW);
}

void SimpleOverdrive::setOverdrive(uint8_t intensity, uint16_t duration) {
  this->overdriveDuration = duration;
  this->overdriveIntensity = intensity;
}
