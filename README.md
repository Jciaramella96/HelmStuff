# Configuration Diff Tool

A Python tool that compares configuration files across multiple server directories and reports differences in an Excel format.

## Overview

This tool scans a directory containing subdirectories (each named after a server hostname) and compares configuration files (`.rc`, `.xml`, `.jrc`) across all servers. It identifies differences in key-value pairs and generates a comprehensive Excel report.

## Features

- **Multi-server analysis**: Compare configurations across unlimited number of servers
- **Key-value parsing**: Automatically extracts key-value pairs from configuration files
- **Smart filtering**: Ignores comment lines (starting with `#`) and empty lines
- **Excel reporting**: Generates detailed Excel reports with multiple worksheets
- **Color-coded results**: Visual indicators for missing files, missing keys, and differing values
- **Comprehensive logging**: Detailed logging with optional verbose mode
- **Error handling**: Robust error handling for malformed files and missing directories

## Directory Structure Expected

```
servers/
├── server1/
│   ├── config.rc
│   ├── sites.xml
│   └── application.jrc
├── server2/
│   ├── config.rc
│   ├── sites.xml
│   └── application.jrc
└── server3/
    ├── config.rc
    ├── sites.xml
    └── application.jrc
```

## Installation

1. **Clone or download the tool:**
   ```bash
   # Download the files to your local directory
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
python config_diff_tool.py /path/to/servers
```

### Advanced Usage

```bash
# Specify custom output file
python config_diff_tool.py /path/to/servers --output my_report.xlsx

# Enable verbose logging
python config_diff_tool.py /path/to/servers --verbose

# Combine options
python config_diff_tool.py /path/to/servers -o detailed_report.xlsx -v
```

### Command Line Arguments

- `directory`: Path to directory containing server subdirectories (required)
- `--output`, `-o`: Output Excel file name (default: `config_diff_report.xlsx`)
- `--verbose`, `-v`: Enable verbose logging
- `--help`, `-h`: Show help message

## Configuration File Format

The tool expects configuration files with key-value pairs in the format:

```
# This is a comment and will be ignored
key1=value1
key2=value with spaces
# Another comment
key3=value3
```

**Parsing Rules:**
- Lines starting with `#` are ignored (comments)
- Empty lines are ignored
- Key-value pairs are split by the first `=` character
- Leading/trailing whitespace is automatically trimmed
- Keys must be non-empty

## Excel Report Structure

The generated Excel report contains multiple worksheets:

### 1. Summary Sheet
- Overall statistics (number of hosts, files, differences)
- List of files with differences

### 2. Individual File Sheets
- One sheet per configuration file that has differences
- Matrix view showing each key and its value across all hosts
- Color coding:
  - **Yellow**: Key missing from this host's file
  - **Red**: File not found on this host
  - **Orange**: Different values across hosts

### 3. Host Overview Sheet
- Summary of each host's configuration files
- Count of total keys per host

## Color Coding Legend

| Color | Meaning |
|-------|---------|
| 🟡 Yellow | Key is missing from this host's configuration file |
| 🔴 Red | Configuration file is missing from this host |
| 🟠 Orange | Key has different values across hosts |
| ⚪ White | Key has consistent value across all hosts |

## Example Output

After running the tool, you'll see console output like:

```
2024-01-15 10:30:00,123 - INFO - Starting configuration diff analysis...
2024-01-15 10:30:00,124 - INFO - Scanning directory: /path/to/servers
2024-01-15 10:30:00,125 - INFO - Found 3 host directories
2024-01-15 10:30:00,126 - INFO - Processing host: server1
2024-01-15 10:30:00,127 - INFO - Processing host: server2
2024-01-15 10:30:00,128 - INFO - Processing host: server3
2024-01-15 10:30:00,129 - INFO - Analyzing differences...
2024-01-15 10:30:00,130 - INFO - Found differences in 2 files
2024-01-15 10:30:00,145 - INFO - Excel report saved to: config_diff_report.xlsx
2024-01-15 10:30:00,146 - INFO - Analysis complete!

Report generated successfully: config_diff_report.xlsx
```

## Supported File Types

- `.rc` files (runtime configuration)
- `.xml` files (XML configuration)
- `.jrc` files (Java runtime configuration)

## Error Handling

The tool handles various error conditions gracefully:

- **Missing directories**: Clear error message if the specified directory doesn't exist
- **No host directories**: Warning if no subdirectories are found
- **File parsing errors**: Continues processing other files, logs warnings
- **Permission errors**: Logs warnings and continues with accessible files
- **Malformed files**: Skips problematic lines and continues parsing

## Troubleshooting

### Common Issues

1. **"No host directories found"**
   - Ensure your directory contains subdirectories named after hostnames
   - Check that subdirectories don't start with `.` (hidden directories are ignored)

2. **"No configuration differences found"**
   - This is normal if all your configurations are identical
   - A report will still be generated confirming this

3. **Permission errors**
   - Ensure you have read permissions for all directories and files
   - Run with appropriate user privileges

4. **Excel file locked**
   - Close any existing Excel files with the same name
   - Choose a different output filename

### Verbose Mode

Use `--verbose` flag to see detailed information about:
- Which files are being processed
- How many keys are found in each file
- Any parsing warnings or errors

## Requirements

- Python 3.7 or higher
- pandas >= 1.5.0
- openpyxl >= 3.1.0

## Performance Considerations

- The tool is optimized for typical configuration file sizes
- For very large directories (100+ hosts), consider running with verbose mode to monitor progress
- Excel file size will grow with the number of differences found

## Contributing

Feel free to submit issues or improvements to this tool. Common enhancement areas:
- Additional file format support
- Custom parsing rules
- Alternative output formats (CSV, JSON)
- Performance optimizations for large datasets