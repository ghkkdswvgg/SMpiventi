#include <Servo.h>
#define PI 3.1415926535897932384626433832795
#define servoPin 10
#define dirPin 11
#define ena 12
#define stepPin 13
#define motorInterfaceType 1
Servo Servo1;

const int stepsPerRevolution = 905;
const float v_min = 0.1;     // RPM to set the starting speed for the acceleration
String readString;
int ind1;
int ind2;
float nb_step ;
float spd_max;
float acc = 0.4;
float spd0 = 10;
float vlm = -1;
float tm;
float slp = -1;
float itm = -1;
int motor_max_speed = 1000;

bool flag = 1;// added for debug

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(ena, OUTPUT);
  // pinMode(4, OUTPUT);
  pinMode(4, INPUT);
  Servo1.attach(servoPin);
  Serial.begin(9600);
  Serial.println("Start");
  Servo1.write(80);
  delay(1000);
  Servo1.write(0);
  delay(1000);
  digitalWrite(dirPin, LOW);
  int fdc = digitalRead(4);
  while (fdc == 0) {
    f_step(motor_max_speed / 10);
    // fdc = int(digitalRead(4));
    fdc = digitalRead(4);
    if (flag)
    {
      Serial.print("fdc=");
      Serial.println(fdc);
      flag = 0;
    }
  }
}

void loop() {
  Serial.print("(in loop)");
  float t;
  instructions();
  Servo1.write(0);
  delay(400);
  digitalWrite(dirPin, HIGH);
  f_stepper();
  delay(1000 * slp);
  digitalWrite(dirPin, LOW);
  f_stepper();

}


void f_stepper() {
  int counter = 0;
  float t = 0;
  float t1 = 0;
  float spd = 0;
  spd_max = (nb_step - acc * spd0 ) / (itm - acc);


  while (t < acc) {
    spd = spd0 + (1 - cos(t * PI / acc) ) * (spd_max - spd0) / 2 ;
    f_step(spd);
    t += 1 / spd;
    counter ++;
  }

  spd = spd_max ;


  while (t <= itm - acc) {
    f_step(spd);
    t += 1 / spd;
    counter ++;
  }

  t1 = t ;

  while (t < itm) {
    spd = spd0 + (1 + cos((t - t1) * PI / acc) ) * (spd_max - spd0) / 2 ;
    f_step(spd);
    t += 1 / spd;
    counter ++;
  }
}

void f_step(float spd) {
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(1000000 / (2 * spd));
  digitalWrite(stepPin, LOW);
  delayMicroseconds(1000000 / (2 * spd));
}

void instructions() {
  vlm = -1;
  itm = -1;
  slp = -1;

  while (slp == -1) {
    if (Serial.available())  {
      char c = Serial.read();  //gets one byte from serial buffer
      if (c == ';') {
        Serial.println();
        Serial.print("captured String is : ");
        Serial.println(readString); //prints string to serial port out

        ind1 = readString.indexOf('T');  //finds location of first ,
        vlm = readString.substring(1, ind1).toFloat();   //captures first data String
        ind2 = readString.indexOf('S', ind1 + 1 ); //finds location of second ,
        itm = readString.substring(ind1 + 1, ind2).toFloat(); //captures second data String
        slp = readString.substring(ind2 + 1).toFloat(); //captures remain part of data after last ,

        Serial.print("vlm = ");
        Serial.println(vlm);
        Serial.print("itm = ");
        Serial.println(itm);
        Serial.print("slp = ");
        Serial.println(slp);

        readString = ""; //clears variable for new input
      }
      else {
        readString += c; //makes the string readString
      }
      nb_step = 250 * vlm;
    }
  }
}
