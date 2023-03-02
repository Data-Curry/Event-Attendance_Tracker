import database

menu = """Please select one of the following options:
1) Add new event.
2) View upcoming events.
3) View all events.
4) Attend an event.
5) View attended events.
6) Exit.

Your selection: """
welcome = "Welcome to the Event Attendance Tracker."


print(welcome)
database.create_tables()

while (user_input := input(menu)) != "6":
    if user_input == "1":
        pass
    elif user_input == "2":
        pass
    elif user_input == "3":
        pass
    elif user_input == "4":
        pass
    elif user_input == "5":
        pass
    else:
        print("Invalid input, please try again.")
        