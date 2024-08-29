#define LEDPIN 11
void setup() {
  // put your setup code here, to run once:
  pinMode(LEDPIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(LEDPIN, !digitalRead(LEDPIN));
  delay(500);
}
