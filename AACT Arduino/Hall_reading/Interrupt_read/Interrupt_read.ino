/*
The purpose of this file is to use interrupts to increment a counter.

In the future this file will be combined with the analogWriting file in order to make a program that 
is able to drive the CMG and take inputs from the hall sensors simultaneously 

This was initially tested with a button that is not debounced in anyway
*/

const byte Hall_Pin = 2;//counted sensor hooked upt to pin 2
int count;//values for reading hall output



boolean read = false;//used as a flag for the ardu to decide whether to print or not
const byte Read_Pin = 3;//the read pin will be pin 3

void setup() {
  //attach an interrupt to the Hall pin
  pinMode(Hall_Pin, INPUT);
  attachInterrupt(digitalPinToInterrupt(Hall_Pin), add, RISING);
  
  //attach an interrupt to the read pin
  pinMode(Read_Pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(Read_Pin), reader, RISING);

  //print results to the serial monitor
  Serial.begin(9600);
  Serial.print("Setup Complete\n");
}

void loop() {
 
  if(read){
    Serial.print("Count = ");
    Serial.println(count);
    count = 0;
    read = false;
  }
}

//ISR for pin 2
void add() {
  count++;
}

//ISR for pin 3
void reader(){
  read = true;
}
