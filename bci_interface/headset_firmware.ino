/*
 * Cerebrum-V1: ESP32-S3 Firmware Boilerplate
 * 
 * Hardware: ADS1299 (8-Channel ADC)
 * Function: Reads neural signals and broadcasts via LSL.
 */

#include <SPI.h>

// Pin Definitions (Matching Build Plan)
const int ADS_CS = 10;
const int ADS_DRDY = 9;
const int ADS_START = 14;
const int ADS_RESET = 21;

void setup() {
  Serial.begin(115200);
  
  // Initialize Pins
  pinMode(ADS_CS, OUTPUT);
  pinMode(ADS_DRDY, INPUT);
  pinMode(ADS_START, OUTPUT);
  pinMode(ADS_RESET, OUTPUT);
  
  // Hardware Reset
  digitalWrite(ADS_RESET, LOW);
  delay(100);
  digitalWrite(ADS_RESET, HIGH);
  
  // Initialize SPI
  SPI.begin(12, 13, 11, 10); // SCLK, MISO, MOSI, SS
  SPI.beginTransaction(SPISettings(4000000, MSBFIRST, SPI_MODE1));
  
  Serial.println("[Headset] ADS1299 Initialized.");
}

void loop() {
  // Wait for Data Ready
  if (digitalRead(ADS_DRDY) == LOW) {
    readADSData();
  }
}

void readADSData() {
  digitalWrite(ADS_CS, LOW);
  
  // Read Status Byte (24 bits)
  for(int i=0; i<3; i++) SPI.transfer(0x00);
  
  // Read 8 Channels (24 bits each)
  for(int chan=0; chan<8; chan++) {
    long val = 0;
    byte b1 = SPI.transfer(0x00);
    byte b2 = SPI.transfer(0x00);
    byte b3 = SPI.transfer(0x00);
    
    // Convert 24-bit 2's complement to long
    val = (b1 << 16) | (b2 << 8) | b3;
    if (val & 0x800000) val |= 0xFF000000;
    
    // Serial Plotter Output for debugging
    if(chan == 0) {
      // Serial.println(val); 
    }
  }
  
  digitalWrite(ADS_CS, HIGH);
}
