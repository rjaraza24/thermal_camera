 #define irTemp 4  
#define irProx 2 
#define irSant 6  

#define relay2 9 
#define relay3 7 
#define relay4 8 
#include <LiquidCrystal_I2C.h>
#include <Wire.h>
LiquidCrystal_I2C lcd(0x3F,20,4);
LiquidCrystal_I2C lcd2(0x27,20,4);

#include "FastLED.h"
#define NUM_LEDS 10
CRGB leds[NUM_LEDS];
#include <Wire.h>
#include <Adafruit_MLX90614.h>

Adafruit_MLX90614 mlx = Adafruit_MLX90614();


boolean misting = false;
boolean sanitizing = false;

float BodyC;
float AmbC;

String hypo = "Hypothermia";
String norm = "Normal";
String fevr = "Fever";
String hypr = "Hyperpyrexia";
void setup() {

  Serial.begin(9600);
  pinMode(irProx, INPUT);
//  pinMode(irSant, INPUT);
//  pinMode(relay, OUTPUT);
//  pinMode(relay2, OUTPUT);
  pinMode(relay3, OUTPUT);
  pinMode(relay4, OUTPUT);  
//  FastLED.addLeds<WS2812B, ledp, RGB>(leds, NUM_LEDS);
//  Serial.println("Adafruit MLX90614 test");  
//  mlx.begin();  
//  lcd2.begin();
//  lcd.begin();
  
//  lcd.init();
//  lcd2.init(); 
//  
//  lcd.backlight();
//  lcd2.backlight();  
  
  delay(100);
  digitalWrite(relay3, LOW);
  digitalWrite(relay4, LOW);
}

void loop() {
  

      
   if((!digitalRead(irProx)) && misting == false){
    misting = true;
    mist();
    delay(100);
    misting = false;
   
  }
  delay(100);
}


void mist(){
    digitalWrite(relay4, HIGH);
    digitalWrite(relay3, LOW);
    delay(10000);
    digitalWrite(relay4, LOW);
    digitalWrite(relay3, LOW);
    Serial.println("Finish, exit chamber");
    delay(10000);
}
