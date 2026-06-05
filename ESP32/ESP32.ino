#include <Arduino.h>
#include <ArduinoJson.h>

#include "phantom_sensation.h"

PhantomSensation ps(13, 12);
StaticJsonDocument<256> json;
String JSONbuffer = "";

//states
bool isFiring = false;
int ammunitionPercent = 100;
int firingPeriod = 100;
PhantomSensation::Pattern firingPattern = PhantomSensation::Pattern::Constant;
int intensityPercent = 100;

//prev states
int prev_firingPeriod = 100;
PhantomSensation::Pattern prev_firingPattern = PhantomSensation::Pattern::Constant;


void setup() {
  Serial.begin(115200);
  ps.update_intensity(1);
  ps.update_pattern_period(1500);
  ps.update_pattern(PhantomSensation::Pattern::HeavyShot);

}

void loop() {

  if (readJsonFromSerial(json)) {
    update_states();
    update_phatom_senstaion();

  }

  ps.process();

}


bool readJsonFromSerial(JsonDocument &doc) {

  // while (Serial.available()) {
  if(!Serial.available()) return false;

    char c = Serial.read();

    if (c == '\n') {
      DeserializationError error = deserializeJson(doc, JSONbuffer);
      JSONbuffer = "";
      return !error;
    }

    JSONbuffer += c;
  // }
  return false;
}

void update_states() {
    isFiring = json["isFiring"];
    firingPeriod = json["firingPeriod"];
    firingPattern = (PhantomSensation::Pattern)(int)json["firingPattern"];
    ammunitionPercent = json["ammunitionPercent"];
    intensityPercent = json["intensityPercent"];

    serializeJson(json, Serial);
    Serial.print("\n");
}

void update_phatom_senstaion(){
  ps.update_position(float(ammunitionPercent) * 0.01f);
  ps.update_intensity(float(intensityPercent) * 0.01f);

  if (prev_firingPeriod != firingPeriod) {
    ps.update_pattern_period(firingPeriod);
    prev_firingPeriod = firingPeriod;
  }

  if (prev_firingPattern != firingPattern) {
    ps.update_pattern(PhantomSensation::Pattern(firingPattern));
    prev_firingPattern = firingPattern;
  }


}


