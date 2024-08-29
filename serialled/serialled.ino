#define LEDPIN 11

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);

  pinMode(LEDPIN, OUTPUT);
}

void loop(){
  if(Serial1.available()>0){
    String str = Serial1.readString().substring(0);
    Serial.println(str);
    if(str == "LED_ON"){
      digitalWrite(LEDPIN, HIGH);
      Serial.println("LED ON");
    }
    else if(str == "LED_OFF"){
      digitalWrite(LEDPIN, LOW);
      Serial.println("LED OFF");
    }
  }
}