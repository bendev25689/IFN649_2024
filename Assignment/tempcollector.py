import paho.mqtt.publish as publish
import serial

#config
mqttsubject = "ifn649" #subject tag for mqtt
mqttip = "54.252.141.222" #ip address of mqtt server
interval = 5 #calculate average and publish every x samples
numsensors = 3 #number of sensors in the system
       #serial addresses for each teensy device
teensys = [serial.Serial('/dev/rfcomm0', timeout=5), serial.Serial('/dev/rfcomm1', timeout=5), serial.Serial('/dev/rfcomm2', timeout=5)]

#non-config
tempstotal = [0] * numsensors #used to store sum of raw data for each sensor
tempscount = [0] * numsensors #used to store a count of number of samples added to tempstotal

#read message from specified serial device, and parse
def read_message(serDevice):
  msg = serDevice.readline().decode('ascii').rstrip() #decode ascii and remove trailing spaces and \r \n characters
  end = len(msg)-1 #find end
  if(len(msg) >0):
    if(msg[0] == '[' and msg[end] == ']'):
      outlist = msg[1:end-1].split(",")
    else:
      outlist = []
  else: #if not, set to empty
    outlist = []
  return outlist

while(1):
  for teensy in teensys: #for each teensy serial device
    indata = read_message(teensy) #read data
    if(len(indata) == 0): #check if data was received. If not, skip this iteration of the foor loop
      print("Error: no data received for " + teensy.port)
      continue
    #cast each item to correct data type and place in variable
    id = int(indata[0])
    hum = float(indata[1])
    temp = float(indata[2])
    hind = float(indata[3])
    print("Teensy " + str(id) + " Temp: " + str(temp) + "C Humidity: " + str(hum) + "% Heat Index: " + str(hind) + "C")
    #add to variables for eventual calculation of average
    tempstotal[id-1] += temp
    tempscount[id-1] += 1
  #after specified number of samples, calculate average and publish to mqtt.
  #uses count of first sensor. (Assumes there is always a sensor 0).
  if(tempscount[0] >= interval):
    for i in range(0,len(tempscount)):
        average = tempstotal[i]/tempscount[i]
        tempstotal[i] = 0
        tempscount[i] = 0
        topublish = "[" + str(i) + "," + str(average) + "]"
        print(average)
        publish.single(mqttsubject, topublish, hostname=mqttip)


#close on exit. (note: to implement: catch interrupt signal for clean exit)
for teensy in teensys:
  teensy.close()
