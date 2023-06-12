#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>



const char* wifiName = "cse16";
const char* wifiPass = "285028502";
String state = "-100";
int relay = 2;
//Web Server address to read/write from
String serverName = "http://192.168.43.62:8000/";

void setup() {

  Serial.begin(9600);
  delay(10);
  Serial.println();
  
  pinMode(relay, OUTPUT); //D4
  digitalWrite(relay, HIGH);


  
  Serial.print("Connecting to ");
  Serial.println(wifiName);

  WiFi.begin(wifiName, wifiPass);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());   //You can get IP address assigned to ESP
}

void loop() {
  WiFiClient client;
  HTTPClient http;    //Declare object of class HTTPClient

  Serial.print("Request Link:");

  String link = serverName + "check/";
  Serial.println(link);

  http.begin(client, link.c_str());    //Specify request destination

  int httpCode = http.GET();            //Send the request
  String payload = http.getString();    //Get the response payload from server

  Serial.print("Response Code:"); //200 is OK
  Serial.println(httpCode);   //Print HTTP return code

  Serial.print("Returned data from Server:");
  Serial.println(payload);    //Print request response payload

  if (httpCode == 200)
  {
    // Allocate JsonBuffer
    // Use arduinojson.org/assistant to compute the capacity.
    const size_t capacity = JSON_OBJECT_SIZE(3) + JSON_ARRAY_SIZE(2) + 60;
    DynamicJsonBuffer jsonBuffer(capacity);

    // Parse JSON object
    JsonObject& root = jsonBuffer.parseObject(payload);
    if (!root.success()) {
      Serial.println(F("Parsing failed!"));
      return;
    }

    // Decode JSON/Extract values
    Serial.println(F("Response:"));
    state = root["state"].as<char*>();
    Serial.println(root["state"].as<char*>());
  }
  else
  {
    Serial.println("Error in response");
  }

  http.end();
  delay(2000);

  if (state == "1")
  {
    Serial.println("on machine");


    digitalWrite(relay, LOW);

    delay(6000);

    digitalWrite(relay, HIGH);



    String link = serverName + "machine/0/";
    Serial.println(link);

    http.begin(client, link.c_str());    //Specify request destination

    int httpCode = http.GET();            //Send the request
    String payload = http.getString();    //Get the response payload from server

    Serial.print("Response Code:"); //200 is OK
    Serial.println(httpCode);   //Print HTTP return code

    Serial.print("Returned data from Server:");
    Serial.println(payload);    //Print request response payload

  }

  //GET Data at every 5 seconds
}
