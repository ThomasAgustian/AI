int Buzzer = 5 ;// Buzzer
int LED_Male = 6; // Pin LED_Male
int LED_Female = 7; // Pin LED_Female
int LED_Warning = 8; // Pin LED_Warning
char genderAllowed = 'F';

void setup() {
  Serial.begin(9600); // Baud rate serial harus sama dengan di Python (9600)
  pinMode(LED_Male, OUTPUT);
  pinMode(LED_Female, OUTPUT);
  pinMode(LED_Warning, OUTPUT);
  pinMode(Buzzer, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char incomingByte = Serial.read(); // Baca input serial
    
    if (incomingByte == 'M' && incomingByte == genderAllowed) { // Laki-laki
      digitalWrite(LED_Male, HIGH); // LED menyala
      delay(500);
      digitalWrite(LED_Male, LOW); // LED mati
    } 
    else if (incomingByte == 'F' && incomingByte == genderAllowed) { // Perempuan
      digitalWrite(LED_Female, HIGH); // LED menyala
      delay(500);
      digitalWrite(LED_Female, LOW); // LED mati
    }
    else if (incomingByte != genderAllowed) {
      digitalWrite(LED_Warning, HIGH); // LED menyala
      tone(Buzzer, 2000);
      delay(500);
      digitalWrite(LED_Warning, LOW); // LED mati
      noTone(Buzzer);
    }
  }
}