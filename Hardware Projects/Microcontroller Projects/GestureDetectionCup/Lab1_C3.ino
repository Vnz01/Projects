int currentState = -1;
int previousState = -1;
int timeLeft = 0;
int rstPressed = 0;
int addPressed = 0;
unsigned long start = 0;
const int buzz = 4;

void setup() {
  Serial.begin(9600);
    setupDisplay();
    pinMode(buzz, OUTPUT);
}

void loop() {
  currentState = detectGesture(); // currentState is taken from detectGesture
  if(currentState != previousState) {
    Serial.println(currentState);  
  }
   // if previous state isn't equal to current state then execute
    if(currentState == 0){ // if current state is 0 then print the state and so forth for 1 and 2
    if(timeLeft == 0 && !rstPressed && addPressed){
    digitalWrite(buzz, HIGH);
  } else if(timeLeft > 0) {
  if(start == 0){
    start = millis();
  }
  if (millis() - start >= 1000) { // increments time passed by 1 every second no matter what
    timeLeft--;
    String timeString = String(timeLeft);
    writeDisplay(timeString.c_str(), 0, true);
    start = millis();
  }
  }
    }else if(currentState == 1){
    delay(300);
    timeLeft++;
    String timeString = String(timeLeft);
    writeDisplay(timeString.c_str(), 0, true);
    addPressed = 1;
    rstPressed = 0;
    start = 0;
    }else if(currentState == 2 && rstPressed == 0){
    timeLeft = 0;
    String timeString = String(timeLeft);
    writeDisplay(timeString.c_str(), 0, true);
    rstPressed = 1;
    digitalWrite(buzz, LOW);
  }
  previousState = currentState; // at end of code set previousState to currentState then another loop starts
}
