#include <Arduino.h>
#include <ArduinoJson.h>

#include "phantom_sensation.h"

//vars
PhantomSensation ps(13, 12);
StaticJsonDocument<256> json;
String JSONbuffer = "";

//prev states
int prev_firingPeriod = 100;
PhantomSensation::Pattern prev_firingPattern = PhantomSensation::Pattern::Constant;

//Multi Tasking
SemaphoreHandle_t jsonMutex;
TaskHandle_t serialTaskHandle;

void serialTask(void *parameter){
    while (true)
    {
        while (Serial.available() > 0)
        {
            char c = Serial.read();

            // Ende einer Nachricht
            if (c == '\n')
            {
                // LOCK
                xSemaphoreTake(jsonMutex, portMAX_DELAY);

                DeserializationError err = deserializeJson(json, JSONbuffer);
                
                // UNLOCK
                xSemaphoreGive(jsonMutex);

                if (err)
                {
                    Serial.print("JSON Fehler: ");
                    Serial.println(err.c_str());
                }

                JSONbuffer = "";


            }
            else
            {
                JSONbuffer += c;
            }
        }

        // CPU freigeben
        vTaskDelay(1);
    }
}

void setup() {
  Serial.begin(115200);
  ps.update_intensity(1);
  ps.update_pattern_period(1500);
  ps.update_pattern(PhantomSensation::Pattern::HeavyShot);

  // Mutex erzeugen
  jsonMutex = xSemaphoreCreateMutex();

  // Task auf Core 0 starten
  xTaskCreatePinnedToCore(
      serialTask,       // Funktion
      "SerialTask",     // Name
      4096,             // Stackgröße
      NULL,             // Parameter
      1,                // Priorität
      &serialTaskHandle,
      0                 // Core
  );

}

void loop() {

  update_phatom_senstaion();

  ps.process();
}

void update_phatom_senstaion(){

  // LOCK
  xSemaphoreTake(jsonMutex, portMAX_DELAY);

  ps.update_position(float(json["ammunitionPercent"]) * 0.01f);
  ps.update_intensity(json["isFiring"] ? (float(json["intensityPercent"]) * 0.01f) : (0.0f));

  if (prev_firingPeriod != json["firingPeriod"]) {
    ps.update_pattern_period(json["firingPeriod"]);
    prev_firingPeriod = json["firingPeriod"];
  }

  int patternRaw = json["firingPattern"] | 0;
  PhantomSensation::Pattern pattern = static_cast<PhantomSensation::Pattern>(patternRaw);

  if (prev_firingPattern != pattern)
  {
      ps.update_pattern(pattern);
      prev_firingPattern = pattern;
  }

  // UNLOCK
  xSemaphoreGive(jsonMutex);

}


