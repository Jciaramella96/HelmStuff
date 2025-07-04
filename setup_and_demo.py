#!/usr/bin/env python3
"""
Setup and Demo Script for Configuration Diff Tool

This script demonstrates the functionality of the configuration diff tool
and provides setup instructions.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import pandas
        import openpyxl
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install required dependencies."""
    print("Installing required dependencies...")
    try:
        # Try with pip
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas', 'openpyxl'])
        return True
    except subprocess.CalledProcessError:
        print("Failed to install with pip. Trying alternative methods...")
        try:
            # Try with apt (Ubuntu/Debian)
            subprocess.check_call(['sudo', 'apt', 'install', '-y', 'python3-pandas', 'python3-openpyxl'])
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Could not install dependencies automatically.")
            return False

def demonstrate_parsing():
    """Demonstrate how the tool parses configuration files."""
    print("\n" + "="*60)
    print("CONFIGURATION DIFF TOOL DEMONSTRATION")
    print("="*60)
    
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
    
    # Demonstrate file parsing
    print("\n2. SAMPLE CONFIGURATION PARSING:")
    
    sample_files = [
        'sample_servers/server1/config.rc',
        'sample_servers/server2/config.rc', 
        'sample_servers/server3/config.rc'
    ]
    
    for file_path in sample_files:
        if Path(file_path).exists():
            print(f"\n--- {file_path} ---")
            with open(file_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        key, value = line.split('=', 1)
                        print(f"  {key.strip()} = {value.strip()}")
    
    # Show differences that would be detected
    print("\n3. DIFFERENCES THAT WOULD BE DETECTED:")
    print("Key: db_host")
    print("  server1: 192.168.1.10")
    print("  server2: 192.168.1.11")
    print("  server3: 192.168.1.12")
    print()
    print("Key: app_version")
    print("  server1: 1.2.0")
    print("  server2: 1.2.1")
    print("  server3: 1.2.0")
    print()
    print("Key: cache_size")
    print("  server1: 256MB")
    print("  server2: 512MB")
    print("  server3: ** MISSING **")
    print()
    print("Key: backup_enabled")
    print("  server1: ** MISSING **")
    print("  server2: ** MISSING **")
    print("  server3: true")

def show_setup_instructions():
    """Show setup instructions for the tool."""
    print("\n" + "="*60)
    print("SETUP INSTRUCTIONS")
    print("="*60)
    
    print("\n1. SYSTEM REQUIREMENTS:")
    print("   - Python 3.7 or higher")
    print("   - pandas library")
    print("   - openpyxl library")
    
    print("\n2. INSTALLATION OPTIONS:")
    print("\n   Option A: Using pip")
    print("   pip install pandas openpyxl")
    
    print("\n   Option B: Using pip with virtual environment")
    print("   python3 -m venv config_diff_env")
    print("   source config_diff_env/bin/activate")
    print("   pip install pandas openpyxl")
    
    print("\n   Option C: Using system packages (Ubuntu/Debian)")
    print("   sudo apt install python3-pandas python3-openpyxl")
    
    print("\n   Option D: Using conda")
    print("   conda install pandas openpyxl")
    
    print("\n3. USAGE:")
    print("   python3 config_diff_tool.py /path/to/your/servers")
    print("   python3 config_diff_tool.py sample_servers --output demo_report.xlsx")

def main():
    """Main demo function."""
    print("Configuration Diff Tool - Setup and Demo")
    print("========================================")
    
    # Check if dependencies are available
    if check_dependencies():
        print("✓ All dependencies are installed!")
        
        # Run the actual tool on sample data
        print("\n4. RUNNING THE ACTUAL TOOL:")
        try:
            import subprocess
            result = subprocess.run([
                sys.executable, 'config_diff_tool.py', 'sample_servers', 
                '--output', 'demo_report.xlsx'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✓ Tool executed successfully!")
                print("✓ Report generated: demo_report.xlsx")
                print("\nOutput:")
                print(result.stdout)
            else:
                print("✗ Tool execution failed:")
                print(result.stderr)
                
        except Exception as e:
            print(f"✗ Error running tool: {e}")
    else:
        print("✗ Dependencies not installed.")
        print("\nWould you like to try installing them? (This may require admin privileges)")
        
        # Show what the tool would do
        demonstrate_parsing()
        show_setup_instructions()
        
        # Offer to install
        choice = input("\nTry to install dependencies automatically? (y/n): ").lower()
        if choice == 'y':
            if install_dependencies():
                print("✓ Dependencies installed successfully!")
                print("You can now run: python3 config_diff_tool.py sample_servers")
            else:
                print("✗ Automatic installation failed.")
                print("Please install manually using one of the methods above.")
    
    # Always show the demonstration
    demonstrate_parsing()

if __name__ == "__main__":
    main()