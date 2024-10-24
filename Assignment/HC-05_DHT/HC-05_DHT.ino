#include "DHT.h"
//#include <SoftwareSerial.h>

#define DHTPIN 21      // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11

#define LEDPIN 11

#define SENSEID 3
DHT dht(DHTPIN, DHTTYPE);

// Teensy 5V <--> HC-05 Vcc
// Teensy Ground <--> HC-05 GND
#define rxPin 7 // Teensy pin 7 <--> HC-05 Tx
#define txPin 8 // Teensy pin 8 <--> HC-05 Rx
//SoftwareSerial BTSerial =  SoftwareSerial(rxPin, txPin);

void setup() {
  // Setup serial for monitor
  Serial.begin(9600); 

  // Setup DHT Sensor
  pinMode(DHTPIN, INPUT);
  dht.begin();

  // Setup Serial1 for BlueTooth
  Serial1.begin(9600); // Default communication rate of the Bluetooth module
}

void loop() {
  if(1){//Serial1.available() > 0){ // Checks whether data is comming from the serial port
    digitalWrite(LEDPIN, HIGH);
    
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    float hic = dht.computeHeatIndex(t, h, false);  

    Serial.print(F("["));
    Serial.print(SENSEID);
    Serial.print(",");
    Serial.print(h); //humidity
    Serial.print(F(","));
    Serial.print(t); //temperature C
    Serial.print(F(","));
    Serial.print(hic); //heat index C
    Serial.println(F("]"));

    Serial1.print(F("["));
    Serial1.print(SENSEID);
    Serial1.print(",");
    Serial1.print(h); //humidity
    Serial1.print(F(","));
    Serial1.print(t); //temperature C
    Serial1.print(F(","));
    Serial1.print(hic); //heat index C
    Serial1.println(F("]"));
    
    delay(1000);
    digitalWrite(LEDPIN, LOW);
    delay(1000);
 }
}