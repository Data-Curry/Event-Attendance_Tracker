import datetime
import database

import tkinter as tk
from tkinter import ttk
from windows import set_dpi_awareness

set_dpi_awareness()


root = tk.Tk()
root.geometry("600x400")
root.resizable(False, False)
root.title("Event Attendance Tracker")

database.create_tables()


def input_2():
    events = database.get_events(upcoming=True)
    heading = "Upcoming"
    print_event_list(events, heading)


def input_3():
    events = database.get_events_chronologically()
    heading = "All"
    print_event_list(events, heading)


def input_4():
    events = database.get_events()
    heading = "All"
    print_event_list(events, heading)


def input_6():
    person = input("Enter person's name: ")
    person_exists = database.get_person(person)
    if person_exists:
        events = database.get_attended_events(person, )
        if events:
            heading = f"{person}'s Attended"
            print_event_list(events, heading)
        else:
            print(f"{person} hasn't attended any events.\n")
    else:
        print(f"{person} is not found in the database.\n")


def input_7():
    pass


def input_8():
    pass


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
        human_time = event_time.strftime("%b %d %Y")
        print(f"{_id}: {event} ({human_time})")
    print("---- \n")


def prompt_attend_event():
    person_name = input("Enter the name of the attendee: ")
    person_exists = database.get_person(person_name)
    if person_exists:
        event_id = input("Enter event ID: ")
        event_exists = database.get_event(event_id)
        if event_exists:
            database.attend_event(person_name, event_id)
            print(f"Event {event_id} attended by {person_name}.")
        else:
            print(f"Event with ID {event_id} is not found in the database.\n")
    else:
        print(f"{person_name} is not found in the database.\n")


def prompt_add_person():
    person_name = input("Enter name: ")
    database.add_person(person_name)


main = ttk.Frame(root, padding=(30, 15))
main.grid()

# -- Widgets --

add_event_button = ttk.Button(main, text="Add New Event", command=prompt_add_event)
view_upcoming_events_button = ttk.Button(main, text="View Upcoming Events", command=input_2)
view_events_chronologically_button = ttk.Button(main, text="View All Events Chronologically", command=input_3)
view_events_by_id_button = ttk.Button(main, text="View All Events by ID", command=input_4)
attend_event_button = ttk.Button(main, text="Attend Event", command=prompt_attend_event)
view_attended_events_button = ttk.Button(main, text="View Attended Events", command=input_6)
add_person_button = ttk.Button(main, text="Add New Person to this App", command=prompt_add_person)
exit_app_button = ttk.Button(main, text="Exit App", command=input_8)

# -- Layout --

add_event_button.grid(column=0, row=0, sticky="W", padx=5, pady=5)
view_upcoming_events_button.grid(column=0, row=1, sticky="W", padx=5, pady=5)
view_events_chronologically_button.grid(column=0, row=2, sticky="W", padx=5, pady=5)
view_events_by_id_button.grid(column=0, row=3, sticky="W", padx=5, pady=5)
attend_event_button.grid(column=0, row=4, sticky="W", padx=5, pady=5)
view_attended_events_button.grid(column=0, row=5, sticky="W", padx=5, pady=5)
add_person_button.grid(column=0, row=6, sticky="W", padx=5, pady=5)
exit_app_button.grid(column=0, row=7, sticky="W", padx=5, pady=5)


root.mainloop()