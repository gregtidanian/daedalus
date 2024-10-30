import re

# Function to parse the netlist file for GPIO mappings and peripheral details
def parse_netlist_file(netlist_file_path):
    net_mappings = {}
    peripherals = set()
    components = set()
    pin_types = {}

    with open(netlist_file_path, 'r') as file:
        lines = file.readlines()

        current_net = None
        for line in lines:
            # Check for net name
            net_name_match = re.search(r'\(name\s+"(/[\w_]+)"\)', line)
            if net_name_match:
                current_net = net_name_match.group(1).strip('/')
                # Detect peripherals based on net nameså
                if "I2C" in current_net:
                    peripherals.add("I2C")
                elif "SPI" in current_net:
                    peripherals.add("SPI")
                elif "RXD" in current_net or "TXD" in current_net:
                    peripherals.add("UART")
                elif "USB" in current_net:
                    peripherals.add("USB")

            # Detect components from node references
            component_match = re.search(r'\(ref\s+"(\w+)"\)', line)
            if component_match:
                components.add(component_match.group(1))

            # Capture pin functions and types within each net
            if current_net:
                gpio_match = re.search(r'\(pinfunction\s+"IO(\d+)"\)', line)
                pintype_match = re.search(r'\(pintype\s+"(\w+)"\)', line)

                if gpio_match:
                    gpio_pin = gpio_match.group(1)
                    net_mappings[current_net] = gpio_pin
                    current_net = None  # Reset for the next net

                if pintype_match and gpio_match:
                    pin_types[gpio_pin] = pintype_match.group(1)

    return net_mappings, peripherals, components, pin_types

# Generate the GPIO mapping header file
def generate_gpio_mapping_header(net_mappings, peripherals, pin_types, output_path):
    with open(output_path, 'w') as header_file:
        header_file.write("// Auto-generated GPIO mappings based on netlist\n\n")
        
        # Define detected peripherals for conditional compilation
        if "I2C" in peripherals:
            header_file.write("#define HAS_I2C\n")
        if "SPI" in peripherals:
            header_file.write("#define HAS_SPI\n")
        if "UART" in peripherals:
            header_file.write("#define HAS_UART\n")
        if "USB" in peripherals:
            header_file.write("#define HAS_USB\n")
        header_file.write("\n")

        # Write #define statements for each net-to-GPIO mapping
        for net_name, gpio_pin in net_mappings.items():
            header_file.write(f"#define {net_name} {gpio_pin}\n")
        
        # Pin Mode Configuration
        header_file.write("\n// Pin Mode Configuration\n")
        header_file.write("void setupPins() {\n")
        for gpio_pin, pin_type in pin_types.items():
            if pin_type == "input":
                header_file.write(f"    pinMode({gpio_pin}, INPUT);\n")
            elif pin_type == "output":
                header_file.write(f"    pinMode({gpio_pin}, OUTPUT);\n")
            elif pin_type == "bidirectional":
                header_file.write(f"    pinMode({gpio_pin}, INPUT_PULLUP);\n")  # Example for bidirectional
        header_file.write("}\n\n")

        # Peripheral Initializations
        header_file.write("// Peripheral Initializations\n")
        if "I2C" in peripherals:
            header_file.write("#ifdef HAS_I2C\n")
            header_file.write("void init_I2C() {\n")
            header_file.write("    Wire.begin(I2C_SDA, I2C_SCL);\n")
            header_file.write("}\n")
            header_file.write("#endif\n\n")

        if "UART" in peripherals:
            header_file.write("#ifdef HAS_UART\n")
            header_file.write("void init_UART() {\n")
            header_file.write("    Serial.begin(9600, SERIAL_8N1, RXD, TXD);\n")
            header_file.write("}\n")
            header_file.write("#endif\n\n")


# Main script execution
netlist_file_path = 'DesignESP32PCB.net'  # Path to the netlist file
output_header_path = 'pinmap.h'  # Output header file path

# Parse the netlist file for GPIO mappings, peripherals, components, and pin types
net_mappings, peripherals, components, pin_types = parse_netlist_file(netlist_file_path)

# Generate the GPIO mapping header file
generate_gpio_mapping_header(net_mappings, peripherals, pin_types, output_header_path)

# Print detected components and peripherals from the electronics design
print(f"Detected Components: {components}")
print(f"Detected Peripherals: {peripherals}")
print(f"GPIO mapping header file generated at: {output_header_path}")
