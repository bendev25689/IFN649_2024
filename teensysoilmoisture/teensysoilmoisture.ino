#define LEDPIN 11
#define SOILPIN 20

void setup() {
  // put your setup code here, to run once:
  pinMode(LEDPIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  int soilVal = analogRead(SOILPIN);
  Serial.print("Soil: ");
  Serial.println(soilVal);
  digitalWrite(LEDPIN, HIGH);
  delay(1000);
  digitalWrite(LEDPIN, LOW);
  delay(100);
}
