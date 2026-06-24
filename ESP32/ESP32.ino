#include <Arduino.h>
#include <ArduinoJson.h>

#include "phantom_sensation.h"

//vars
PhantomSensation ps(13, 12);
StaticJsonDocument<512> json;
String JSONbuffer = "";
bool new_json_arrived = false;

//prev statesS
bool prev_mode = false;
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
                if (!err)
                {
                  new_json_arrived = true;
                }
                else
                {
                    Serial.print("JSON Fehler: ");
                    Serial.println(err.c_str());
                }
                
                // UNLOCK
                xSemaphoreGive(jsonMutex);


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
  Serial.begin(74880);
  ps.update_intensity(1.0);
  ps.update_position(1.0);
  ps.update_pattern(PhantomSensation::Pattern::SinePulse, 1096, false);

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


  // Serial.println(json.as<String>());



  if (new_json_arrived) 
  {
    // LOCK
    xSemaphoreTake(jsonMutex, portMAX_DELAY);

    ps.update_position(float(json["ammunitionPercent"]) * 0.01f);
    ps.update_intensity(json["isFiring"] ? (float(json["intensityPercent"]) * 0.01f) : (0.0f));

    int patternRaw = json["firingPattern"] | 0;
    PhantomSensation::Pattern pattern = static_cast<PhantomSensation::Pattern>(patternRaw);
    prev_firingPattern = pattern;

    prev_firingPeriod = json["firingPeriod"];
    prev_mode = json["oneShot"];
    ps.update_pattern(pattern, json["firingPeriod"], json["oneShot"]);
    new_json_arrived = false;

    // UNLOCK
    xSemaphoreGive(jsonMutex);
  }


}


