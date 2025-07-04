#!/usr/bin/env python3
"""
Configuration Diff Tool

A tool to compare configuration files across multiple server directories
and report differences in an Excel format.

Usage:
    python config_diff_tool.py <directory_path> [--output output.xlsx] [--verbose]
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Any
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font
from openpyxl.utils.dataframe import dataframe_to_rows


class ConfigDiffTool:
    """Main class for comparing configuration files across server directories."""
    
    def __init__(self, base_directory: str, output_file: str = "config_diff_report.xlsx"):
        self.base_directory = Path(base_directory)
        self.output_file = output_file
        self.config_extensions = {'.rc', '.xml', '.jrc'}
        self.host_configs = defaultdict(dict)  # {host: {filename: {key: value}}}
        self.all_files = set()
        self.all_keys_per_file = defaultdict(set)
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def is_valid_config_file(self, file_path: Path) -> bool:
        """Check if a file is a valid configuration file based on extension."""
        return file_path.suffix.lower() in self.config_extensions
    
    def parse_config_file(self, file_path: Path) -> Dict[str, str]:
        """
        Parse a configuration file into key-value pairs.
        
        Args:
            file_path: Path to the configuration file
            
        Returns:
            Dictionary of key-value pairs
        """
        config_data = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line_num, line in enumerate(file, 1):
                    # Strip whitespace
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Split by '=' and ensure we have both key and value
                    if '=' in line:
                        key, value = line.split('=', 1)  # Split only on first '='
                        key = key.strip()
                        value = value.strip()
                        
                        if key:  # Only add if key is not empty
                            config_data[key] = value
                            
        except Exception as e:
            self.logger.warning(f"Error parsing {file_path}: {e}")
            
        return config_data
    
    def scan_directories(self) -> None:
        """Scan the base directory for host subdirectories and their config files."""
        if not self.base_directory.exists():
            raise FileNotFoundError(f"Directory {self.base_directory} does not exist")
        
        self.logger.info(f"Scanning directory: {self.base_directory}")
        
        # Find all subdirectories (host directories)
        host_directories = [d for d in self.base_directory.iterdir() 
                          if d.is_dir() and not d.name.startswith('.')]
        
        if not host_directories:
            raise ValueError("No host directories found in the specified path")
        
        self.logger.info(f"Found {len(host_directories)} host directories")
        
        # Process each host directory
        for host_dir in host_directories:
            host_name = host_dir.name
            self.logger.info(f"Processing host: {host_name}")
            
            # Find all config files in this host directory
            config_files = [f for f in host_dir.iterdir() 
                          if f.is_file() and self.is_valid_config_file(f)]
            
            for config_file in config_files:
                file_name = config_file.name
                self.all_files.add(file_name)
                
                # Parse the configuration file
                config_data = self.parse_config_file(config_file)
                self.host_configs[host_name][file_name] = config_data
                
                # Track all keys for this file across all hosts
                self.all_keys_per_file[file_name].update(config_data.keys())
                
                self.logger.debug(f"Parsed {file_name} for {host_name}: {len(config_data)} keys")
    
    def find_differences(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Find differences in configuration values across hosts.
        
        Returns:
            Dictionary with file names as keys and list of differences as values
        """
        differences = {}
        
        for file_name in sorted(self.all_files):
            file_differences = []
            all_keys = self.all_keys_per_file[file_name]
            
            for key in sorted(all_keys):
                # Collect values for this key across all hosts
                key_values = {}
                hosts_with_key = []
                
                for host_name in sorted(self.host_configs.keys()):
                    if file_name in self.host_configs[host_name]:
                        if key in self.host_configs[host_name][file_name]:
                            value = self.host_configs[host_name][file_name][key]
                            key_values[host_name] = value
                            hosts_with_key.append(host_name)
                        else:
                            key_values[host_name] = "** MISSING **"
                    else:
                        key_values[host_name] = "** FILE NOT FOUND **"
                
                # Check if there are differences in values
                unique_values = set(v for v in key_values.values() 
                                  if v not in ["** MISSING **", "** FILE NOT FOUND **"])
                
                if len(unique_values) > 1 or len(key_values) != len(hosts_with_key):
                    # There are differences
                    diff_entry = {
                        'key': key,
                        'hosts': key_values,
                        'unique_values': list(unique_values),
                        'has_missing': "** MISSING **" in key_values.values(),
                        'has_missing_file': "** FILE NOT FOUND **" in key_values.values()
                    }
                    file_differences.append(diff_entry)
            
            if file_differences:
                differences[file_name] = file_differences
                
        return differences
    
    def create_excel_report(self, differences: Dict[str, List[Dict[str, Any]]]) -> None:
        """Create an Excel report with the differences found."""
        wb = Workbook()
        
        # Remove default worksheet
        wb.remove(wb.active)
        
        # Create summary worksheet
        summary_ws = wb.create_sheet("Summary")
        self._create_summary_sheet(summary_ws, differences)
        
        # Create worksheet for each file with differences
        for file_name, file_diffs in differences.items():
            # Clean filename for worksheet name (Excel has limitations)
            sheet_name = file_name[:27] + "..." if len(file_name) > 30 else file_name
            sheet_name = sheet_name.replace('/', '_').replace('\\', '_')
            
            ws = wb.create_sheet(sheet_name)
            self._create_file_diff_sheet(ws, file_name, file_diffs)
        
        # Create host overview worksheet
        overview_ws = wb.create_sheet("Host Overview")
        self._create_host_overview_sheet(overview_ws)
        
        # Save the workbook
        wb.save(self.output_file)
        self.logger.info(f"Excel report saved to: {self.output_file}")
    
    def _create_summary_sheet(self, ws, differences: Dict[str, List[Dict[str, Any]]]) -> None:
        """Create the summary worksheet."""
        ws.title = "Summary"
        
        # Header
        ws['A1'] = "Configuration Diff Tool - Summary Report"
        ws['A1'].font = Font(bold=True, size=14)
        
        # Statistics
        row = 3
        ws[f'A{row}'] = "Statistics:"
        ws[f'A{row}'].font = Font(bold=True)
        row += 1
        
        ws[f'A{row}'] = f"Total hosts analyzed: {len(self.host_configs)}"
        row += 1
        ws[f'A{row}'] = f"Total config files: {len(self.all_files)}"
        row += 1
        ws[f'A{row}'] = f"Files with differences: {len(differences)}"
        row += 2
        
        # Files with differences
        ws[f'A{row}'] = "Files with differences:"
        ws[f'A{row}'].font = Font(bold=True)
        row += 1
        
        ws[f'A{row}'] = "File Name"
        ws[f'B{row}'] = "Keys with Differences"
        ws[f'A{row}'].font = Font(bold=True)
        ws[f'B{row}'].font = Font(bold=True)
        row += 1
        
        for file_name, file_diffs in differences.items():
            ws[f'A{row}'] = file_name
            ws[f'B{row}'] = len(file_diffs)
            row += 1
    
    def _create_file_diff_sheet(self, ws, file_name: str, file_diffs: List[Dict[str, Any]]) -> None:
        """Create a worksheet for a specific file's differences."""
        # Header
        ws['A1'] = f"Differences in: {file_name}"
        ws['A1'].font = Font(bold=True, size=12)
        
        # Column headers
        row = 3
        ws[f'A{row}'] = "Key"
        ws[f'A{row}'].font = Font(bold=True)
        
        col = 2
        host_names = sorted(self.host_configs.keys())
        for host_name in host_names:
            ws.cell(row=row, column=col, value=host_name)
            ws.cell(row=row, column=col).font = Font(bold=True)
            col += 1
        
        # Data rows
        row += 1
        for diff in file_diffs:
            ws[f'A{row}'] = diff['key']
            
            col = 2
            for host_name in host_names:
                value = diff['hosts'].get(host_name, "** NOT FOUND **")
                cell = ws.cell(row=row, column=col, value=value)
                
                # Color coding
                if value == "** MISSING **":
                    cell.fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")  # Yellow
                elif value == "** FILE NOT FOUND **":
                    cell.fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")  # Red
                elif len(diff['unique_values']) > 1:
                    cell.fill = PatternFill(start_color="FFA500", end_color="FFA500", fill_type="solid")  # Orange
                
                col += 1
            row += 1
    
    def _create_host_overview_sheet(self, ws) -> None:
        """Create a host overview worksheet."""
        ws.title = "Host Overview"
        
        # Header
        ws['A1'] = "Host Overview"
        ws['A1'].font = Font(bold=True, size=12)
        
        # Column headers
        row = 3
        ws[f'A{row}'] = "Host Name"
        ws[f'B{row}'] = "Config Files Found"
        ws[f'C{row}'] = "Total Keys"
        ws[f'A{row}'].font = Font(bold=True)
        ws[f'B{row}'].font = Font(bold=True)
        ws[f'C{row}'].font = Font(bold=True)
        
        row += 1
        for host_name in sorted(self.host_configs.keys()):
            ws[f'A{row}'] = host_name
            ws[f'B{row}'] = len(self.host_configs[host_name])
            
            # Count total keys across all files for this host
            total_keys = sum(len(file_config) for file_config in self.host_configs[host_name].values())
            ws[f'C{row}'] = total_keys
            row += 1
    
    def run(self) -> None:
        """Main execution method."""
        try:
            self.logger.info("Starting configuration diff analysis...")
            
            # Scan directories and parse files
            self.scan_directories()
            
            # Find differences
            self.logger.info("Analyzing differences...")
            differences = self.find_differences()
            
            if not differences:
                self.logger.info("No differences found across all configuration files!")
                # Still create a report showing this
                wb = Workbook()
                ws = wb.active
                ws.title = "No Differences Found"
                ws['A1'] = "No configuration differences found across all hosts!"
                ws['A1'].font = Font(bold=True, size=14)
                wb.save(self.output_file)
            else:
                # Create Excel report
                self.logger.info(f"Found differences in {len(differences)} files")
                self.create_excel_report(differences)
            
            self.logger.info("Analysis complete!")
            
        except Exception as e:
            self.logger.error(f"Error during analysis: {e}")
            raise


def main():
    """Main function to run the configuration diff tool."""
    parser = argparse.ArgumentParser(
        description="Compare configuration files across server directories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python config_diff_tool.py /path/to/servers
  python config_diff_tool.py /path/to/servers --output my_report.xlsx
  python config_diff_tool.py /path/to/servers --verbose
        """
    )
    
    parser.add_argument(
        'directory',
        help='Path to directory containing server subdirectories'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='config_diff_report.xlsx',
        help='Output Excel file name (default: config_diff_report.xlsx)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate input directory
    if not os.path.exists(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist")
        sys.exit(1)
    
    # Run the tool
    try:
        tool = ConfigDiffTool(args.directory, args.output)
        tool.run()
        print(f"\nReport generated successfully: {args.output}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()