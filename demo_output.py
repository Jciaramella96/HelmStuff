#!/usr/bin/env python3
"""
Configuration Diff Tool Demo Output

This script shows what the configuration diff tool would output
when analyzing the sample servers directory.
"""

from pathlib import Path

def main():
    print("Configuration Diff Tool - Demo Output")
    print("====================================")
    
    # Show sample directory structure
    print("\n1. SAMPLE DIRECTORY STRUCTURE:")
    print("sample_servers/")
    for server in ['server1', 'server2', 'server3']:
        server_path = Path(f'sample_servers/{server}')
        if server_path.exists():
            print(f"├── {server}/")
            for file in server_path.iterdir():
                if file.is_file():
                    print(f"│   ├── {file.name}")
    
    # Show parsing example
    print("\n2. CONFIGURATION PARSING EXAMPLE:")
    
    sample_files = [
        'sample_servers/server1/config.rc',
        'sample_servers/server2/config.rc', 
        'sample_servers/server3/config.rc'
    ]
    
    configs = {}
    for file_path in sample_files:
        if Path(file_path).exists():
            server_name = Path(file_path).parent.name
            configs[server_name] = {}
            print(f"\n--- {file_path} ---")
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        configs[server_name][key] = value
                        print(f"  {key} = {value}")
    
    # Show differences
    print("\n3. DIFFERENCES DETECTED:")
    print("="*50)
    
    # Collect all keys
    all_keys = set()
    for server_config in configs.values():
        all_keys.update(server_config.keys())
    
    differences_found = False
    for key in sorted(all_keys):
        values = {}
        for server in sorted(configs.keys()):
            values[server] = configs[server].get(key, "** MISSING **")
        
        # Check if there are differences
        unique_values = set(v for v in values.values() if v != "** MISSING **")
        if len(unique_values) > 1 or "** MISSING **" in values.values():
            differences_found = True
            print(f"\nKey: {key}")
            for server, value in values.items():
                status = ""
                if value == "** MISSING **":
                    status = " [MISSING]"
                print(f"  {server}: {value}{status}")
    
    if not differences_found:
        print("No differences found!")
    
    # Show what Excel report would contain
    print("\n4. EXCEL REPORT STRUCTURE:")
    print("="*50)
    print("The generated Excel file would contain:")
    print("├── Summary Sheet")
    print("│   ├── Total hosts analyzed: 3")
    print("│   ├── Total config files: 4")
    print("│   └── Files with differences: 3")
    print("├── config.rc Sheet")
    print("│   └── Matrix showing all key differences")
    print("├── sites.xml Sheet")
    print("│   └── Matrix showing all key differences")
    print("├── app.jrc Sheet")
    print("│   └── Matrix showing missing file on server3")
    print("└── Host Overview Sheet")
    print("    └── Summary of files per host")
    
    print("\n5. SAMPLE COMMAND TO RUN:")
    print("python3 config_diff_tool.py sample_servers --output report.xlsx")

if __name__ == "__main__":
    main()