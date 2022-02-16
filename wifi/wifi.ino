#include <DHT.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266HTTPClient.h>

//WiFi Data
const char* ssid = "Home118-2.4";
const char* password = "18181818!";
WiFiServer server(80);

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
  while (WiFi.status() != WL_CONNECTED) 
  {
     delay(500);
     Serial.print("*");
  }
  
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

  Serial.print("Server Starting...\n");
  server.begin();
  Serial.print("Sensor Starting...\n");
  dht.begin();
  Serial.print("Setup Complete...\n");
}

void loop() {
  if (WiFi.status() != WL_CONNECTED){
    Serial.print("Reconnecting...");
    WiFi.begin(ssid, password);
  }
  serial();
  relay();
}

//Read serial and analog responses
void serial(){
  //humidity = dht.readHumidity();
  //temperature = dht.readTemperature();

  //leftSoilMoisture = analogRead(SMSensor_L);
}

void relay(){
  WiFiClient client = server.available();
  if (!client)
  {
    return;
  }
  Serial.println("Waiting for new client");

  while(!client.available())
  {
    delay(1);
  }

  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();

  if(request.indexOf("/Water=ON") != -1){
    digitalWrite(WaterPin, LOW);
    waterStatus = true;
  }
  if(request.indexOf("/Water=OFF") != -1){
    digitalWrite(WaterPin, HIGH);
    waterStatus = false;
  }

  if(request.indexOf("/Humidifier=ON") != -1){
    digitalWrite(HumidityPin, LOW);
    humidStatus = true;
  }
  if(request.indexOf("/Humidifier=OFF") != -1){
    digitalWrite(HumidityPin, HIGH);
    humidStatus = false;
  }

  if(request.indexOf("/SoilMoisture=ON") != -1){
    digitalWrite(SoilPin, LOW);
    SMSensorStatus = true;
  }
  if(request.indexOf("/SoilMoisture=OFF") != -1){
    digitalWrite(SoilPin, HIGH);
    SMSensorStatus = false;
  }

  if(request.indexOf("/relay4=ON") != -1){
    digitalWrite(unknown, LOW);
    freeSlot1 = true;
  }
  if(request.indexOf("/relay4=OFF") != -1){
    digitalWrite(unknown, HIGH);
    freeSlot1 = false;
  }

  if(request.indexOf("/WaterValve=ON") != -1){
    digitalWrite(WaterValve, LOW);
    WaterValveStatus = true;
  }
  if(request.indexOf("/WaterValve=OFF") != -1){
    digitalWrite(WaterValve, HIGH);
    WaterValveStatus = false;
  }

  //*------------------HTML Page Code---------------------*//



  client.println("HTTP/1.1 200 OK"); //

  client.println("Content-Type: text/html");

  client.println("");

  client.println("<!DOCTYPE HTML>");

  client.println("<html>");

  client.println("<br><br>");

  client.println("Temperature:");
  client.println(temperature);
  client.println("Humidity:");
  client.println(humidity);
  client.println("LSM:");
  client.println(String(leftSoilMoisture));
  client.println("RSM:");
  client.println(String(rightSoilMoisture));
  client.println("WaterStatus:");
  client.println(waterStatus);
  client.println("SMStatus:");
  client.println(SMSensorStatus);
  client.println("HumidifierStatus:");
  client.println(humidStatus);
  client.println("WaterValve:");
  client.println(WaterValveStatus);
  client.println("FreeSlot1:");
  client.println(freeSlot1);  
  
  client.println("<br />");
  
  client.println("Water Pump");
  client.println("<a href=\"/Water=ON\"\"><button>ON</button></a>");
  client.println("<a href=\"/Water=OFF\"\"><button>OFF</button></a><br />");

  client.println("Humidifier");
  client.println("<a href=\"/Humidifier=ON\"\"><button>ON</button></a>");
  client.println("<a href=\"/Humidifier=OFF\"\"><button>OFF</button></a><br />");

  client.println("SoilMoisture");
  client.println("<a href=\"/SoilMoisture=ON\"\"><button>ON</button></a>");
  client.println("<a href=\"/SoilMoisture=OFF\"\"><button>OFF</button></a><br />");

  client.println("FreeSlot 1");
  client.println("<a href=\"/relay4=ON\"\"><button>ON</button></a>");
  client.println("<a href=\"/relay4=OFF\"\"><button>OFF</button></a><br />");

  client.println("WaterValve");
  client.println("<a href=\"/WaterValve=ON\"\"><button>ON</button></a>");
  client.println("<a href=\"/WaterValve=OFF\"\"><button>OFF</button></a><br />");

  client.println("</html>");
  delay(1);

  Serial.println("Client disonnected");

  Serial.println("");
}
