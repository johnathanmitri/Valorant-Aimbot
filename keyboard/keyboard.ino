#include <ps2dev.h>    //Emulate a PS/2 device
PS2dev keyboard(3,2);  //clock, data

unsigned long timecount = 0;

void setup()
{
  
  Serial.begin(9600);
  Serial.write("OH MY GOD\n");
  pinMode(LED_BUILTIN, OUTPUT);

  digitalWrite(LED_BUILTIN, HIGH);  
  delay(4000);
  digitalWrite(LED_BUILTIN, LOW);  
  delay(1000);
  digitalWrite(LED_BUILTIN, HIGH);  
  delay(150);
  digitalWrite(LED_BUILTIN, LOW); 

  Serial.write("Keyboard init...\n");
  keyboard.keyboard_init();
  Serial.write("Keyboard init finished!!\n");
}

void loop()
{
  //Handle PS2 communication and react to keyboard led change
  //This should be done at least once each 10ms
  unsigned char leds;
  if(keyboard.keyboard_handle(&leds)) {
    //Serial.print('LEDS');
    //Serial.print(leds, HEX);
    digitalWrite(LED_BUILTIN, leds);
  }

  //Print a number every second
  if((millis() - timecount) > 1000) {
    keyboard.keyboard_mkbrk(PS2dev::ONE);
    Serial.print('.');
    timecount = millis();
  }
}