import sqlite3
from datetime import datetime
from get_info import TestMod, codes, testObjects, getInfo
import pandas as pd
import os
import sys

def create_database():
    """Creates the database and table if they don't exist"""
    try:
        # Create a connection to the database (or create it if it doesn't exist)
        conn = sqlite3.connect('test_results.db')
        cursor = conn.cursor()

        # Create the test_results table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_code INTEGER NOT NULL,
            test_name TEXT NOT NULL,
            test_result TEXT NOT NULL,
            analysis_time TIMESTAMP NOT NULL
        )
        ''')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        print("Database structure verified successfully.")
    except Exception as e:
        print(f"Error creating database structure: {e}")

def update_database():
    """Analyzes the log file, updates database, and refreshes Excel sheet"""
    try:
        # Create database and table first
        create_database()
        
        # Analyze the log file
        getInfo("putty.log")
        
        # Connect to database
        conn = sqlite3.connect('test_results.db')
        cursor = conn.cursor()
        
        current_time = datetime.now()
        
        # Insert new test results
        for test in testObjects:
            result_str = '\n'.join(test.result)
            test_name = codes.get(test.code, "Unknown Test")
            
            cursor.execute('''
            INSERT INTO test_results (test_code, test_name, test_result, analysis_time)
            VALUES (?, ?, ?, ?)
            ''', (test.code, test_name, result_str, current_time))
        
        conn.commit()
        conn.close()
        print("Database updated successfully with new test results.")
        
        # Update Excel sheet
        create_excel_sheet()
        
    except Exception as e:
        print(f"Error in update process: {e}")

def create_excel_sheet():
    """Creates or updates an Excel sheet with database information"""
    try:
        # Connect to the database
        conn = sqlite3.connect('test_results.db')
        
        # Read the data into a pandas DataFrame
        df = pd.read_sql_query("SELECT * FROM test_results", conn)
        
        # Format the analysis_time column
        df['analysis_time'] = pd.to_datetime(df['analysis_time']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Create or update Excel file
        excel_file = 'test_results.xlsx'
        if os.path.exists(excel_file):
            # If file exists, create a backup
            backup_file = f'test_results_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            os.rename(excel_file, backup_file)
        
        # Write to Excel
        df.to_excel(excel_file, index=False, sheet_name='Test Results')
        print(f"Excel sheet created/updated successfully: {excel_file}")
        
        conn.close()
    except Exception as e:
        print(f"Error creating Excel sheet: {e}")

def reset_database():
    """Resets the database and Excel files by removing them"""
    try:
        # Remove database file if it exists
        if os.path.exists('test_results.db'):
            os.remove('test_results.db')
            print("Database file removed successfully.")
        
        # Remove Excel file if it exists
        if os.path.exists('test_results.xlsx'):
            os.remove('test_results.xlsx')
            print("Excel file removed successfully.")
            
        # Remove any backup Excel files
        for file in os.listdir('.'):
            if file.startswith('test_results_backup_') and file.endswith('.xlsx'):
                os.remove(file)
                print(f"Backup file {file} removed successfully.")
                
        print("Reset completed successfully.")
    except Exception as e:
        print(f"Error during reset: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    else:
        update_database()

