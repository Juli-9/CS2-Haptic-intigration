#include <Arduino.h>
#include <ArduinoJson.h>

#include "haptic_controller.h"

//vars
HapticController hc(13, 12);
StaticJsonDocument<512> json;
StaticJsonDocument<512> tmp;
String JSONbuffer = "";
bool new_json_arrived = false;

//prev statesS
bool prev_mode = false;
int prev_firingPeriod = 100;
HapticController::Pattern prev_firingPattern = HapticController::Pattern::Constant;

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
                DeserializationError err = deserializeJson(tmp, JSONbuffer);
                
                // LOCK
                xSemaphoreTake(jsonMutex, portMAX_DELAY);

                if (!err)
                {
                  json = tmp;
                  new_json_arrived = true;
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
  Serial.setRxBufferSize(4096);
  Serial.begin(230400);
  hc.update_intensity(0.0);
  hc.update_position(1.0);
  hc.update_pattern(HapticController::Pattern::SinePulse, 1096, false);

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
  hc.process();
}

void update_phatom_senstaion(){


  // Serial.println(json.as<String>());



  if (new_json_arrived) 
  {
    // LOCK
    xSemaphoreTake(jsonMutex, portMAX_DELAY);

    if (json["isFiring"]){
      hc.on();
      hc.update_intensity(float(json["intensityPercent"]) * 0.01f);
    }
    else {
      hc.soft_stop();
      new_json_arrived = false;
      // UNLOCK
      xSemaphoreGive(jsonMutex);
      return;
    }

    hc.update_position(float(json["ammunitionPercent"]) * 0.01f);

    int patternRaw = json["firingPattern"] | 0;
    HapticController::Pattern pattern = static_cast<HapticController::Pattern>(patternRaw);

    if(prev_firingPattern != pattern
    || prev_firingPeriod != json["firingPeriod"]
    || json["oneShot"] != prev_mode
    || json["oneShot"])
    {

        prev_firingPattern = pattern;
        prev_firingPeriod = json["firingPeriod"];
        prev_mode = json["oneShot"];
        hc.update_pattern(pattern, json["firingPeriod"], json["oneShot"]);

    }


    new_json_arrived = false;

    // UNLOCK
    xSemaphoreGive(jsonMutex);
  }


}


