int sampleTime = 0; // Time of last sample (in Sampling tab)
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
bool sending;

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  sending = false;
  writeDisplay("Sleep", 0, true);
}

void loop() {
  String command = receiveMessage();
  if(command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
  }
  else if(command == "wearable") {
    sending = true;
    // String timeString = String(timeLeft);
    // writeDisplay(timeString.c_str(), 0, true);
    writeDisplay("Wearable", 0, true);
  }
  else {
    String hold = "Steps :";
    String cmd = String(hold + command);
    writeDisplay(cmd.c_str(), 0, false);
  }
  if(sending && sampleSensors()) {
    String response = String(millis()) + "," + String(analogRead(0)) + "," + String(analogRead(1)) + "," + String(analogRead(2));
    sendMessage(response);    
  }
}
