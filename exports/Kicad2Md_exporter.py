import sys
import re

def parse_sexp(text):
    """Simple S-expression parser to handle KiCad netlists."""
    tokens = re.findall(r'\(|\)|"[^"]*"|[^\s()]+', text)
    
    def parse(tokens):
        res = []
        while tokens:
            token = tokens.pop(0)
            if token == '(':
                res.append(parse(tokens))
            elif token == ')':
                return res
            else:
                if token.startswith('"') and token.endswith('"'):
                    token = token[1:-1]
                res.append(token)
        return res
    
    parsed = parse(tokens)
    return parsed[0] if parsed else None

def find_sub(expr, key):
    """Helper to find a sub-expression starting with key."""
    if not isinstance(expr, list):
        return None
    for item in expr:
        if isinstance(item, list) and item[0] == key:
            return item
    return None

def find_all_subs(expr, key):
    """Helper to find all sub-expressions starting with key."""
    if not isinstance(expr, list):
        return []
    return [item for item in expr if isinstance(item, list) and item[0] == key]

def main():
    if len(sys.argv) < 3:
        print("Usage: python Kicad2Md_exporter.py <input_netlist> <output_markdown>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        with open(input_path, 'r') as f:
            input_content = f.read()

        root = parse_sexp(input_content)
        if not root:
            print("Failed to parse netlist.")
            return

        # 1. Map components for quick lookup
        components = {}
        comp_section = find_sub(root, "components")
        if comp_section:
            for item in find_all_subs(comp_section, "comp"):
                ref = find_sub(item, "ref")
                val = find_sub(item, "value")
                if ref and val:
                    components[ref[1]] = val[1]

        # 2. Process Nets
        power_nets = []
        signal_nets = []
        local_nets = []
        unconnected_nets = []

        # Keywords for power nets
        power_keywords = {'gnd', 'vcc', 'vdd', 'vss', 'batt', 'usb', '3.3v', '5v', '12v', '+', '-'}

        nets_section = find_sub(root, "nets")
        if nets_section:
            for item in find_all_subs(nets_section, "net"):
                name_sub = find_sub(item, "name")
                net_name = name_sub[1] if name_sub else "Unnamed"
                
                nodes = []
                significant_pin = None
                
                for node_sub in find_all_subs(item, "node"):
                    ref = find_sub(node_sub, "ref")[1]
                    pin = find_sub(node_sub, "pin")[1]
                    pin_func_sub = find_sub(node_sub, "pinfunction")
                    pin_func = pin_func_sub[1] if pin_func_sub else None
                    
                    comp_val = components.get(ref, "?")
                    node_str = f"{ref}[{comp_val}]-{pin}"
                    if pin_func:
                        node_str += f"({pin_func})"
                        # Heuristic for significant pin: ICs (U) or specialized components
                        if not significant_pin and (ref.startswith('U') or ref.startswith('Q') or ref.startswith('J')):
                            significant_pin = f"{ref}-{pin_func}"
                    elif not significant_pin and (ref.startswith('U') or ref.startswith('Q')):
                         significant_pin = f"{ref}-{pin}"

                    nodes.append(node_str)
                
                if not nodes:
                    continue

                display_name = net_name
                if net_name.startswith("Net-(") and significant_pin:
                    display_name = f"{net_name} (via {significant_pin})"

                net_data = {
                    'name': net_name,
                    'display_name': display_name,
                    'nodes': nodes
                }

                if net_name.startswith("unconnected-"):
                    unconnected_nets.append(net_data)
                elif net_name.startswith("Net-("):
                    local_nets.append(net_data)
                elif any(pk in net_name.lower() for pk in power_keywords):
                    power_nets.append(net_data)
                else:
                    signal_nets.append(net_data)

        # 3. Generate Markdown
        output = []
        output.append("# Topology Analysis\n")
        
        def format_nets(title, nets, group_by_prefix=False):
            if not nets:
                return
            output.append(f"## {title}")
            
            if group_by_prefix:
                # Group by prefix (first word before underscore)
                groups = {}
                for n in nets:
                    prefix = n['name'].split('_')[0] if '_' in n['name'] else "Other"
                    if prefix not in groups:
                        groups[prefix] = []
                    groups[prefix].append(n)
                
                for prefix in sorted(groups.keys()):
                    if prefix != "Other":
                        output.append(f"### {prefix}")
                        for n in sorted(groups[prefix], key=lambda x: x['name']):
                            output.append(f"- **{n['display_name']}**: {', '.join(n['nodes'])}")
                    
                if "Other" in groups:
                    output.append(f"### Other Signals")
                    for n in sorted(groups["Other"], key=lambda x: x['name']):
                        output.append(f"- **{n['display_name']}**: {', '.join(n['nodes'])}")
            else:
                for n in sorted(nets, key=lambda x: x['name']):
                    output.append(f"- **{n['display_name']}**: {', '.join(n['nodes'])}")
            output.append("")

        format_nets("Power Nets", power_nets)
        format_nets("Signal Nets", signal_nets, group_by_prefix=True)
        format_nets("Local (Auto-named) Nets", local_nets)
        
        if unconnected_nets:
            output.append("<details>")
            output.append("<summary>Unconnected Pins</summary>\n")
            for n in sorted(unconnected_nets, key=lambda x: x['name']):
                 output.append(f"- **{n['display_name']}**: {', '.join(n['nodes'])}")
            output.append("\n</details>")

        md_content = "\n".join(output)
        with open(output_path, 'w') as f:
            f.write(md_content)

        print(f"Exported to {output_path}")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error: {e}")

if __name__ == "__main__":
    main()