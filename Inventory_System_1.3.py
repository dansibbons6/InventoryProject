#Made changes in structure as a result of testing and bug fixes

#import modules required
import os, csv
from datetime import datetime

#sets up required variables
CSV_PATH = "inventory.csv"
COLUMNS = ["item_id", "item_name", "quantity", "unit", "added_by", "date_added"]
csv_filename = CSV_PATH
def ensure_csv_ready():
    #Creates the CSV file with a header if it doesn't exist or is empty
    if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0:
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(COLUMNS)


def read_all_rows():
    #Read all items as a list of dicts
    ensure_csv_ready()
    with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def next_item_id():
    #Find the next numeric item_id by scanning the csv file
    rows = read_all_rows()
    max_id = 0
    for r in rows:
        try:
            max_id = max(max_id, int(r.get("item_id", "0")))
        except ValueError:
            pass
    return str(max_id + 1)


def append_row(row):
    #Append a single row to csv file without overwriting the file
    ensure_csv_ready()
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writerow(row)

def allow_access():
    #Grants access to the system if password is correct
    password = input("Please enter the password:").lower().strip()
    if password == "password":
        print("Access to inventory system granted")
        show_menu()
    else:
        print("Access to inventory system denied")
        allow_access()


def print_inventory():
    #Prints all items and information from the system
    print("\n--- All Items ---")
    rows = read_all_rows()
    if not rows:
        print("No items found.\n")
        return another_action()

    print(f"{'ID':>3} {'Name':<20} {'Qty':>4} {'Unit':<4} {'Added By':<12} {'Date'}")
    for r in rows:
        print(f"{r.get('item_id', ''):>3} {r.get('item_name', ''):<20}"
              f"{r.get('quantity', ''):>4} {r.get('unit', ''):<4}"
              f"{r.get('added_by', ''):<12} {r.get('date_added', '')}")
    print()
    another_action()

def search_item():
    #Searches the system using item_name or added_by
    print("\n--- Search Items ---")
    term = input("Enter search term (item name or added_by): ").strip().lower()
    if not term:
        print("No search term entered. Please try again.\n")
        return another_action()

    rows = read_all_rows()
    results = []
    for r in rows:
        combined = (r.get('item_name', '') + ' ' + r.get('added_by', '')).lower()
        if term in combined:
            results.append(r)

    if not results:
        print("No results found.\n")
        return another_action()

    print(f"{'ID':>3} {'Name':<20} {'Qty':>4} {'Unit':<4} {'Added By':<12} {'Date'}")
    for r in results:
        print(f"{r.get('item_id', ''):>3} {r.get('item_name', ''):<20}"
              f"{r.get('quantity',''):>4} {r.get('unit',''):<4}" 
              f"{r.get('added_by',''):<12} {r.get('date_added','')}")
    print()
    another_action()

def add_item():
    #Gets inputs from user and adds item to the system
    print("Adding new item")
    name = input("Item name: ").strip()
    qty_text = input("Quantity (whole number): ").strip()
    unit = input("Unit (e.g., pcs): ").strip()
    if unit == "":
        unit = "pcs"
    else:
        unit = unit

    added_by = input("Your name: ").strip()
    try:
        qty = int(qty_text)
        if qty <= 0:
            print("Quantity must be greater than 0.\n")
            return another_action()
    except ValueError:
        print("Quantity must be a whole number.\n")
        return another_action()

    row = {"item_id": next_item_id(),
           "item_name": name,
           "quantity": str(qty),
           "unit": unit,
           "added_by": added_by,
           "date_added": datetime.now().strftime("%Y-%m-%d"),
           }
    append_row(row)
    print("Item added \n")
    another_action()

def delete_item(csv_filename):
    #Gets the item name and deletes from the system
    term = input("Enter search term (item name): ").strip().lower()
    if not term:
        print("No search term entered. Please try again.\n")
        return another_action()

    rows = read_all_rows() #list

    for r in rows:
        combined = (r.get('item_name', '')).lower()
        if term in combined:
            #print(rows.index(r))
            row_index = rows.index(r) + 1

            rows = []
            with open(csv_filename, 'r') as file:
                reader = csv.reader(file)
                rows = [row for idx, row in enumerate(reader) if idx != row_index]
            with open(csv_filename, 'w', newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            another_action()
        else:
            print("Item name not found.\n")
            return another_action()

def exit_inventory_system():
    #Exits the program after saying 'Goodbye' to user
    print("Exiting inventory system")
    print("Goodbye")
    os._exit(0)

def show_menu():
    #Displays menu and gets user choice of action
    print('''                   Inventory system menu

                 1 - Print inventory
                 2 - Search for an item
                 3 - Add an item
                 4 - Delete an item
                 5 - Exit inventory system\n''')

    choice = input("Enter your choice:").strip()

    if choice == "1":
        print("Printing inventory system")
        print_inventory()

    elif choice == "2":
        print("Searching for an item")
        search_item()

    elif choice == "3":
        add_item()

    elif choice == "4":
        print("Deleting an item")
        delete_item(csv_filename)

    elif choice == "5":
        exit_inventory_system()

    else:
        print("Invalid choice")
        show_menu()


def another_action():
    #Asks user if they want to complete another action or exit the system
    answer = input("Do you wish to return to the menu or exit? Menu/Exit: ").lower().strip()
    if answer == "menu":
        show_menu()
    elif answer == "exit":
        exit_inventory_system()
    else:
        print("Please choose either Menu/Exit: ")
        another_action()



def main():
    #Main program
    print("Welcome to the Inventory System!")
    user_name = input("Please enter your Username:").strip()
    allow_access()


if __name__ == "__main__":
    main()