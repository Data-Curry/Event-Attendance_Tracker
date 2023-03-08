import datetime
import database

menu = """Please select one of the following options:
1) Add new event.
2) View upcoming events.
3) View all events.
4) Attend an event.
5) View attended events.
6) Add new person to this app.
7) Exit.

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


def print_event_list(events, heading):
    print(f"-- {heading} Events --")
    for _id, event, event_timestamp in events:
        event_time = datetime.datetime.fromtimestamp(event_timestamp)
        human_time = event_time.strftime("%b %d %y")
        print(f"{_id}: {event} (on {human_time})")
    print("---- \n")


def prompt_attend_event():
    person_name = input("Enter the name of the attendee: ")
    event_id = input("Enter event ID: ")
    database.attend_event(person_name, event_id)
    print(f"Event {event_id} attended by {person_name}.")


def prompt_get_attended_events():
    person = input("Enter person's name: ")
    events = database.get_attended_events(person,)
    print_attended_events(events, person)


def print_attended_events(events, person):
    print(f"-- {person}'s Attended Events --")
    for event in events:
        print(f"{event[1]}")
    print("---- \n")


def prompt_add_person():
    person_name = input("Enter name: ")
    database.add_person(person_name)


while (user_input := input(menu)) != "7":
    if user_input == "1":
        prompt_add_event()
    elif user_input == "2":
        events = database.get_events(upcoming=True)
        heading = "Upcoming"
        print_event_list(events, heading)
    elif user_input == "3":
        events = database.get_events()
        heading = "All"
        print_event_list(events, heading)
    elif user_input == "4":
        prompt_attend_event()
    elif user_input == "5":
        prompt_get_attended_events()
    elif user_input == "6":
        prompt_add_person()
    else:
        print("Invalid input, please try again.")
