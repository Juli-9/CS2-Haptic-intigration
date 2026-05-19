#include "phatom_sensation.h"
#include "timer.h"

PhatomSensation ps(13, 12);
// Timer t;

void setup() {
  // Serial.begin(9600);
  ps.update_intensity(1);
  ps.update_pattern_period(1500);
  ps.update_pattern(PhatomSensation::Pattern::HeavyShot);

}

void loop() {
  ps.process();


  // t.start(100);
  // for(float i = 0.0; i < 1.0;){
  //   if (t.isFinished()){
  //     t.start(100);
  //     ps.update_position(i);
  //     i += 0.01;
  //   } 

  //   ps.process();
  //   Serial.println(i);
  // }
  // ps.off();
  // ps.update_position(0);
  // delay(1000);
}