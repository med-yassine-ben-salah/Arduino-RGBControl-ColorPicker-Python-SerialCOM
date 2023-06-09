const int redPin = 9;
const int greenPin = 10;
const int bluePin = 11;

void setup() {
  Serial.begin(9600);
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String rgbString = Serial.readStringUntil('\n');
    rgbString.trim();

    int commaIndex = rgbString.indexOf(',');
    if (commaIndex != -1) {
      int redValue = rgbString.substring(0, commaIndex).toInt();
      rgbString = rgbString.substring(commaIndex + 1);

      commaIndex = rgbString.indexOf(',');
      if (commaIndex != -1) {
        int greenValue = rgbString.substring(0, commaIndex).toInt();
        int blueValue = rgbString.substring(commaIndex + 1).toInt();

        analogWrite(redPin, redValue);
        analogWrite(greenPin, greenValue);
        analogWrite(bluePin, blueValue);
      }
    }
  }
}
