// black - data
//
// brown - ground
//
// orange - clock



#include <ps2dev.h>

PS2dev mouse(3,2); // 2 data 3clock

const int ps2PowerPin = 5;

char buttons[3] = {0,0,0};

int delta_x = 0;
int delta_y = 0;
//we start off not enabled
int enabled = 0;

//ack a host command
void ack() {
  while(mouse.write(0xFA));
}

void write_packet() {
  char overflowx =0;
  char overflowy =0;
  char data[3];
  int x,y;
  
  if (delta_x > 255) {
    overflowx =1;
    x=255;
  }
  if (delta_x < -255) {
    overflowx = 1;
    x=-255;
  }  
  if (delta_y > 255) {
    overflowy =1;
    y=255;
  }
  if (delta_y < -255) {
    overflowy = 1;
    y=-255;
  }
  
  data[0] = ((overflowy & 1) << 7) |
    ( (overflowx & 1) << 6) |
    ( (((delta_y &0x100)>>8) & 1) << 5) |
    ( ( ((delta_x &0x100)>>8)& 1) << 4) |
    ( ( 1) << 3) |
    ( ( buttons[1] & 1) << 2) |
    ( ( buttons[2] & 1) << 1) |
    ( ( buttons[0] & 1) << 0) ;
    
  data[1] = delta_x & 0xff;
  data[2] = delta_y & 0xff;
  
  mouse.write(data[0]);
  mouse.write(data[1]);

  mouse.write(data[2]);

  delta_x = 0;
  delta_y = 0;
}

int mousecommand(int command) {
  unsigned char val;

  //This implements enough mouse commands to get by, most of them are
  //just acked without really doing anything

  switch (command) {
  case 0xFF: //reset
    ack();
    //the while loop lets us wait for the host to be ready
    while(mouse.write(0xAA)!=0);  
    while(mouse.write(0x00)!=0);
  
    break;
  case 0xFE: //resend
    ack();
    break;
  case 0xF6: //set defaults 
    //enter stream mode   
    ack();
    break;
  case 0xF5:  //disable data reporting
    //FM
    ack();
    break;
  case 0xF4: //enable data reporting
    //FM
    enabled = 1;
    ack();
    Serial.println("Now Enabled.");
    break;
  case 0xF3: //set sample rate
    ack();
    mouse.read(&val); // for now drop the new rate on the floor
    Serial.print("Set sample rate: ");
    Serial.println(val);

    //      Serial.println(val,HEX);
    ack();
    break;
  case 0xF2: //get device id
    ack();
    mouse.write(00);
    break;
  case 0xF0: //set remote mode 
    ack();  
    break;
  case 0xEE: //set wrap mode
    ack();
    break;
  case 0xEC: //reset wrap mode
    ack();
    break;
  case 0xEB: //read data
    ack();
    write_packet();
    break;
  case 0xEA: //set stream mode
    ack();
    break;
  case 0xE9: //status request
    ack();
    //      send_status();
    break;
  case 0xE8: //set resolution
    ack();
    mouse.read(&val);
    //    Serial.println(val,HEX);
    ack();
    break;
  case 0xE7: //set scaling 2:1
    ack();
    break;
  case 0xE6: //set scaling 1:1
    ack();
    break;

  } 
  
}

int xcenter ;
int ycenter;

int xsum = 0;
int ysum = 0;

void(* resetFunc) (void) = 0; //declare reset function @ address 0

void setup() {
  unsigned char val;
  Serial.begin(9600);
  Serial.println("Just started...");

  pinMode(ps2PowerPin, INPUT); 

  while (digitalRead(ps2PowerPin) == LOW)
    delay(5);
  Serial.println("power is on...");
  // send the mouse start up
  while(mouse.write(0xAA)!=0);  
  while(mouse.write(0x00)!=0);
  //Serial.write("whiles ended");
  //delay(5000);
  //Serial.write("whiles ended agian. ");

  
  
}



void loop() {
  if (digitalRead(ps2PowerPin) == LOW)
    resetFunc();

  unsigned char  c;
  if( (digitalRead(3)==LOW) || (digitalRead(2) == LOW)) {
    while(mouse.read(&c)) ;
    mousecommand(c);
  } 

  if (enabled) {
    // move the mouse diagonally

    int32_t sumX = 0;
    int32_t sumY = 0;
    while (Serial.available() >= 9) { // Check if at least 8 bytes are available to read (two 32-bit integers)
      int32_t int1, int2;
      Serial.readBytes((char*)&int1, sizeof(int1));
      Serial.readBytes((char*)&int2, sizeof(int2));
      sumX += int1;
      sumY += int2;

      int8_t mouseButtons;
      Serial.readBytes((char*)&mouseButtons, sizeof(mouseButtons));

      buttons[0] = mouseButtons & 1; // first bit, mouse1
      buttons[1] = (mouseButtons >> 1) & 1; // second bit, mouse2
      buttons[2] = (mouseButtons >> 2) & 1; // third bit, mouse3

    }

    if (sumX != 0 || sumY != 0)
    {
      Serial.print("delta X: ");
      Serial.print(sumX);
      Serial.print("   delta Y: ");
      Serial.println(sumY);
    }
    delta_x = sumX;
    delta_y = sumY;
    write_packet();
    
  }
  else {
    Serial.print("Not enabled...");
  }
  delay(50);

}
