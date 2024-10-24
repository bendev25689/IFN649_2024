#Configuration
numsensors = 3 #number of sensor modules in the system
target = 25 #target inside temperature
inside = [2] #list of sensors located inside (by index)
outside = [0,1] #list of sensors located outside (by index)
mqttip = "54.252.141.222"

#non-configurable
temps = [0] * numsensors #create empty array for raw temperature values
lastrec = "" #last window action, to prevent repeated command/notification

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

def on_connect(client, userdate, flags, rc): #advise of connection status, run on connection attempt
  print("Connected to MQTT")
  print("Connection returned result: " + str(rc))
  client.subscribe("ifn649")
def on_message(client, userdata, msg): #run each time a message is received
  global numsensors,temps,target,hyst,inside,outside,lastrec,mqttip #specify global scope for variables
  data = msg.payload.decode('ascii').rstrip() #decode incoming message and remove drailing space and \r \n characters
  end = len(data)-1 #find end
  if(len(data) > 0):
    if(data[0] == "[" and data[end] == "]"): #check if string is data, if so: parse.
      datalist = data[1:end-1].split(",")
      datalist[0] = int(datalist[0])
      datalist[1] = float(datalist[1])
      temps[datalist[0]] = datalist[1]
      print(datalist[1])
    else:
      print("not data")
      return
  else: #if not data, skip this cycle
    print("not data")
    return
  intemp = 0
  outtemp = 0
  #find average of all inside sensors
  for i in inside:
    intemp += temps[i]
  intemp = intemp / len(inside)
  #find average of all outside sensors
  for i in outside:
    outtemp += temps[i]
  outtemp = outtemp / len(outside)
  #check if data is present for all sensors, to prevent sending recommendation prematurely.
  zeroitems = 0
  for temp in temps:
    if temp == 0:
      zeroitems += 1
  if zeroitems == 0:
    if((outtemp <= intemp and intemp >= target) or (outtemp >= intemp and intemp <= target)): #open window if outside temperature would adjust inside temperature towards target.
      if lastrec is not "Open": #only send command/notification if different to previous command
        print("Open Windows. Outside: " + str(int(outtemp)) + "C Inside: " + str(int(intemp)) + "C")
        publish.single("notification", "Open Windows.\nOutside: " + str(int(outtemp)) + "C Inside: " + str(int(intemp)) + "C", hostname=mqttip)
        lastrec="Open"
    else: #otherwise, close the window.
      if lastrec is not "Close": #only send command/notification if different to previous command
        print("Close Windows. Outside: " + str(int(outtemp)) + "C Inside: " + str(int(intemp)) + "C")
        publish.single("notification", "Close Windows.\nOutside: " + str(int(outtemp)) + "C Inside: " + str(int(intemp)) + "C", hostname=mqttip)
        lastrec="Close"

#connect to mqtt, and run forever.
client=mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqttip, 1883, 60)
client.loop_forever()
