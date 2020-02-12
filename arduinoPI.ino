// include the library code:
#include <LiquidCrystal.h>
#include <dht.h>


// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
dht DHT;

void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  //  pinMode(7, OUTPUT);
  pinMode(9, INPUT);
  // initialize the serial communications:
  Serial.begin(9600);
}

void loop() {
  int chk = DHT.read11(8);
  double humidity = DHT.humidity;
  double temp = DHT.temperature;
  
  Serial.print(temp);
  Serial.print(humidity);
  
  // when characters arrive over the serial port...
  if (Serial.available()) {
    // wait a bit for the entire message to arrive
    delay(100);
    // clear the screen
    lcd.clear();
    // read all the available characters
    while (Serial.available() > 0) {
      // display each character to the LCD
      lcd.write(Serial.read());
    }
  }
  
  delay(1200);
}
