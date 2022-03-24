#include "Adafruit_MLX90393.h"

uint8 addres1 = 12;
uint8 addres2 = 13;

Adafruit_MLX90393 sensor1 = Adafruit_MLX90393();
Adafruit_MLX90393 sensor2 = Adafruit_MLX90393();
#define MLX90393_CS 10

void setup(void)
{
  Serial.begin(115200);

  /* Wait for serial on USB platforms. */
  while (!Serial) {
      delay(10);
  }

  Serial.println("Starting Adafruit MLX90393 Demo");

  if (! sensor1.begin_I2C(addres1) || ! sensor2.begin_I2C(addres2)) {          // hardware I2C mode, can pass in address & alt Wire
    Serial.println("No sensor found ... check your wiring?");
    while (1) { delay(10); }
  }
  Serial.println("Found 2 MLX90393 sensors");

  sensor1.setGain(MLX90393_GAIN_2_5X);
  sensor2.setGain(MLX90393_GAIN_2_5X);

  // Set resolution, per axis
  sensor1.setResolution(MLX90393_X, MLX90393_RES_19);
  sensor1.setResolution(MLX90393_Y, MLX90393_RES_19);
  sensor1.setResolution(MLX90393_Z, MLX90393_RES_16);

  sensor2.setResolution(MLX90393_X, MLX90393_RES_19);
  sensor2.setResolution(MLX90393_Y, MLX90393_RES_19);
  sensor2.setResolution(MLX90393_Z, MLX90393_RES_16);

  // Set oversampling
  sensor1.setOversampling(MLX90393_OSR_2);
  sensor2.setOversampling(MLX90393_OSR_2);

  // Set digital filtering
  sensor1.setFilter(MLX90393_FILTER_6);
  sensor2.setFilter(MLX90393_FILTER_6);
}

void loop(void) {
  /*
  // get X Y and Z data at once
  if (sensor.readData(&x, &y, &z)) {
      Serial.print("X: "); Serial.print(x, 4); Serial.println(" uT");
      Serial.print("Y: "); Serial.print(y, 4); Serial.println(" uT");
      Serial.print("Z: "); Serial.print(z, 4); Serial.println(" uT");
  } else {
      Serial.println("Unable to read XYZ data from the sensor.");
  }
  */

  delay(500);

  /* Or....get a new sensor event, normalized to uTesla */
  sensors_event_t event1;
  sensors_event_t event2;
  sensor1.getEvent(&event1);
  sensor2.getEvent(&event2);
  /* Display the results (magnetic field is measured in uTesla) */
  Serial.print("X1: "); Serial.print(event1.magnetic.x);
  Serial.print(" \tY1: "); Serial.print(event1.magnetic.y);
  Serial.print(" \tZ1: "); Serial.print(event1.magnetic.z);

  Serial.print(" \tX2: "); Serial.print(event2.magnetic.x);
  Serial.print(" \tY2: "); Serial.print(event2.magnetic.y);
  Serial.print(" \tZ2: "); Serial.print(event2.magnetic.z);
  Serial.println("");

  delay(500);
}
