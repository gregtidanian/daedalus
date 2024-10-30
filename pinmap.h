// Auto-generated GPIO mappings based on netlist

#define HAS_I2C
#define HAS_UART
#define HAS_USB

#define GPIO0 0
#define GPIO1 1
#define GPIO2 2
#define GPIO3 3
#define GPIO4 4
#define GPIO5 5
#define GPIO6 6
#define GPIO7 7
#define GPIO8 8
#define GPIO9 9
#define GPIO10 10
#define GPIO11 11
#define GPIO12 12
#define GPIO13 13
#define GPIO14 14
#define GPIO15 15
#define GPIO16 16
#define GPIO21 21
#define GPIO26 26
#define GPIO33 33
#define GPIO34 34
#define GPIO35 35
#define GPIO36 36
#define GPIO37 37
#define GPIO38 38
#define GPIO39 39
#define GPIO40 40
#define GPIO41 41
#define GPIO42 42
#define GPIO45 45
#define GPIO46 46
#define GPIO47 47
#define GPIO48 48
#define I2C_SCL 17
#define I2C_SDA 18
#define USB_N 19
#define USB_P 20

// Pin Mode Configuration
void setupPins() {
    pinMode(0, INPUT_PULLUP);
    pinMode(1, INPUT_PULLUP);
    pinMode(2, INPUT_PULLUP);
    pinMode(3, INPUT_PULLUP);
    pinMode(4, INPUT_PULLUP);
    pinMode(5, INPUT_PULLUP);
    pinMode(6, INPUT_PULLUP);
    pinMode(7, INPUT_PULLUP);
    pinMode(8, INPUT_PULLUP);
    pinMode(9, INPUT_PULLUP);
    pinMode(10, INPUT_PULLUP);
    pinMode(11, INPUT_PULLUP);
    pinMode(12, INPUT_PULLUP);
    pinMode(13, INPUT_PULLUP);
    pinMode(14, INPUT_PULLUP);
    pinMode(15, INPUT_PULLUP);
    pinMode(16, INPUT_PULLUP);
    pinMode(21, INPUT_PULLUP);
    pinMode(26, INPUT_PULLUP);
    pinMode(33, INPUT_PULLUP);
    pinMode(34, INPUT_PULLUP);
    pinMode(35, INPUT_PULLUP);
    pinMode(36, INPUT_PULLUP);
    pinMode(37, INPUT_PULLUP);
    pinMode(38, INPUT_PULLUP);
    pinMode(39, INPUT_PULLUP);
    pinMode(40, INPUT_PULLUP);
    pinMode(41, INPUT_PULLUP);
    pinMode(42, INPUT_PULLUP);
    pinMode(45, INPUT_PULLUP);
    pinMode(46, INPUT_PULLUP);
    pinMode(47, INPUT_PULLUP);
    pinMode(48, INPUT_PULLUP);
    pinMode(17, INPUT_PULLUP);
    pinMode(18, INPUT_PULLUP);
    pinMode(19, INPUT_PULLUP);
    pinMode(20, INPUT_PULLUP);
}

// Peripheral Initializations
#ifdef HAS_I2C
void init_I2C() {
    Wire.begin(I2C_SDA, I2C_SCL);
}
#endif

#ifdef HAS_UART
void init_UART() {
    Serial.begin(9600, SERIAL_8N1, RXD, TXD);
}
#endif

