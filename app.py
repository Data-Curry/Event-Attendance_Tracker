import datetime
import database

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
from windows import set_dpi_awareness
from scrollable_window import ViewItemsByIDDisplayWindow, \
    ViewEventsChronologicallyDisplayWindow, \
    ViewUpcomingEventsDisplayWindow, \
    ViewAttendedEventsDisplayWindow


attended_events = ()
upcoming_events = ()
events_chronologically = ()
events_by_id = ()

set_dpi_awareness()


class EventAttendanceTracker(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Event Attendance Tracker")
        self.frames = dict()

        container = ttk.Frame(self)
        container.grid(padx=60, pady=30, sticky="EW")

        for FrameClass in (MainMenu, AddEvent, ViewUpcomingEvents, ViewEventsChronologically, ViewEventsByID,
                           AttendEvent, ViewAttendedEvents, AddNewPerson):
            frame = FrameClass(container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        self.show_frame(MainMenu)

    def show_frame(self, container):       # switches view from current frame to frame passed in container
        frame = self.frames[container]
        frame.tkraise()                    # puts this frame on top of the stack of frames


class MainMenu(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        add_event_button = ttk.Button(
            self,
            text="Add New Event",
            command=lambda: controller.show_frame(AddEvent)  # switches to AddEvent class frame
        )
        view_upcoming_events_button = ttk.Button(
            self,
            text="View Upcoming Events",
            command=lambda: controller.show_frame(ViewUpcomingEvents)  # switches to ViewUpcomingEvents class frame
        )
        view_events_chronologically_button = ttk.Button(
            self,
            text="View All Events Chronologically",
            command=lambda: controller.show_frame(ViewEventsChronologically)  # switches to ViewEventsChronologically class frame
        )
        view_events_by_id_button = ttk.Button(
            self,
            text="View All Events by ID",
            command=lambda: controller.show_frame(ViewEventsByID)  # switches to ViewEventsByID class frame
        )
        attend_event_button = ttk.Button(
            self,
            text="Attend Event",
            command=lambda: controller.show_frame(AttendEvent)  # switches to AttendEvent class frame
        )
        view_attended_events_button = ttk.Button(
            self,
            text="View Attended Events",
            command=lambda: controller.show_frame(ViewAttendedEvents)  # switches to ViewAttendedEvents class frame
        )
        add_person_button = ttk.Button(
            self,
            text="Add New Person to this App",
            command=lambda: controller.show_frame(AddNewPerson)  # switches to AddNewPerson class frame
        )
        exit_app_button = ttk.Button(self, text="Exit App", command=exit)

        add_event_button.grid(column=0, row=0, sticky="W")
        view_upcoming_events_button.grid(column=0, row=1, sticky="W")
        view_events_chronologically_button.grid(column=0, row=2, sticky="W")
        view_events_by_id_button.grid(column=0, row=3, sticky="W")
        attend_event_button.grid(column=0, row=4, sticky="W")
        view_attended_events_button.grid(column=0, row=5, sticky="W")
        add_person_button.grid(column=0, row=6, sticky="W")
        exit_app_button.grid(column=0, row=7, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)


class AddEvent(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.event_value = tk.StringVar()
        self.event_date_value = tk.StringVar(value="dd-mm-yyyy")

        event_label = ttk.Label(self, text="Event name", font=("Segoe UI", 15, "bold"))
        event_label_input = ttk.Entry(self, width=45, textvariable=self.event_value, font=("Segoe UI", 15))
        event_date_label = ttk.Label(self, text="Event date", font=("Segoe UI", 15, "bold"))
        event_date_label_input = ttk.Entry(self, width=11, textvariable=self.event_date_value, font=("Segoe UI", 15))
        add_event_button = ttk.Button(
            self, text="Add Event",
            command=lambda: self.add_new_event(self.event_value.get(), self.event_date_value.get())
        )
        return_to_main_menu = ttk.Button(
            self,
            text="Return to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        event_label.grid(column=0, row=0, sticky="W")
        event_label_input.grid(column=1, row=0, sticky="EW")
        event_date_label.grid(column=0, row=1, sticky="W")
        event_date_label_input.grid(column=1, row=1, sticky="W")
        add_event_button.grid(column=0, row=2, columnspan=2, sticky="W")
        return_to_main_menu.grid(column=0, row=3, columnspan=2, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=15)

    def get_events(self):
        events = database.get_events()
        return events

    def check_if_event_in_db(self, event_string, timestamp):  # checks if event is already in db
        event_list = self.get_events()                        # events in db is a list of tuples
        for _id, event, event_stamp in event_list:            # iterates through elements of each tuple
            if event_string == event and timestamp == event_stamp:
                messagebox.showinfo(
                    title="Event exists!",
                    message=f"The event you entered is already in the database. It's ID: {_id}"
                )
                return True
            else:
                return False

    def add_new_event(self, event, event_date):
        event_string = str(event)
        event_date_string = str(event_date)

        if len(event_string) == 0 or len(event_date_string) == 0:
            messagebox.showinfo(title="Oops!", message="Make sure you entered the information correctly.")
        else:
            try:
                parsed_date = datetime.datetime.strptime(event_date_string, "%d-%m-%Y")
            except ValueError:
                messagebox.showinfo(title="Oops!", message="Make sure you entered the date in dd-mm-yyyy format.")
            else:
                timestamp = parsed_date.timestamp()
                event_exists = self.check_if_event_in_db(event_string, timestamp)  # checks if event in db already
                if not event_exists:
                    database.add_event(event_string, timestamp)
                    messagebox.showinfo(title="Success!", message=f"{event_string} added!")


class ViewUpcomingEvents(ttk.Frame):
    global upcoming_events

    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.upcoming_events = ()

        self.upcoming_events_window = ViewUpcomingEventsDisplayWindow(self)  # scrollable window
        self.upcoming_events_window.grid(column=0, row=1, sticky="NSEW")

        upcoming_events_label = ttk.Label(
            self,
            text="           Upcoming Events  --  ID: Event (Date)           ",
            font=("Segoe UI", 15, "bold", "underline")
        )
        display_events_button = ttk.Button(
            self,
            text="Click to display upcoming events",
            command=self.get_events)
        return_to_main_menu = ttk.Button(
            self,
            text="Return to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        upcoming_events_label.grid(column=0, row=0, sticky="EW")
        display_events_button.grid(column=0, row=2, sticky="W")
        return_to_main_menu.grid(column=1, row=2, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=5)

    def get_events(self):
        events = database.get_events(upcoming=True)
        final_list = self.make_upcoming_event_list(events)  # make list into readable format
        return final_list

    def make_upcoming_event_list(self, events):
        global upcoming_events
        event_list = []
        no_duplication = ()
        for _id, event, event_timestamp in events:
            event_time = datetime.datetime.fromtimestamp(event_timestamp)
            human_time = event_time.strftime("%b %d %Y")
            list_line = f"{_id}: {event} ({human_time})"
            event_list.append(list_line)
        event_tuple = tuple(event_list)
        if event_tuple == upcoming_events:                  # if display button is clicked again,
            return no_duplication                           # don't return the event list again
        else:
            upcoming_events = event_tuple
            self.upcoming_events_window.update_upcoming_events_widgets(upcoming_events)
            return upcoming_events


class ViewEventsChronologically(ttk.Frame):
    global events_chronologically

    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.events_chronologically_window = ViewEventsChronologicallyDisplayWindow(self)  # scrollable window
        self.events_chronologically_window.grid(column=0, row=1, sticky="NSEW")

        events_chronologically_label = ttk.Label(
            self,
            text="   All Events Chronologically  --  ID: Event (Date)   ",
            font=("Segoe UI", 15, "bold", "underline")
        )
        display_events_button = ttk.Button(
            self,
            text="Click to display events chronologically",
            command=self.get_events)
        return_to_main_menu = ttk.Button(
            self,
            text="Return to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        events_chronologically_label.grid(column=0, row=0, sticky="EW")
        display_events_button.grid(column=0, row=2, sticky="W")
        return_to_main_menu.grid(column=1, row=2, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=5)

    def get_events(self):
        events = database.get_events_chronologically()
        final_list = self.make_events_chronologically_list(events)  # makes list into readable format
        return final_list

    def make_events_chronologically_list(self, events):
        global events_chronologically
        event_list = []
        no_duplication = ()
        for _id, event, event_timestamp in events:
            event_time = datetime.datetime.fromtimestamp(event_timestamp)
            human_time = event_time.strftime("%b %d %Y")
            list_line = f"{_id}: {event} ({human_time})"
            event_list.append(list_line)
        event_tuple = tuple(event_list)
        if event_tuple == events_chronologically:          # if display button is clicked again,
            return no_duplication                          # don't return the event list again
        else:
            events_chronologically = event_tuple
            self.events_chronologically_window.update_events_chronologically_widgets(events_chronologically)  # in scrollable_window.py
            return events_chronologically


class ViewEventsByID(ttk.Frame):
    global events_by_id

    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.events_by_id_window = ViewItemsByIDDisplayWindow(self)  # scrollable window
        self.events_by_id_window.grid(column=0, row=1, sticky="NSEW")

        events_by_id_label = ttk.Label(
            self,
            text="             All Events by ID  --  ID: Event (Date)             ",
            font=("Segoe UI", 15, "bold", "underline")
        )
        display_events_button = ttk.Button(self, text="Click to display events by ID",
                                           command=self.get_events)

        return_to_main_menu = ttk.Button(
            self,
            text="Return to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        events_by_id_label.grid(column=0, row=0, sticky="EW")
        display_events_button.grid(column=0, row=2, sticky="W")
        return_to_main_menu.grid(column=1, row=2, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=5)

    def get_events(self):
        events = database.get_events()
        final_list = self.make_events_by_id_list(events)    # makes list into readable format
        return final_list

    def make_events_by_id_list(self, events):
        global events_by_id
        event_list = []
        no_duplication = ()
        for _id, event, event_timestamp in events:
            event_time = datetime.datetime.fromtimestamp(event_timestamp)
            human_time = event_time.strftime("%b %d %Y")
            list_line = f"{_id}: {event} ({human_time})"
            event_list.append(list_line)
        event_tuple = tuple(event_list)
        if event_tuple == events_by_id:          # if the display button is clicked again,
            return no_duplication                # don't return the event list again
        else:
            events_by_id = event_tuple
            self.events_by_id_window.update_events_by_id_widgets(events_by_id)  # method in scrollable_window.py
            return events_by_id


class AttendEvent(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.event = tk.StringVar()
        self.event_value = tk.StringVar()
        self.person = tk.StringVar()
        self.person_value = tk.StringVar()

        event_label = ttk.Label(self, text="Event ID:", font=("Segoe UI", 15, "bold"))
        event_label_input = ttk.Entry(self, width=45, textvariable=self.event_value, font=("Segoe UI", 15))
        person_label = ttk.Label(self, text="Person's name:", font=("Segoe UI", 15, "bold"))
        person_label_input = ttk.Entry(self, width=45, textvariable=self.person_value, font=("Segoe UI", 15))
        attend_event_button = ttk.Button(
            self,
            text="Attend Event",
            command=lambda: self.attend_event(person_label_input.get(), event_label_input.get())
        )
        return_to_main_menu = ttk.Button(
            self,
            text="Return to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        event_label.grid(column=0, row=0, sticky="E")
        event_label_input.grid(column=1, row=0, sticky="EW")
        person_label.grid(column=0, row=1, sticky="E")
        person_label_input.grid(column=1, row=1, sticky="EW")
        attend_event_button.grid(column=0, row=2, sticky="W")
        return_to_main_menu.grid(column=0, row=3, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=15)

    def check_if_person_in_database(self, person_string):
        person_name = database.get_person(person_string)
        return person_name

    def check_if_event_in_database(self, event_id_string):
        event = database.get_event(event_id_string)
        return event

    def attend_event(self, person, event_id):
        person_string = str(person)
        event_id_string = str(event_id)
        if len(person_string) == 0 or len(event_id_string) == 0:
            messagebox.showinfo(
                title="Oops!",
                message="Make sure you entered the information correctly."
            )
        person_check = self.check_if_person_in_database(person_string)  # ensures db entry uses person already in db
        if len(person_check) == 0:
            messagebox.showinfo(
                title="Not in database!",
                message=f"{person_string} is not in the database.  You must first add {person_string} to the database "
                        f"with the Add Person button on the Main Menu."
            )
        event_check = self.check_if_event_in_database(event_id_string)  # ensures db entry uses event already in db
        if len(event_check) == 0:
            messagebox.showinfo(
                title="Not in database!",
                message=f"The event with ID {event_id_string} is not in the database.  Use the View Events by ID "
                        f"button on the Main Menu to see all events in the database."
            )
        else:
            database.attend_event(person_string, event_id_string)
            messagebox.showinfo(
                title="Success!",
                message=f"{person_string} has attended the event with ID: {event_id_string}"
            )


class ViewAttendedEvents(ttk.Frame):
    global attended_events

    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.attended_events = ()

        self.attended_events_window = ViewAttendedEventsDisplayWindow(self)  # scrollable window
        self.attended_events_window.grid(column=0, row=2, sticky="NSEW")

        self.person = tk.StringVar()
        self.person_value = tk.StringVar()
        self.events = tk.StringVar(value="No events attended")

        person_label = ttk.Label(self, text="<-- Person's name", font=("Segoe UI", 15, "bold"))
        person_label_input = ttk.Entry(self, width=45, textvariable=self.person_value, font=("Segoe UI", 15))
        header = ttk.Label(
            self,
            text="                           ID: Event (Date)",
            font=("Segoe UI", 15, "bold"))
        view_attended_events_button = ttk.Button(
            self,
            text="View Attended Events",
            command=self.view_attended_events)
        return_to_main_menu = ttk.Button(
            self,
            text="Return to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        person_label.grid(column=1, row=0, sticky="E")
        person_label_input.grid(column=0, row=0, sticky="EW")
        header.grid(column=0, row=1, sticky="W")
        view_attended_events_button.grid(column=0, row=3, sticky="EW")
        return_to_main_menu.grid(column=1, row=3, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=7, pady=2)

    def view_attended_events(self):
        person = self.person_value.get()
        events = database.get_attended_events(person)
        final_list = self.make_attended_events_list(events)  # formats the list
        return final_list

    def make_attended_events_list(self, events):             # converts timestamps into readable dates
        global attended_events
        event_list = []
        no_duplication = ()
        for _id, event, event_timestamp in events:
            event_time = datetime.datetime.fromtimestamp(event_timestamp)
            human_time = event_time.strftime("%b %d %Y")
            list_line = f"{_id}: {event} ({human_time})"
            event_list.append(list_line)
        event_tuple = tuple(event_list)
        if event_tuple == attended_events:                  # if display button is clicked again,
            return no_duplication                           # don't return the event list again
        else:
            attended_events = event_tuple
            self.attended_events_window.update_attended_events_widgets(attended_events)  # in scrollable_window.py
            return attended_events


class AddNewPerson(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.person = tk.StringVar()
        self.person_value = tk.StringVar()

        header = ttk.Label(self, text="Add New Person", font=("Segoe UI", 15, "bold", "underline"))
        person_label = ttk.Label(self, text="Enter New Person's Name:", font=("Segoe UI", 15, "bold"))
        person_label_input = ttk.Entry(self, width=45, textvariable=self.person_value, font=("Segoe UI", 15))
        add_person_button = ttk.Button(
            self,
            text="Add Person",
            command=lambda: self.add_new_person(person_label_input.get())
        )
        return_to_main_menu = ttk.Button(
            self,
            text="Return to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        header.grid(column=0, row=0, sticky="EW")
        person_label.grid(column=0, row=1, sticky="W")
        person_label_input.grid(column=0, row=2, sticky="EW")
        add_person_button.grid(column=0, row=3, sticky="EW")
        return_to_main_menu.grid(column=0, row=4, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=15)

    def check_if_person_in_db(self, person):
        name_check = database.get_person(person)
        return name_check                            # returns either the person's name or an empty tuple

    def add_new_person(self, person):
        person_string = str(person)
        if len(person_string) == 0:
            messagebox.showinfo(
                title="Oops!",
                message="Make sure you enter a name."
            )
        person_exists = self.check_if_person_in_db(person_string)  # checks if person's name is in db already
        if person_exists:                                          # if the name is found in the database
            messagebox.showinfo(
                title="Name already exists!",
                message="The person you entered is already in the database."
            )
        else:                                                      # if name_check returns an empty tuple
            database.add_person(person_string)
            messagebox.showinfo(
                title="Success!",
                message=f"{person_string} added."
            )


root = EventAttendanceTracker()
root.geometry("875x500")
root.resizable(False, False)

font.nametofont("TkDefaultFont").configure(size=15)

style = ttk.Style(root)

root.columnconfigure(0, weight=1)

database.create_tables()

style.theme_use("clam")

root.mainloop()
