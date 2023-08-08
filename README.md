### WiFi controlled RC car

This project offers an easy way to control a cheap RC car over WiFi using HTTP GET commands, sent from a web browser or python file. The implementation provides a convenient solution for vision or Machine Learning applications (ex. reinforcement learning) to test the developed models in the real world, not just in a simulator.

<p align="center"> 
    <img src="/info/car.jpg" width="400">
<div align="center">"Drift tin car", cheap RC car with hacked WiFi module esp8266-01</div>
</p>

#### WiFi features
- mDNS support, the RC car easily can be accessed through local the network: "http://esprccar.local/"
- button combinations allowed (like forward + turn left)
- selectable "virtual press" duration

#### Command set - browser

To list all available features, just access the http://esprccar.local/ location, by default an info page will be returned as plain text.
Commands can be composed according to the needs, using the "set" query parameters. After a command was sent, an HTTP response on the processed parameters and values is returned.

<p align="center"> 
    <img src="/info/cmd.jpg" width="500">
</p>

```
Command structure:

http://esprccar.local/set?p0=1&duration=1000&p3=1
- set - command to set the port values
- p0...p3 - selectable ports, can be combined according to the needs
- duration - in [ms] defines the pin activation time (pulse LOW to HIGH and back)
- query starts with "?", more commands can be combined using "&". i.e. ...?p0=1&p3=1&p2=1&duration=1000
- sending values without 'duration' variable, set the port value to 1/0. 
```
#### Command set  - application

A basic python GUI application is provided, see ```basic_gui.py```, to demostrate how to drive the RC car using the keyboard.
<p align="center"> 
    <img src="/info/gui.jpg" width="320">
<div align="center">basic gui</div>
</p>

By pressing the ```q,w,e,a,s,d``` keys the car will move like with the original remote control. If duration set from the trackbar, the key pressed will be reseted after a period of time. Letting the value on zero, allows the key repetitions.
```Note: q - left+forward, w - forward, e - right+forward, a-left, s-backward, d - right```

The application provides a simple ```cmd_api``` function, that can be used to send commands from the python file.
```cmd_api("0001") - will set the ports p3=0, p2=0, p1=0, p0=1```
```cmd_api("xx01") - will set the ports p1=0, p0=1, while ignores p3, p2 settings```



### HW preparation
- esp-01 module + programmer [1]
- 1kOhm resitor for CH_PF pin to Vcc
- 2x4 pin connector

<p align="center"> 
    <img src="/info/esp.jpg" width="400">
<div align="center">ESP8266-01, source:[2]</div>
</p>

Identify the button pins, see the picture below, and pins from ESP01 module above [2].

We will need to wire:
- GND to the ground (- balck wire)
- Vcc to the 3V (+ red wire)
- IO1, IO2, TXD, RXD to the button pins
- 1kOhm resistor, between esp Vcc and CH_PF pin
```Note: order of the GPIO pins does not matter, can be compensated from the SW.``` 

```Note: for more advanced RC controls, a set of relays or optocoupler can be added between the GPIOs and buttons. for This RC no galvanic separation was needed.```

<p align="center"> 
    <img src="/info/hw1.jpg" width="400">
    <img src="/info/hw.jpg" width="400">
<div align="center"></div>

After the wiring is ready, the ```RC_car_controls_test.ino``` code can be uploaded to test all the connections for the buttons to work.
If you are confident that all is working, edit the ```RC_car_wifi_control.ino``` project and put your local <b>```SSID```</b> for the WiFi and <b>```password```</b>.

##### Improvements
1. An on/off button could be added to separate the esp8266-01 from the permanent supply when connected to the RC.
2. Update the HW with the optocoupler variant for more generic use.
3. ~~Masking the set functions port parameters when processed in the SW.~~
4. ~~Send commands without the "duration" parameter to set permanently the GPIOs (on or off). In this way, the solution can be used for diverse IoT projects.~~

### Resources
1. [Flash Program ESP-01 using USB Serial Adapter](https://www.diyhobi.com/flash-program-esp-01-using-usb-serial-adapter/)
2. [ESP-01 802.11 b/g/n Wi-Fi Module](https://docs.ai-thinker.com/_media/esp8266/docs/esp-01_product_specification_en.pdf)
3. [HTTP Request Methods](https://www.w3schools.com/tags/ref_httpmethods.asp)
4. [send http requests as fast as possible in-python](https://skillshats.com/blogs/send-http-requests-as-fast-as-possible-in-python/)

/Enjoy.

