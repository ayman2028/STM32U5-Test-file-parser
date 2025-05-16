from create_database import update_database, reset_database, create_excel_sheet, create_database

def print_menu():
    print("\n=== STM32U5 Test File Parser ===")
    print("1. Analyze log file and update database")
    print("2. Generate Excel file from database")
    print("3. Reset database and Excel files")
    print("4. Exit")
    print("================================")

def main():
    update_database()

if __name__ == "__main__":
    main() 