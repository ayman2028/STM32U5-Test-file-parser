from create_database import update_database, reset_database, create_excel_sheet, create_database

def print_menu():
    print("\n=== STM32U5 Test File Parser ===")
    print("1. Analyze log file and update database")
    print("2. Generate Excel file from database")
    print("3. Reset database and Excel files")
    print("4. Exit")
    print("================================")

def main():
    create_database()
    while True:
        print_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            print("\nAnalyzing log file and updating database...")
            update_database()
        elif choice == "2":
            print("\nGenerating Excel file from database...")
            create_excel_sheet()
        elif choice == "3":
            confirm = input("\nAre you sure you want to reset the database? This will delete all data! (y/n): ").strip().lower()
            if confirm == 'y':
                reset_database()
            else:
                print("Reset cancelled.")
        elif choice == "4":
            print("\nExiting program. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 