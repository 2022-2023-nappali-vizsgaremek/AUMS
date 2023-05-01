#include <SPI.h>
#include <MFRC522.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <WiFiClientSecure.h>
#include <ESP8266HTTPClient.h>

constexpr uint8_t SS_PIN = D4;
constexpr uint8_t RST_PIN = D3;

const char* ssid = "AUMS";
const char* password = "PROJ-AUMS";
const char* server = "https://api.proj-aums.hu/card_validation/";

String tag;
MFRC522::MIFARE_Key key;
MFRC522 rfid(SS_PIN, RST_PIN);

HTTPClient http;

void setup()
{
    Serial.begin(9600);

    SPI.begin();
    rfid.PCD_Init();

    pinMode(D0, OUTPUT);
    pinMode(D1, OUTPUT);
    pinMode(D2, OUTPUT);

    digitalWrite(D0, HIGH); delay(250);
    digitalWrite(D1, HIGH); delay(250);
    digitalWrite(D2, HIGH); delay(250);
    delay(1500);
    digitalWrite(D0, LOW); delay(250);
    digitalWrite(D1, LOW); delay(250);
    digitalWrite(D2, LOW); delay(250);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        digitalWrite(D1, HIGH); delay(250);
        digitalWrite(D1, LOW); delay(250);
    }
}

void loop()
{
    if (!rfid.PICC_IsNewCardPresent()) return;
    if (rfid.PICC_ReadCardSerial())
    {
        for (byte i = 0; i < 4; i++)
        { tag += rfid.uid.uidByte[i]; }

        digitalWrite(D1, HIGH); delay(250);
        digitalWrite(D1, LOW);

        WiFiClientSecure client;
        client.setInsecure();

        if (client.connect("api.proj-aums.hu", 443))
        {
            String request = "POST " + String(server) + tag + " HTTP/1.1\r\n" +
                "Content-Type: application/x-www-form-urlencoded\r\n" +
                "Host: api.proj-aums.hu\r\n" +
                "Content-Length: 0\r\n\r\n";

            client.print(request);

            unsigned long timeout = millis();
            while (client.available() == 0)
            {
                if (millis() - timeout > 10000)
                {
                    client.stop();
                    return;
                }
            }

            String response = client.readStringUntil('\r');
            if (response.indexOf("200 OK") > 0)
            {
                digitalWrite(D0, HIGH);
                delay(1500);
                digitalWrite(D0, LOW);
            }
            else if (response.indexOf("201 Created") > 0)
            {
                digitalWrite(D1, HIGH);
                delay(1500);
                digitalWrite(D1, LOW);
            }
            else
            {
                digitalWrite(D2, HIGH);
                delay(1500);
                digitalWrite(D2, LOW);
            }

            client.stop();
        }
        else
        {
            for (int i = 0; i < 3; i++)
            {
                digitalWrite(D1, HIGH); delay(250);
                digitalWrite(D1, LOW); delay(250);
            }
        }

        tag = "";
        rfid.PICC_HaltA();
        rfid.PCD_StopCrypto1();
    }
}