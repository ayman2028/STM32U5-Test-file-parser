# STM32U5-Test-file-parser

## File Descriptions

### get_info.py
This Python script is designed to parse test log files (default: "putty.log") and extract test information. It:

- Processes log files containing test results marked with "Test#" patterns
- Identifies different test types using numeric codes (e.g., 1 for "Memory Monitor Test", 2 for "Runtime Test")
- Organizes test results into sections based on test boundaries
- Creates TestMod objects to store test codes and their corresponding results
- Handles file reading errors and invalid test codes gracefully

The script is particularly useful for analyzing and organizing test output from STM32U5 device testing.