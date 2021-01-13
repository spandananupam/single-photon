int pin = 7;
unsigned long period;
unsigned long timeRes = 100;
int numPulses = 0;
unsigned long timeStart = millis();

void setup() {
  Serial.begin(9600);
  pinMode(pin, INPUT);
}

void loop() {
  if (millis() - timeStart >= timeRes) {
    Serial.println(numPulses);
    numPulses = 0;
    timeStart = timeStart + timeRes; 
  }
  period = pulseIn(pin, HIGH);
  if (period > 0) {
    numPulses++;
  }
}
