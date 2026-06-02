#include <ArduinoJson.h>

#include "phatom_sensation.h"

PhatomSensation ps(13, 12);

void setup() {
  Serial.begin(9600);
  ps.update_intensity(1);
  ps.update_pattern_period(1500);
  ps.update_pattern(PhatomSensation::Pattern::HeavyShot);

}

void loop() {
  ps.process();
}

void 