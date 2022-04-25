/* Imports -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= */
#include <Arduino.h>
#include "Adafruit_MLX90393.h"'
#include <math.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <NTPClient.h>

#define WIFI_SSID "Hey Tom its Bob"
#define WIFI_PASS "allwewannadoiseatyourbrains" 
#define TARGET_IP "192.168.1.14"
#define TARGET_PORT 56200
/* Sensor code -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= */

struct XYZ {
  float x;
  float y;
  float z;
};

Adafruit_MLX90393 initSensor(Adafruit_MLX90393 sensor, int address) {
  if (! sensor.begin_I2C(address)) {
    Serial.println("No sensor found with address: "); 
    Serial.print(address);
  }
  
  sensor.setGain(MLX90393_GAIN_2X);

  // Set resolution, per axis
  sensor.setResolution(MLX90393_X, MLX90393_RES_19);
  sensor.setResolution(MLX90393_Y, MLX90393_RES_19);
  sensor.setResolution(MLX90393_Z, MLX90393_RES_19);

  // Set oversampling
  sensor.setOversampling(MLX90393_OSR_1);

  // Set digital filtering
  sensor.setFilter(MLX90393_FILTER_6);

  return sensor;
}


struct XYZ getSensValues(Adafruit_MLX90393 sensor){
  struct XYZ values;
  
  // get X Y and Z data at once
  if (sensor.readData(&values.x, &values.y, &values.z)) {        
      
      return values;
   }
}


/* Communication code =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= */

void setupWifi(){
  WiFi.begin(WIFI_SSID, WIFI_PASS);

    // Connecting to WiFi...
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);
  // Loop continuously while WiFi is not connected
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(800);
    Serial.print(".");
  }
  
  // Connected to WiFi
  Serial.println();
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());
}

/* Arduino setup/loop code and variable declares -=-=-=-=-=-=-=-=-= */
// sensor
Adafruit_MLX90393 sensor1 = Adafruit_MLX90393();
XYZ sensor1Values;
Adafruit_MLX90393 sensor2 = Adafruit_MLX90393();
XYZ sensor2Values;
Adafruit_MLX90393 sensor3 = Adafruit_MLX90393();
XYZ sensor3Values;

//Communication
WiFiUDP UDP;
NTPClient timeClient(UDP, "pool.ntp.org");

void setup() {
  Serial.begin(115200);
  sensor1 = initSensor(sensor1,12);
  sensor2 = initSensor(sensor2,13);
  sensor3 = initSensor(sensor3,14);

  setupWifi();
  timeClient.begin();
  timeClient.setTimeOffset(2*3600);
  
}

void loop() {
    timeClient.update();
    // get sensor values
    sensor1Values = getSensValues(sensor1);
    sensor2Values = getSensValues(sensor2);
    sensor3Values = getSensValues(sensor3);

    char message[256];
    snprintf(message,sizeof(message),"R;%s;%f;%f;%f;%f;%f;%f;%f;%f;%f",
    timeClient.getFormattedTime(),
    sensor1Values.x,sensor1Values.y,sensor1Values.z,
    sensor2Values.x,sensor2Values.y,sensor2Values.z,
    sensor3Values.x,sensor3Values.y,sensor3Values.z);
    
    // Send packet
    UDP.beginPacket("192.168.1.14", 56200);
    UDP.write(message);
    UDP.endPacket();
}
