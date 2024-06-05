#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN      A0        
#define SS_PIN       10        

MFRC522 mfrc522(SS_PIN, RST_PIN); 

void setup() {
  Serial.begin(9600);

  SPI.begin();
  mfrc522.PCD_Init();  
}

void loop() {
    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
      String s="";
      byte *id = mfrc522.uid.uidByte;   
      byte idSize = mfrc522.uid.size;  
      MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
  
      for (byte i = 0; i < idSize; i++) { 
        s += String(id[i],BIN);
      }
      Serial.println(s);

      delay(500);
    } 
}
