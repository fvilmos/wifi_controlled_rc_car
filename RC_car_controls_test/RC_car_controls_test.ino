/************************************************************************** 
RC car control test SW
Activates the ESP-01 module GPIO pints for 1s HIGH then LOW 
To be used to test the remote control to ESP-01 connection and wiring

Author: fvilmos, https://github.com/fvilmos
***************************************************************************/

void setup() 
{
  /* set up the l4 pins as output */
  pinMode(0, OUTPUT);
  pinMode(1, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
}

void loop() 
{

    /* keep 1s low 1s high the pin*/
    for (byte i=0; i<4; i++)
    {
      digitalWrite(i, LOW);
      delay(1000);
      digitalWrite(i, HIGH);
      delay(1000);      
    }

}