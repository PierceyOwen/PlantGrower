#include <DHT.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266HTTPClient.h>

//WiFi Data
const char* ssid = "Home118-2.4";
const char* password = "18181818!";
const char* host = "http://192.168.0.162:8081";

//Sensor Data Vars
float humidity = 0;
float temperature = 0;
float leftSoilMoisture = 0;
float rightSoilMoisture = 0;

//Relay Status
boolean humidStatus = false;
boolean waterStatus = false;
boolean SMSensorStatus = false;
boolean freeSlot1 = false;
boolean WaterValveStatus = false;

//D4 is not used 12v
  
uint8_t SMSensor_L = A0;
//uint8_t SMSensor_R = ?
uint8_t DHTPin = D0; //tempHumiditySensor
uint8_t WaterPin = D1; //12v
uint8_t SoilPin = D2; //5v
//3 is fail on pull low
uint8_t unused_in_or_out = D4;
uint8_t unknown = D5; //relay4 5v power
uint8_t WaterValve = D6; //12v with D4 as data
uint8_t HumidityPin = D7; //12v

// Initialize DHT sensor.
DHT dht(DHTPin, DHT11);

//HTML Vars
String header;

void setup() {
  Serial.begin(115200);
  // Connect to WiFi
  WiFi.begin(ssid, password);
  
  Serial.println("");
  Serial.println("WiFi connection Successful");
  Serial.print("The IP Address of ESP8266 Module is: \n\n");
  Serial.print(WiFi.localIP());// Print the IP address

  pinMode(WaterPin, OUTPUT);
  pinMode(HumidityPin, OUTPUT);
  pinMode(SoilPin, OUTPUT);

  pinMode(DHTPin, INPUT);
  pinMode(SMSensor_L, INPUT);

  digitalWrite(WaterPin, HIGH);
  digitalWrite(HumidityPin, HIGH);
  digitalWrite(SoilPin, HIGH);
  digitalWrite(unknown, HIGH);
  digitalWrite(WaterValve, HIGH);

  Serial.print("Sensor Starting...\n");
  dht.begin();
  Serial.print("Setup Complete...\n");
}

void loop() {
  if (WiFi.status() != WL_CONNECTED){
    Serial.print("Reconnecting...\n");
    WiFi.begin(ssid, password);
  }
  logic();
}

void logic(){
  WiFiClient client;
  HTTPClient http;
  String path;

  //Send climate information
  Serial.print("Sending Climate\n");
  path = "/SetClimate.php?ID=1&temperature=" + String(temperature) + "&humidity=" + String(humidity);
  http.begin(host+path);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded"); 
  http.POST("");
  http.end();
  delay(5000);

  //Send Plant Information
  Serial.print("Sending Plant Info\n");
  path = "/SetPlant.php?ID=1&Moisture=" + String(leftSoilMoisture);
  http.begin(host+path);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded"); 
  http.POST("");
  http.end();
  delay(5000);

  //Send Water Utility Information
  Serial.print("Sending Utility Info\n");
  path = "/SetRelayStatus.php?ID=1&WaterStatus=" + String(waterStatus) + "&HumidifierStatus=" + String(humidStatus) + "&SMSensorStatus=" + String(SMSensorStatus) + "&LightStatus=-1";
  http.begin(host+path);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded"); 
  http.POST("");
  http.end();
  delay(5000);

  //Get Action Requests
  client.connect(host, 8081);
  String URL = "/GetActionRequest.json";
  client.print(String("GET ") + URL + " HTTP/1.1\r\n" + "Host: " + host + "\r\n" + "Connection: close\r\n\r\n");
  String httpResponse = client.readStringUntil('r');

  Serial.print(httpResponse);
  delay(10000);
}
