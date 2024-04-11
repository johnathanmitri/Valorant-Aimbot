const int ps2PowerPin = A0;

void setup() {
  Serial.begin(9600); 
  pinMode(ps2PowerPin, INPUT); 
}

void loop() {
  //Serial.print("Available: ");
  //Serial.println(Serial.available());
  int32_t sumX = 0;
  int32_t sumY = 0;

  Serial.print("Reading: ");
  Serial.println(analogRead(ps2PowerPin));
  /*if (digitalRead(ps2PowerPin) == HIGH) {
    Serial.println("5V is ON");
  } else {
    Serial.println("5V is OFF");
  }*/
  while (Serial.available() >= 8) { // Check if at least 8 bytes are available to read (two 32-bit integers)
    int32_t int1;
    Serial.readBytes((char*)&int1, sizeof(int1));
    int32_t int2;
    Serial.readBytes((char*)&int2, sizeof(int2));

    sumX += int1;
    sumY += int2;
  }

  if (sumX != 0 || sumY != 0)
  {
    Serial.print("delta X: ");
    Serial.print(sumX);
    Serial.print("   delta Y: ");
    Serial.println(sumY);
  }
  delay(1000);
}