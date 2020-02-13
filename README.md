# PlantGrower
Arduino and raspberryPI auto cannabis grower

**
Note: the program currently only displays the temperature and humidity 
**

Add arduinoPi.ino to your arduino with a temperature and humidity sensor attached to pin 9, make sure your arduino is ACM0 on your
raspberryPi. Do this by running 'ls /deb/tty*' in the terminal on your PI
If your ACM is different on your pi, you can change the Serial port on line 8 of the ui.py

Run the ui.py through terminal to start the program.
