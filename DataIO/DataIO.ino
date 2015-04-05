int val = 0; // variable to store value read at analog pin 3
int inbyte;
int val1;
void setup()
{
  // initialize serial comms
  Serial.begin(9600); 
}
 
void loop()
{
  inbyte = 0;
  inbyte = Serial.read();
  //while(inbyte != 1){
    //inbyte = Serial.read();
  //}
  // read A0
  val1 = analogRead(0);
  // print to serial
  Serial.print(val1);
  Serial.print("\n");
  // wait 
  delay(50);
}
