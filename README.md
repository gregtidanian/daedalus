*The following comes entirely from conversations and ideas from [Walter Jacob](https://github.com/jacobw56), founder of [Overkill Projects](https://overkillprojects.com/)*.

Firmware development typically involves referring to information from electronics design files, as well as component datasheets.

Having direct access to information within the toolchain you are writing firmware on, and being able to generate some code directly from electronics design files can reduce the risk of mistakes.

The following outlines a command line tool that parses files that an electronics engineer has worked on or generated.

# Device Tree Source File Generation

A devicetree is a datastructure that describes hardware to driver models and provides initial hardware configurations for firmware development.

# Hardware

The device tree source file generation will be based on the open source zephyr project [ZSWatch](https://github.com/jakkra/ZSWatch), including the [hardware design files](https://github.com/jakkra/ZSWatch-HW/tree/f00c755fa8d6e1f00ff1e177645d56457bea2659) by [Jakob Krantz](https://github.com/jakkra).

# Pin Map Header File Generation
The command line tool had the initial goal of:

1. Generating a template header file with hardware-specific information
2. Printing component and peripheral information to the terminal

## Approaches

The approaches were to work directly from electronics design files and to work from a generated netlist file.

### Design Files

Electronics KiCAD design files for a development kit based on the ESP32-S3 microcontroller [1] were initially used as files to test a parsing script on.

![Screenshot 2024-10-30 at 16 21 39](https://github.com/user-attachments/assets/b8d761ac-4d25-40af-9625-605bff231e76)

The benefits of linking a tool to schematic (.kicad_sch) and layout (.kicad_pcb) files directly include:

- If there are changes made to design files a firmware development tool can be used to directly verify what breaking changes to firmware are made if any
- The firmware developer would only need to link their firmware to design files, without the need to carry out further file generation for relevant information

The electronics design files included information on if I2C or SPI were being used, however information around pin-mapping could not be obtained. This meant that information around what bus peripherals and components were included in the design were able to be printed to the terminal, however generating a template header file with pin mapping information was not possible.
Therefore 

One considered solution was to create a JSON library of pin-out information for key microcontrollers including the ESP32 series which was used in the example electronics file. The solution is not robust however, as the parsed information did not include the pin-out information and therefore would only be able to include default pin information (e.g. for I2C or SPI peripherals).

## Netlist

A more robust solution was to use a netlist file generated from KiCAD.

![Screenshot 2024-10-30 at 17 02 22](https://github.com/user-attachments/assets/64a46fe3-f182-4635-83ca-69e88cd34280)


![Screenshot 2024-10-30 at 17 02 52](https://github.com/user-attachments/assets/38d1d41c-2fcd-42fe-bbf8-1b187af3a42b)


The benefits of using a netlist file include:

- Information regarding pinouts and connections are available
- Most electronics design software allow users to generate a netlist file, meaning the tool's compatibility is not limited to KiCAD

The drawbacks of using a netlist file include:

- Generating a netlist file is an added step for a user to use the command line tool
- If an electronics designer makes a change to the electronics design and forgets to regenerate the netlist file, the tool will not be working on the correct version

The generated netlist file is _DesignESP32PCB.net_.

The parsing script written is _pinmapgenerator.py_ and the generated header file is pinmap.h. The contents of the generated header file include:

- Pin definitions
```
#define I2C_SCL 17
#define I2C_SDA 18
#define USB_N 19
#define USB_P 20
```

- Pin mode configurations

`pinMode(0, INPUT_PULLUP);`

- Peripheral Initialisations
```
// Peripheral Initialisations
#ifdef HAS_I2C
void init_I2C() {
    Wire.begin(I2C_SDA, I2C_SCL);
}
#endif
```

The terminal also outputted the following information about the design:
```
Detected Components: {'J3', 'RESET1', 'C2', 'R4', 'R1', 'C5', 'C4', 'R6', 'R5', 'U4', 'R7', 'R3', 'C6', 'D1', 'C1', 'C7', 'R8', 'J1', 'JUSB1', 'BOOT1', 'R2', 'D2', 'C3', 'U1', 'U3', 'U2'}
Detected Peripherals: {'I2C', 'USB', 'UART'}
GPIO mapping header file generated at: pinmap.h
```
## Future Considerations

It is worth ensuring that netlist files from other electronics design software have enough similarity in their formatting that the tool is compatible with them. If not it could be worth making formatting changes depending on which software is being used. The software being used is mentioned in the netlist file.

For future, if there is a feature on the command line tool which can connect to netlist files as well as design files more functionality may be possible, including a feature to setup a firmware toolchain semi-autonomously for input into the design.

A feature where on the firmware toolchain a reference of pinouts can be easily accessible.

A feature where you can graphically view components in the electronics design.

A feature for developing firmware test procedures.

Potentially expanding into a firmware-specific IDE

Considering a version control system based on tracking firmware changes but linking them to electronics designs too.


# References

[1] John from Predictable Designs
[2] https://docs.zephyrproject.org/latest/build/dts/index.html
