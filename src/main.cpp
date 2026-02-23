#include <Arduino.h>
#include <stdlib.h>

void runTurn();

const int buttonPin = 2;  
const int ledPin = 13; 
const int buzzerPin = 7; 
const int startButtonPin = 10;  

const int frequency = 220;
const int maxTurns = 5;

int buttonState = 0;
int startButtonState = 0;
int turnNo = 0;

unsigned long start_time;
unsigned long end_time;
float difference;

// toto jsou hranice pro random na ledku a buzzer
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
  // začátek kola
  buttonState = digitalRead(buttonPin);

  start_time = micros();
  
  // náhodně urči jestli zazní buzzer nebo se rozsvítí ledka
  int rand_val = rand() % (upper_bound - lower_bound + 1) + lower_bound; 
  // náhodně urči delay před dalším kolem
  int rand_val_delay = rand() % (8000 - 1000 + 1) + 1000;

  while (buttonState == 0){
    if (rand_val == 1){
      digitalWrite(ledPin, HIGH);
      buttonState = digitalRead(buttonPin);
    }
    if (rand_val == 2){
      tone(buzzerPin, frequency);
      buttonState = digitalRead(buttonPin);
    }
  }
  
  // počítání reakční doby
  end_time = micros();
  difference = (end_time - start_time);
  Serial.println(">rozdíl v milisekundách:");
  Serial.println(difference / 1000);
  
  //konec kola - vypnout + počkat
  digitalWrite(ledPin, LOW);
  noTone(buzzerPin);
  
  turnNo += 1;
  delay(rand_val_delay); 
}

void loop() {
  startButtonState = digitalRead(startButtonPin);
  Serial.println(">start");
  
  // pokud se zmáčkl start button začni
  if (startButtonState == 1){
      delay(1000);
      // dokud se nedosáhne maximálního počtu kol, spouštěj další kola
      while (turnNo <= maxTurns){
          runTurn();
      } 
      Serial.println("<maximální počet kol dosažen");
  }
  turnNo = 1;
}



