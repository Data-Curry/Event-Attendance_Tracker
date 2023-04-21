import datetime
import database

import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from windows import set_dpi_awareness

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

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


class MainMenu(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        add_event_button = ttk.Button(
            self,
            text="Add New Event",
            command=lambda: controller.show_frame(AddEvent)
        )
        view_upcoming_events_button = ttk.Button(
            self,
            text="View Upcoming Events",
            command=lambda: controller.show_frame(ViewUpcomingEvents)
        )
        view_events_chronologically_button = ttk.Button(
            self,
            text="View All Events Chronologically",
            command=lambda: controller.show_frame(ViewEventsChronologically)
        )
        view_events_by_id_button = ttk.Button(
            self,
            text="View All Events by ID",
            command=lambda: controller.show_frame(ViewEventsByID)
        )
        attend_event_button = ttk.Button(
            self,
            text="Attend Event",
            command=lambda: controller.show_frame(AttendEvent)
        )
        view_attended_events_button = ttk.Button(
            self,
            text="View Attended Events",
            command=lambda: controller.show_frame(ViewAttendedEvents)
        )
        add_person_button = ttk.Button(
            self,
            text="Add New Person to this App",
            command=lambda: controller.show_frame(AddNewPerson)
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

        self.event = tk.StringVar()
        self.event_value = tk.StringVar(value="Enter event here")
        self.event_date = tk.StringVar()
        self.event_date_value = tk.StringVar(value="dd-mm-yyyy")

        event_label = ttk.Label(self, text="Event name")
        event_label_input = ttk.Entry(self, width=50, textvariable=self.event, font=("Segoe UI", 15))
        event_date_label = ttk.Label(self, text="Event date")
        event_date_label_input = ttk.Entry(self, width=10, textvariable=self.event_date, font=("Segoe UI", 15))
        add_event_button = ttk.Button(self, text="Add Event", command=self.add_new_event)
        return_to_main_menu = ttk.Button(
            self,
            text="Return to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        event_label.grid(column=0, row=0, sticky="W")
        event_label_input.grid(column=1, row=0, sticky="EW")
        event_date_label.grid(column=0, row=1, sticky="W")
        event_date_label_input.grid(column=1, row=1, sticky="EW")
        add_event_button.grid(column=0, row=2, columnspan=2, sticky="W")
        return_to_main_menu.grid(column=0, row=3, columnspan=2, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=15)

    def add_new_event(self, event, event_date):
        parsed_date = datetime.datetime.strptime(event_date, "%d-%m-%y")
        timestamp = parsed_date.timestamp()
        database.add_event(event, timestamp)


class ViewUpcomingEvents(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.events = tk.StringVar(value="No upcoming events")

        upcoming_events_label = ttk.Label(self, text="Upcoming Events")
        upcoming_events_display = tk.Listbox(self, listvariable=self.events, height=8, width=50)
        return_to_main_menu = ttk.Button(
            self,
            text="Return to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        upcoming_events_label.grid(column=0, row=0, sticky="EW")
        upcoming_events_display.grid(column=0, row=1, sticky="EW")
        return_to_main_menu.grid(column=0, row=2, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=15)


class ViewEventsChronologically(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.events = tk.StringVar(value="No events registered yet")

        events_chronologically_label = ttk.Label(self, text="All Events Chronologically")
        events_chronologically_display = tk.Listbox(self, listvariable=self.events, height=8, width=50)
        return_to_main_menu = ttk.Button(
            self,
            text="Return to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        events_chronologically_label.grid(column=0, row=0, sticky="EW")
        events_chronologically_display.grid(column=0, row=1, sticky="EW")
        return_to_main_menu.grid(column=0, row=2, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=15)


class ViewEventsByID(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.events = tk.StringVar(value="No events registered yet")

        events_by_id_label = ttk.Label(self, text="All Events by ID")
        events_by_id_display = tk.Listbox(self, listvariable=self.events, height=8, width=50)
        return_to_main_menu = ttk.Button(
            self,
            text="Return to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        events_by_id_label.grid(column=0, row=0, sticky="EW")
        events_by_id_display.grid(column=0, row=1, sticky="EW")
        return_to_main_menu.grid(column=0, row=2, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=15)


class AttendEvent(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.event = tk.StringVar()
        self.event_value = tk.StringVar()
        self.person = tk.StringVar()
        self.person_value = tk.StringVar()

        event_label = ttk.Label(self, text="Event ID:")
        event_label_input = ttk.Entry(self, width=50, textvariable=self.event_value, font=("Segoe UI", 15))
        person_label = ttk.Label(self, text="Person's name:")
        person_label_input = ttk.Entry(self, width=50, textvariable=self.person_value, font=("Segoe UI", 15))
        attend_event_button = ttk.Button(self, text="Attend Event", command=self.attend_event)
        return_to_main_menu = ttk.Button(
            self,
            text="Return to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        event_label.grid(column=0, row=0, sticky="W")
        event_label_input.grid(column=1, row=0, sticky="EW")
        person_label.grid(column=0, row=1, sticky="W")
        person_label_input.grid(column=1, row=1, sticky="EW")
        attend_event_button.grid(column=0, row=2, sticky="W")
        return_to_main_menu.grid(column=0, row=3, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=15)

    def attend_event(self, event_id, person):
        pass


class ViewAttendedEvents(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.person = tk.StringVar()
        self.person_value = tk.StringVar()
        self.events = tk.StringVar(value="No events attended")

        person_label = ttk.Label(self, text="Person's name:")
        person_label_input = ttk.Entry(self, width=50, textvariable=self.person_value, font=("Segoe UI", 15))
        attended_events_display = tk.Listbox(self, listvariable=self.events, height=8)
        view_attended_events_button = ttk.Button(self, text="View Attended Events", command=self.view_attended_events)
        return_to_main_menu = ttk.Button(
            self,
            text="Return to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        person_label.grid(column=0, row=0, sticky="EW")
        person_label_input.grid(column=1, row=0, sticky="EW")
        attended_events_display.grid(column=0, row=1, columnspan=2, sticky="EW")
        view_attended_events_button.grid(column=0, row=2, sticky="EW")
        return_to_main_menu.grid(column=1, row=2, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=15)

    def view_attended_events(self, person):
        pass


class AddNewPerson(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.person = tk.StringVar()
        self.person_value = tk.StringVar()

        person_label = ttk.Label(self, text="New Person's Name:")
        person_label_input = ttk.Entry(self, width=50, textvariable=self.person_value, font=("Segoe UI", 15))
        add_person_button = ttk.Button(self, text="Add Person", command=self.add_new_person)
        return_to_main_menu = ttk.Button(
            self,
            text="Return to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        person_label.grid(column=0, row=0, sticky="W")
        person_label_input.grid(column=0, row=1, sticky="EW")
        add_person_button.grid(column=0, row=2, sticky="EW")
        return_to_main_menu.grid(column=0, row=3, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=15)

    def add_new_person(self, person):
        pass


root = EventAttendanceTracker()
root.geometry("800x425")
root.resizable(False, False)

font.nametofont("TkDefaultFont").configure(size=15)

root.columnconfigure(0, weight=1)

database.create_tables()

root.mainloop()
