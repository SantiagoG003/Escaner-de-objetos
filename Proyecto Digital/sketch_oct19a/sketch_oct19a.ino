#include <SoftwareSerial.h>
#include <DFRobotDFPlayerMini.h>

SoftwareSerial mySerial(16, 17); // RX, TX
DFRobotDFPlayerMini myDFPlayer;

void setup() {
  Serial.begin(9600); // Comunicación serial con la PC
  mySerial.begin(9600); // Comunicación serial con DFPlayer Mini

  if (!myDFPlayer.begin(mySerial)) {
    Serial.println("DFPlayer Mini no iniciado");
    while (true);
  }
  
  myDFPlayer.volume(20);  // Ajustar el volumen (0-30)
  Serial.println("DFPlayer Mini iniciado");
}

void loop() {
  if (Serial.available() > 0) {
    String objeto = Serial.readStringUntil('\n');
    
    if (objeto == "vaso") {
      myDFPlayer.play(1);  // Reproducir el archivo 0001.mp3
    }
    // Puedes añadir más objetos y reproducir sus respectivos archivos de audio.
  }
}
