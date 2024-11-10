import re

# Function to parse the netlist file and extract component details
def parse_netlist_file(file_path):
    # Dictionary to store components with their reference as key
    components = {}
    component = None  # Temporarily holds the current component being parsed
    pins = []  # List to hold pin details for the current component

    # Open the netlist file and read all lines
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Loop through each line to extract component data
    for line in lines:
        # Check if a new component starts; save the previous component if any
        if "(comp " in line or "(libpart " in line:
            # Add the previous component to the dictionary if it has a reference
            if component is not None and 'ref' in component:
                component['pins'] = pins if pins else None  # Add pins if they exist
                components[component['ref']] = component
            # Reset for the new component
            component = {}
            pins = []

        # If 'component' is still None, initialise it (for the first component)
        if component is None:
            component = {}

        # Extract the reference ID (e.g., R101, C202) and store it
        ref_match = re.search(r'\(ref "(.*?)"\)', line)
        if ref_match:
            component['ref'] = ref_match.group(1).lower()

        # Extract the value of the component (e.g., resistor value, capacitor type)
        value_match = re.search(r'\(value "(.*?)"\)', line)
        if value_match:
            component['value'] = value_match.group(1)
        elif 'value' not in component:
            component['value'] = 'unknown'  # Assign "unknown" if no value found

        # Extract the footprint (physical layout) of the component
        footprint_match = re.search(r'\(footprint "(.*?)"\)', line)
        if footprint_match:
            component['footprint'] = footprint_match.group(1)
        elif 'footprint' not in component:
            component['footprint'] = 'unknown'  # Assign "unknown" if no footprint found

        # Extract pin details if available and add to pins list
        pin_match = re.search(r'\(pin \(num "(.*?)"\) \(name "(.*?)"\) \(type "(.*?)"\)', line)
        if pin_match:
            pin = {
                'num': pin_match.group(1),   # Pin number
                'name': pin_match.group(2),  # Pin name
                'type': pin_match.group(3)   # Pin type (e.g., input, output)
            }
            pins.append(pin)

    # Save the last component after the loop if it has a reference
    if component is not None and 'ref' in component:
        component['pins'] = pins if pins else None
        components[component['ref']] = component

    # Return the dictionary of all parsed components
    return components

# Function to generate the DTS file from parsed component data
def generate_dts_file(components, output_path):
    # Open the output file in write mode
    with open(output_path, 'w') as dts_file:
        # Write DTS header information
        dts_file.write("/dts-v1/;\n/\n{\n")
        dts_file.write("    compatible = \"custom,ZSWatch-v2\";\n\n")

        # Go through each component to write its data to the DTS
        for ref, component in components.items():
            # Get component value and footprint or default to 'unknown'
            value = component.get('value', 'unknown')
            footprint = component.get('footprint', 'unknown')
            pins = component.get('pins', [])

            # Write component reference, footprint, and label
            dts_file.write(f"    {ref} {{\n")
            dts_file.write(f"        compatible = \"custom,{footprint}\";\n")
            dts_file.write(f"        label = \"{ref.upper()} - {value}\";\n")

            # Write pin information if pins are available for the component
            if pins:
                dts_file.write("        pins {\n")
                for pin in pins:
                    dts_file.write(f"            pin{pin['num']} {{\n")
                    dts_file.write(f"                pin-name = \"{pin['name']}\";\n")
                    dts_file.write(f"                pin-type = \"{pin['type']}\";\n")
                    dts_file.write("            };\n")
                dts_file.write("        };\n")

            dts_file.write("    };\n\n")

        # Close the DTS file structure
        dts_file.write("};\n")

# Main script
netlist_file_path = 'ZSWatch.net'
output_dts_path = 'ZSWatch.dts'

try:
    # Parse the netlist file and generate the DTS file
    components = parse_netlist_file(netlist_file_path)
    generate_dts_file(components, output_dts_path)
    print(f"Device Tree file generated at: {output_dts_path}")
except FileNotFoundError:
    print(f"File not found: {netlist_file_path}")
except IOError as e:
    print(f"IO error: {e}")
