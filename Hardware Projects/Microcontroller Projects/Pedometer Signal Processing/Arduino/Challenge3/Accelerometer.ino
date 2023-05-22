const int accelX = A0;
const int accelY = A1;
const int accelZ = A2;
void setupAccelSensor() {
  pinMode(accelX, INPUT);
  pinMode(accelY, INPUT);
  pinMode(accelZ, INPUT);
}
void readAccelSensor() {
  int ax = analogRead(accelX);
  int ay = analogRead(accelY);
  int az = analogRead(accelZ);
  Serial.print(ax);
  Serial.print(",");
  Serial.print(ay);
  Serial.print(",");
  Serial.println(az);
  return(ax,ay,az);
}