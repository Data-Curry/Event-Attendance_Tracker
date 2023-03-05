import datetime
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


def prompt_add_event():
    event = input("Enter event name: ")
    event_date = input("Enter event date (dd-mm-yyyy): ")
    parsed_date = datetime.datetime.strptime(event_date, "%d-%m-%Y")
    timestamp = parsed_date.timestamp()

    database.add_event(event, timestamp)


def print_events(events, heading):
    print(f"-- {heading} Events --")
    for event in events:
        print(f"{event[0]} (on {event[1]})")
    print("---- \n")


def prompt_attend_event():
    event = input("Enter name of event: ")
    database.attend_event(event)
    print(f"{event} attended.")


while (user_input := input(menu)) != "6":
    if user_input == "1":
        prompt_add_event()
    elif user_input == "2":
        events = database.get_events(upcoming=True)
        heading = "Upcoming"
        print_events(events, heading)
    elif user_input == "3":
        events = database.get_events()
        heading = "All"
        print_events(events, heading)
    elif user_input == "4":
        prompt_attend_event()
    elif user_input == "5":
        events = database.get_attended_events()
        heading = "Attended"
        print_events(events, heading)
    else:
        print("Invalid input, please try again.")
