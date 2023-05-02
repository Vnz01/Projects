const int accelX = A0;
const int accelY = A1;
const int accelZ = A2;
int ctr = 0;
float accelerationThreshold = 3;

void setupAccelSensor() {
  pinMode(accelX, INPUT);
  pinMode(accelY, INPUT);
  pinMode(accelZ, INPUT);
}

int detectShaking(){
  int xRaw = analogRead(accelX);
  int yRaw = analogRead(accelY);
  int zRaw = analogRead(accelZ);
  float xAccel = (xRaw - 512.0) / 100.0; // convert to acceleration in g
  float yAccel = (yRaw - 512.0) / 100.0;
  float zAccel = (zRaw - 512.0) / 100.0;
  delay(100);
  int nxRaw = analogRead(accelX);
  int nyRaw = analogRead(accelY);
  int nzRaw = analogRead(accelZ);
  float nxAccel = (nxRaw - 512.0) / 100.0; // convert to acceleration in g
  float nyAccel = (nyRaw - 512.0) / 100.0;
  float nzAccel = (nzRaw - 512.0) / 100.0;
  if (abs(nxAccel - xAccel) > accelerationThreshold || abs(nyAccel - yAccel) > accelerationThreshold || abs(nzAccel - zAccel) > accelerationThreshold) {
    return 1;
  } else {
    return 0;
  }
}


int detectGesture(){
  int ax = analogRead(accelX); // takes reading from accelerometer
  int ay = analogRead(accelY);
  int az = analogRead(accelZ);

  float sensitivity = 75; // Sensitivity of accelerometer in mV/g
  int accX = (ax - 512) * sensitivity / 1000.0; // Convert x value to acceleration in g
  int accY = (ay - 512) * sensitivity / 1000.0; // Convert y value to acceleration in g
  float accZ = (az - 512) * sensitivity / 1000.0; // Convert z value to acceleration in g
  if(detectShaking()){
    return 2;
  } else {
    if(ax < az && ay < az){ // if acceleration is less than 1 and Z value is greater than both x and y
    ctr++; // then it means that it is rightside up
    if(ctr >= 10) {
      ctr = 0;
      return 0;
    }
  } else if(ax > az && ay > az){ // same for this but if z is less than it is the other way aroumd
    ctr++;
    if(ctr >= 10) {
      ctr = 0;
      return 1;
    }
  }
  }
}
