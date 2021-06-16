// Initialize DS3231 Time Module
#include <Wire.h>
#include "RTClib.h"
RTC_DS3231 rtc;
//char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
String timeLabel = "Time";


bool century = false;
bool h12Flag;
bool pmFlag;

// Initialize Light Sensor:
int lightInput = A2;
int lightStatus = 0; // variable for reading the pin status
String lightLabel = "Photoresistor";


//Initialize DHT 22 Humidity Sensor
#include <Adafruit_Sensor.h>
#include <DHT.h>
// Set DHT pin:
#define DHTPIN 2

String humidityLabel = "Humidity in %";
String temperatureLabel = "Temperature in C°";
// Set DHT type, uncomment whatever type you're using!
#define DHTTYPE DHT22   // DHT 22  (AM2302)
// Initialize DHT sensor for normal 16mhz Arduino:
DHT dht = DHT(DHTPIN, DHTTYPE);


//Initialize CO2 Sensor
#include <MHZ19.h>
#include <SoftwareSerial.h>

int MHZ_TX_PIN = 10;  // TX Pin von MH-Z19C Digital pins --> Green
int MHZ_RX_PIN = 11;  // RX Pin von MH-Z19C Digital pins --> Blue
String co2Label = "CO2 in ppm";

// Objekt for the Sensor
MHZ19 co2Sensor;
SoftwareSerial co2Serial(MHZ_TX_PIN, MHZ_RX_PIN);

// Soil Moisture Sensor
const int dry = 595; // value for dry sensor
const int wet = 239; // value for wet sensor
String moistureLabe1 = "Soil Moisture in %";



bool label = true;
void setup() {
  // Begin serial communication at a baud rate of 9600:
  Serial.begin(9600);
  delay(3000);

  // Setup DS3231 Time Module
 if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  }

  if (rtc.lostPower()) {
    Serial.println("RTC lost power, lets set the time!");
 
  // Comment out below lines once you set the date & time.
    // Following line sets the RTC to the date & time this sketch was compiled
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  
  }

  //Setup Light Sensor
  pinMode(lightInput, INPUT);
  // Setup Humidity Sensor
  dht.begin();
  //Setup CO2 Sensor
  co2Serial.begin(9600);
  co2Sensor.begin(co2Serial);
  // Automatic calibration
  co2Sensor.autoCalibration(false);

   
}
void loop() {

    while(label){
    Serial.print(timeLabel);
    Serial.print(",");
    Serial.print(lightLabel);
    Serial.print(",");
    Serial.print(humidityLabel);
    Serial.print(",");
    Serial.print(temperatureLabel);
    Serial.print(",");
    Serial.print(co2Label);
    Serial.print(",");
    Serial.print(moistureLabe1);
    Serial.print('\n');
    


    label = false;
  }

 // Wait a few seconds between measurements:
  delay(1000);


 // Read Time
   DateTime now = rtc.now();
    //Serial.println("\n");
    //Serial.print(now.year(), DEC);
    //Serial.print('/');
    //Serial.print(now.month(), DEC);
    //Serial.print('/');
    //Serial.print(now.day(), DEC);
    //Serial.print(" (");
    //Serial.print(daysOfTheWeek[now.dayOfTheWeek()]);
    //Serial.print(") ");
    Serial.print(now.hour(), DEC);
    Serial.print(':');
    Serial.print(now.minute(), DEC);
    Serial.print(':');
    Serial.print(now.second(), DEC);
    Serial.print(",");

 // Read light status
 lightStatus = analogRead(lightInput);
 Serial.print(lightStatus); 
 Serial.print(",");

  // Read the humidity in %:
  float humidityValue = dht.readHumidity();
  // Read the temperature as Celsius:
  float temperatureValue = dht.readTemperature();
  
  // Check if any reads failed and exit early (to try again):
  if (isnan(humidityValue) || isnan(temperatureValue)){
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  Serial.print(humidityValue);
  Serial.print(",");
  Serial.print(temperatureValue);
  Serial.print(",");

  //Check CO2 in ppm
  int co2Content = co2Sensor.getCO2();
  Serial.print(co2Content);
  Serial.print(",");

  // Soil Moisture
   int sensorVal = analogRead(A3);
   int percentageHumididy = map(sensorVal, wet, dry, 100, 0); 
   Serial.print(percentageHumididy);
   Serial.print('\n');
  
 
}
