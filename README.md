# IFN649 2024 S2
### Benjamin Barrera

## Assignment 2
Assignment 2 code located in "Assignment" folder  
Device description:  
Controls interior temperature of house by opening/closing windows.  
Places temperature sensors inside and outside the house.  
 - Teensy layer (Tier 1):
   - Reads temperature from temperature sensor every 2 seconds and immediately sends via serial over bluetooth to Raspberry pi .
 - Raspberry pi layer (Tier 2):  
   - collects temperature readings from all bluetooth sensors, and, at a specified interval, calculates average temperature over a period of time for each sensor.  
   - The average temperature readings are sent to tier 3 AWS.
 - AWS layer (Tier 3):
   - Received data from raspberry pi
   - target temperature is set here
   - calculation for recommendation is calculated here
   - result is published via mqtt so that mobile phone app can subscribe to it for mobile notifications (app used: https://play.google.com/store/apps/details?id=de.radioshuttle.mqttpushclient)
 - Not yet implemented:
   - Automatic opening and closing of windows
   - Take forecast into account
   - Data visualisation/GUI interface
