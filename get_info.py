import re
import os
import sqlite3

file_path = "putty.log"
codes  = {
    1 : "Memory Monitor Test",
    2 : "Runtime Test"
}


class TestMod:
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.result = []

testObjects = []

def print_tests():
    print("\n=== Test Analysis Results ===")
    for i, test in enumerate(testObjects, 1):
        print(f"\nTest #{i}")
        print(f"Code: {test.code}")
        print(f"Type: {test.name}")
        print("Results:")
        for line in test.result:
            print(f"  {line}")
        print("-" * 40)

def getInfo(fileName):
    try:
        pattern = "Test#"
        global testObjects
        global codes

        with open(fileName) as file:
            sections = []
            current_section = []
            start = False

            for line in file:
                match = re.search(pattern, line)

                if match is not None:
                    start = True
                    if current_section:
                        testObjects[-1].result = current_section  # Assign previous section to last object
                        sections.append(current_section)
                    current_section = []  # Reset for new section

                    begin = match.end()
                    code = line[begin:begin+3].strip()

                    try:
                        code = int(code)  # Convert extracted code to an integer
                    except ValueError:
                        print(f"Warning: '{code}' is not a valid integer.")
                        continue

                    testObjects.append(TestMod(code, codes.get(code, "Unknown Code")))

                elif start and (line.strip() != "") and (line.strip() != "Test end"):
                    current_section.append(line.strip())

                # If "Test end" appears, finalize current section and move to the next
                if "Test end" in line:
                    if current_section:
                        testObjects[-1].result = current_section
                        sections.append(current_section)
                        current_section = []  # Reset for next section
                        start = False  # Stop collecting until next "Test#"

            # Append the last section if it wasn't finalized before
            if current_section:
                testObjects[-1].result = current_section
                sections.append(current_section)

    except FileNotFoundError:
        print(f"Error: File '{fileName}' not found.")
    except Exception as e:
        print(f"Error: {e}")

# Remove the automatic execution
# 
getInfo(file_path)
# print_tests()
