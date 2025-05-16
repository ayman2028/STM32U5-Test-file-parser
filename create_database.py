import sqlite3
from datetime import datetime
from get_info import TestMod, codes, testObjects

def create_database():
    # Create a connection to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('test_results.db')
    cursor = conn.cursor()

    # Create the test_results table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS test_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_code INTEGER NOT NULL,
        test_name TEXT NOT NULL,
        test_result TEXT NOT NULL,
        analysis_time TIMESTAMP NOT NULL
    )
    ''')

    # Get current timestamp
    current_time = datetime.now()

    # Insert test results into the database
    for test in testObjects:
        # Convert the result list to a string
        result_str = '\n'.join(test.result)
        
        # Get test name from the codes dictionary
        test_name = codes.get(test.code, "Unknown Test")
        
        cursor.execute('''
        INSERT INTO test_results (test_code, test_name, test_result, analysis_time)
        VALUES (?, ?, ?, ?)
        ''', (test.code, test_name, result_str, current_time))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Database created successfully with test results.")

if __name__ == "__main__":
    create_database() 