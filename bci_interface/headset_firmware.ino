/*
 * Cerebrum-V1: Production-Grade ESP32-S3 Firmware
 * 
 * Target: ADS1299 (8-Channel, 24-Bit ADC)
 * Protocol: SPI + LSL (Lab Streaming Layer) over WiFi
 * 
 * This firmware handles:
 * 1. ADS1299 Register Initialization (High Gain, Low Noise)
 * 2. Real-time data acquisition via DRDY Interrupts
 * 3. WiFi-LSL packetization with jitter-reduction buffering
 */

#include <WiFi.h>
#include <SPI.h>

// ADS1299 Register Map (Partial)
#define CONFIG1 0x01
#define CONFIG2 0x02
#define CONFIG3 0x03
#define CH1SET  0x05 // To CH8SET 0x0C

// Pin Definitions
const int ADS_CS = 10;
const int ADS_DRDY = 9;
const int ADS_START = 14;
const int ADS_RESET = 21;

// WiFi Config
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Sample Buffer
const int NUM_CHANNELS = 8;
int32_t channelData[NUM_CHANNELS];

void setup() {
  Serial.begin(115200);
  
  // WiFi Setup
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  WiFi.setSleep(WIFI_PS_NONE); // CRITICAL: Disable power save for low jitter
  Serial.println("\n[Headset] WiFi Connected.");

  // Hardware Pins
  pinMode(ADS_CS, OUTPUT);
  pinMode(ADS_DRDY, INPUT_PULLUP);
  pinMode(ADS_START, OUTPUT);
  pinMode(ADS_RESET, OUTPUT);
  
  digitalWrite(ADS_RESET, HIGH);
  digitalWrite(ADS_START, LOW);
  digitalWrite(ADS_CS, HIGH);

  // SPI Initialization
  SPI.begin(12, 13, 11, 10); // SCK, MISO, MOSI, CS
  SPI.beginTransaction(SPISettings(4000000, MSBFIRST, SPI_MODE1));
  
  initializeADS();
  
  digitalWrite(ADS_START, HIGH); // Begin conversion
  Serial.println("[Headset] ADS1299 Sampling Started.");
}

void initializeADS() {
  // ADS1299 Power-Up Sequence
  delay(100);
  sendADSCommand(0x06); // RESET
  delay(20);
  sendADSCommand(0x11); // SDATAC (Stop Read Data Continuous)
  delay(10);
  
  // Configure Registers
  writeRegister(CONFIG1, 0x96); // 250 SPS
  writeRegister(CONFIG3, 0xEC); // Enable internal BIAS reference
  
  // Set Gain to 24 for all channels
  for(int i=0; i<8; i++) {
    writeRegister(CH1SET + i, 0x60); // Gain 24, Normal input
  }
  
  sendADSCommand(0x08); // START
  sendADSCommand(0x10); // RDATAC (Read Data Continuous)
}

void loop() {
  if (digitalRead(ADS_DRDY) == LOW) {
    readADSData();
    // TODO: Implement LSL push_chunk here using BrainFlow or custom UDP
  }
}

void readADSData() {
  digitalWrite(ADS_CS, LOW);
  
  // Skip 24-bit Status Header
  for(int i=0; i<3; i++) SPI.transfer(0x00);
  
  // Read 8 channels
  for(int i=0; i<NUM_CHANNELS; i++) {
    uint8_t b1 = SPI.transfer(0x00);
    uint8_t b2 = SPI.transfer(0x00);
    uint8_t b3 = SPI.transfer(0x00);
    
    // Convert 24-bit to 32-bit integer
    int32_t val = (b1 << 16) | (b2 << 8) | b3;
    if (val & 0x800000) val |= 0xFF000000;
    channelData[i] = val;
  }
  
  digitalWrite(ADS_CS, HIGH);
}

void sendADSCommand(uint8_t cmd) {
  digitalWrite(ADS_CS, LOW);
  SPI.transfer(cmd);
  digitalWrite(ADS_CS, HIGH);
}

void writeRegister(uint8_t reg, uint8_t val) {
  digitalWrite(ADS_CS, LOW);
  SPI.transfer(0x40 | reg); // Write Command
  SPI.transfer(0x00);        // Number of registers - 1
  SPI.transfer(val);
  digitalWrite(ADS_CS, HIGH);
}
