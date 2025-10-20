#Initial idea for structure

def allow_access():

    password = input("Please enter the password:").lower()
    if password == "password":
        print("Access to inventory system granted")
        show_menu()
    else:
        print("Access to inventory system denied")
        allow_access()

def print_inventory():
    print("Inventory printed")

def search_item():
    print("Searching for an item")

def add_item():
    print("Adding an item")

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

        choice = input("Enter your choice:")

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



print("Welcome to the Inventory System!")
user_name = input("Please enter your Username:")
allow_access()

