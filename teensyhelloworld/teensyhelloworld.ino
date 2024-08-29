
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("Hello, World!!!!!");
  Serial.println(millis()/1000);
  delay(1000);
}
