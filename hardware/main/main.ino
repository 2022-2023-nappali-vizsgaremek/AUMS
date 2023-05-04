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

byte* stringToBytes(const char* str)
{
    static byte bytes[20];

    for (uint8_t i = 0; i < 20; ++i)
    {
        bytes[i] = strtoul(str, NULL, 16);

        str += 2;
        if (*str == ':') ++str;
    }
    return bytes;
}

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

WiFiClientSecure secureClient;

void loop()
{
    if (!rfid.PICC_IsNewCardPresent()) return;
    if (rfid.PICC_ReadCardSerial())
    {
        for (byte i = 0; i < 4; i++)
        { tag += rfid.uid.uidByte[i]; }

        digitalWrite(D1, HIGH); delay(250);
        digitalWrite(D1, LOW);

        String url = String(server) + tag;

        secureClient.setInsecure();
        http.begin(secureClient, url);

        http.addHeader("Content-Type", "application/x-www-form-urlencoded");
        http.addHeader("Authorization", "Bearer OOkbqF8pliyFSWOQOti45PsQfkUTqMfc9MY2w0WshjbyM8li98ffW1eC2xz4kLhscoxSfQI8ajVS2lRRZH8Dqbx6AnvMS6rYhwfjwtVhyAsRSTcVIlnwT9dIGqWnd59f");

        int httpCode = http.POST("");

        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_CREATED)
        {
            if (httpCode == HTTP_CODE_OK)
            {
                digitalWrite(D0, HIGH);
                delay(1500);
                digitalWrite(D0, LOW);
            }
            else if (httpCode == HTTP_CODE_CREATED)
            {
                digitalWrite(D1, HIGH);
                delay(1500);
                digitalWrite(D1, LOW);
            }
        }
        else
        {
            digitalWrite(D2, HIGH);
            delay(1500);
            digitalWrite(D2, LOW);
        }

        http.end();

        tag = "";
        rfid.PICC_HaltA();
        rfid.PCD_StopCrypto1();
    }
}