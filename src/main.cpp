#include <Arduino.h>
#include <stdlib.h>

void runTurn();

const int buttonPin = 2;  
const int ledPin = 13; 
const int buzzerPin = 7; 
const int startButtonPin = 10;  

const int frequency = 220;
const int maxTurns = 10;

int buttonState = 0;
int startButtonState = 0;
int turnNo = 0;

unsigned long start_time;
unsigned long end_time;
float difference;

const int upper_bound = 2;
const int lower_bound = 1;

void setup() {
  Serial.begin(9600);
  
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT);
  pinMode(buzzerPin, OUTPUT);
  pinMode(startButtonPin, INPUT);
}

void runTurn(){
  buttonState = digitalRead(buttonPin);
  int value = rand() % (upper_bound - lower_bound + 1) + lower_bound;

  Serial.println("start");
  start_time = micros();
  
  while (buttonState == 0){
    if (value == 1){
      digitalWrite(ledPin, HIGH);
      buttonState = digitalRead(buttonPin);
    }
    if (value == 2){
      tone(buzzerPin, frequency);
      buttonState = digitalRead(buttonPin);
    }
  }
  
  end_time = micros();
  difference = (end_time - start_time);
  Serial.println(turnNo);
  Serial.println("time difference in miliseconds:");
  Serial.println(difference  / 1000);
  
  digitalWrite(ledPin, LOW);
  noTone(buzzerPin);
  
  turnNo += 1;
  delay(2000);
}

void loop() {
  startButtonState = digitalRead(startButtonPin);
  
  if (startButtonState == 1){
      delay(1000);
      while (turnNo <= maxTurns){
          runTurn();
      } 
      Serial.println("max turns reached");
  }
  turnNo = 1;
}



