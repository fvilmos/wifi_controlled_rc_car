/************************************************************************** 
RC car control
Enstabilish a WiFi connection to the local network,
than wait for commands.

list commands: http://ip_address/
command format: http://ip_address/set/p[0..3]&duration=[0..,10000]
separate commands with '&'


pass commands like: 
http://x.x.x.x/set?p0=1&p2=1&duration=1000 => 2 buttons pressed for 1s
http://x.x.x.x/set?p0=1&duration=500 => 1 button pressed for 0.5s

or (using DNS)
http://esprccar.local/set?p0=1&duration=500

Author: fvilmos, https://github.com/fvilmos
***************************************************************************/

/*includes*/
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

/*constants and variables*/

/*Wi-Fi SSID*/
const char * ssid = "SSID"; /* <- update here with SSID */
const char * password =  "PASSW"; /* <- upate here with password */

/*web server object*/
ESP8266WebServer server(80);
MDNSResponder mdns;

/*put ports on the initioal state*/
void reset_gpios()
{
  /* init the pins*/
  for (byte i=0; i<4; i++)
  {
    digitalWrite(i, HIGH);  
  }
}

/*handle root, list content*/
void cb_root()
{
  String info ="\nRC car control \nEnstabilish a WiFi connection to the local network, than wait for commands.\nlist commands: http://ip_address/ \ncommand format: http://ip_address/set/p[0..3]&duration=[0..,10000] \n\npass commands like: \nhttp://x.x.x.x/set?p0=1&p2=1&duration=1000 => 2 buttons pressed for 1s \nhttp://x.x.x.x/set?p0=1&duration=500 => 1 button pressed for 0.5s\n\n\nAuthor: fvilmos, https://github.com/fvilmos";
  server.send(200, "text/plain", info);
}

void cb_set()
{
  String message = "Arguments:";
  byte ports[]={0,0,0,0};
  int duration=0;
  byte val = 0;

  message += server.args();
  message += "\n";

  for (int i = 0; i < server.args(); i++) 
  {
    message += server.argName(i) + ": ";
    message += server.arg(i) + "\n";
    val = (byte)atoi(server.arg(i).c_str());


    /*search for ports*/
    if (strcmp(server.argName(i).c_str(),"p0") == 0)
    {
      ports[0]=val;
    }
    
    if (strcmp(server.argName(i).c_str(),"p1") == 0)
    {
      ports[1]=val;
    }
    
    if (strcmp(server.argName(i).c_str(),"p2") == 0)
    {
      ports[2]=val;
    }
    
    if (strcmp(server.argName(i).c_str(),"p3") == 0)
    {
      ports[3]=val;
    }

    if (strcmp(server.argName(i).c_str(),"duration") == 0)
    {
      duration= atoi(server.arg(i).c_str());
    }

  }

  /*write values to the GPIOs, wait, than reset*/
  for (byte i=0; i<4; i++)
  {
    if (ports[i]==1)
    {
      digitalWrite(i, LOW);
    }
    else
    {
      digitalWrite(i, HIGH);
    }
  }
  delay(duration);
  reset_gpios();
  
  server.send(200, "text/plain", message); 
}

/*implement callback for unknown requests*/
void cb_not_found()
{
  server.send(200, "text/plain", "command not understood!");
}

/*setup*/
void setup() 
{
  /* set up the 4 pins as output */
  pinMode(0, OUTPUT);
  pinMode(1, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);

  /* init the pins*/
  reset_gpios();

  /*connect to the WiFI*/
  WiFi.begin(ssid, password);

  /*wait till get connected*/
  while (WiFi.status() != WL_CONNECTED) 
  {
      delay(500);
  }

  mdns.begin("esprccar", WiFi.localIP());

  /*add callbacks*/
  server.on("/", HTTP_GET, cb_root); /*callback get*/
  server.on("/set",HTTP_GET,cb_set); /*callback set*/
  server.onNotFound(cb_not_found);   /*callback not found*/
  server.begin();

  /*solve MDNS name, name.local*/
  mdns.addService("http","tcp", 80);

}

/*main*/
void loop() 
{
  mdns.update();
  server.handleClient();
}

