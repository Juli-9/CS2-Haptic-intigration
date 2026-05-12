#include "phatom_sensation.h"

PhatomSensation ps(13, 12);

void setup() {
  Serial.begin(9600);
  ps.update_intensity(.15);
}

void loop() {
  for(float i = 0.0; i < 1.0; i+=0.01){
    ps.update_position(i);
    ps.process();
    Serial.println(i);
    delay(100);
  }
  ps.off();
  delay(1000);
}