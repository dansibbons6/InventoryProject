# Added functional detail for working with CSV files
import os, csv
from datetime import datetime

CSV_PATH = "inventory.csv"
COLUMNS = ["item_id", "item_name", "quantity", "unit", "added_by", "date_added"]

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
    password = input("Please enter the password:").lower().strip()
    if password == "password":
        print("Access to inventory system granted")
        show_menu()
    else:
        print("Access to inventory system denied")
        allow_access()


def print_inventory():
    print("Inventory printed")
    print("\n--- All Items ---")
    rows = read_all_rows()
    if not rows:
        print("No items found.\n")
        return

    print(f"{'ID':>3} {'Name':<20} {'Qty':>4} {'Unit':<4} {'Added By':<12} {'Date'}")
    for r in rows:
        print(f"{r.get('item_id', ''):>3} {r.get('item_name', ''):<20}"
              f"{r.get('quantity', ''):>4} {r.get('unit', ''):<4}"
              f"{r.get('added_by', ''):<12} {r.get('date_added', '')}")
    print()

def search_item():
    print("Searching for an item")


def add_item():
    print("Adding an item")
    print("Adding new item")
    name = input("Item name: ").strip()
    qty_text = input("Quantity (whole number): ").strip()
    unit = input("Unit (e.g., pcs): ").strip()
    added_by = input("Your name: ").strip()

    try:
        qty = int(qty_text)
        if qty <= 0:
            print("Quantity must be greater than 0.\n")
            return
    except ValueError:
        print("Quantity must be a whole number.\n")
        return

    row = {"item_id": next_item_id(),
           "item_name": name,
           "quantity": str(qty),
           "unit": unit,
           "added_by": added_by,
           "date_added": datetime.now().strftime("%Y-%m-%d"),
           }
    append_row(row)
    print("Item added \n")

def delete_item():
    print("Deleting an item")


def exit_inventory_system():
    print("Exiting inventory system")


def show_menu():
    print('''                   Inventory system menu

                 1 - Print inventory
                 2 - Search for an item
                 3 - Add an item
                 4 - Delete an item
                 5 - Exit inventory system''')

    choice = input("Enter your choice:").strip()

    if choice == "1":
        print("Printing inventory system")
        print_inventory()

    elif choice == "2":
        print("Searching for an item")
        search_item()

    elif choice == "3":
        print("Adding an item")
        add_item()

    elif choice == "4":
        print("Deleting an item")
        delete_item()

    elif choice == "5":
        print("Exiting inventory system")
        exit_inventory_system()

    else:
        print("Invalid choice")
        show_menu()


def main():
    print("Welcome to the Inventory System!")
    user_name = input("Please enter your Username:")
    allow_access()


if __name__ == "__main__":
    main()

