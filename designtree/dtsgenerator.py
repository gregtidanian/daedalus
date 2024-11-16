import os
import re
import yaml  # For generating YAML bindings

# Function to parse the netlist file and obtain component details
def parse_netlist_file(file_path):
    components = {}
    component = None
    pins = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if "(comp " in line or "(libpart " in line:
            if component is not None and 'ref' in component:
                component['pins'] = pins if pins else None
                components[component['ref']] = component
            component = {}
            pins = []

        if component is None:
            component = {}

        ref_match = re.search(r'\(ref "(.*?)"\)', line)
        if ref_match:
            component['ref'] = ref_match.group(1).lower()

        value_match = re.search(r'\(value "(.*?)"\)', line)
        if value_match:
            component['value'] = value_match.group(1)
        elif 'value' not in component:
            component['value'] = 'unknown'

        footprint_match = re.search(r'\(footprint "(.*?)"\)', line)
        if footprint_match:
            component['footprint'] = footprint_match.group(1)
        elif 'footprint' not in component:
            component['footprint'] = 'unknown'

        pin_match = re.search(r'\(pin \(num "(.*?)"\) \(name "(.*?)"\) \(type "(.*?)"\)', line)
        if pin_match:
            pin = {
                'num': pin_match.group(1),
                'name': pin_match.group(2),
                'type': pin_match.group(3)
            }
            pins.append(pin)

    if component is not None and 'ref' in component:
        component['pins'] = pins if pins else None
        components[component['ref']] = component

    return components

# Function to generate DTS files and folder structure
def generate_files(components, output_dir, netlist_file_name):
    # Create necessary folders
    os.makedirs(f"{output_dir}/bindings", exist_ok=True)
    os.makedirs(f"{output_dir}/common", exist_ok=True)
    os.makedirs(f"{output_dir}/boards", exist_ok=True)

    # Generate common.dtsi
    with open(f"{output_dir}/common/common.dtsi", 'w') as common_file:
        common_file.write("/dts-v1/;\n\n")
        for ref, component in components.items():
            value = component.get('value', 'unknown')
            footprint = component.get('footprint', 'unknown')
            common_file.write(f"/ {{\n    {ref} {{\n")
            common_file.write(f"        compatible = \"custom,{footprint}\";\n")
            common_file.write(f"        label = \"{ref.upper()} - {value}\";\n")
            common_file.write("    };\n};\n\n")

    # Generate YAML bindings
    for component in components.values():
        compatible = component.get('footprint', 'unknown')
        yaml_binding = {
            "compatible": f"custom,{compatible}",
            "description": f"Binding for {compatible}",
            "properties": {
                "label": {"type": "string", "description": "Human-readable label"},
            },
        }
        with open(f"{output_dir}/bindings/{compatible.replace(':', '_')}.yaml", 'w') as yaml_file:
            yaml.dump(yaml_binding, yaml_file, default_flow_style=False)

    # Derive the board file name from the netlist file name
    board_file_name = os.path.splitext(netlist_file_name)[0] + '.dts'

    # Generate board-specific DTS
    with open(f"{output_dir}/boards/{board_file_name}", 'w') as board_file:
        board_file.write("/dts-v1/;\n/\n{\n")
        board_file.write("    #include \"../common/common.dtsi\"\n")
        board_file.write("};\n")

    return board_file_name

# Main script
netlist_file_path = 'ZSWatch.net'  # Netlist file
output_dir = 'dts'  # Output directory to "dts"
try:
    # Parse the netlist file and generate the DTS structure
    components = parse_netlist_file(netlist_file_path)
    board_file_name = generate_files(components, output_dir, os.path.basename(netlist_file_path))
    print(f"Device Tree files generated in: {output_dir}")
    print(f"Board-specific DTS file: {output_dir}/boards/{board_file_name}")
except FileNotFoundError:
    print(f"File not found: {netlist_file_path}")
except IOError as e:
    print(f"IO error: {e}")
