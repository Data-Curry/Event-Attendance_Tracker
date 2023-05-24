import datetime
import database

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
from scrollable_window import DisplayWindow
from windows import set_dpi_awareness

display_data = ["This is the content of the Display Data Variable"]

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

        self.event_value = tk.StringVar()
        self.event_date_value = tk.StringVar(value="dd-mm-yyyy")

        event_label = ttk.Label(self, text="Event name")
        event_label_input = ttk.Entry(self, width=50, textvariable=self.event_value, font=("Segoe UI", 15))
        event_date_label = ttk.Label(self, text="Event date")
        event_date_label_input = ttk.Entry(self, width=10, textvariable=self.event_date_value, font=("Segoe UI", 15))
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
        event_date_label_input.grid(column=1, row=1, sticky="EW")
        add_event_button.grid(column=0, row=2, columnspan=2, sticky="W")
        return_to_main_menu.grid(column=0, row=3, columnspan=2, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=15)

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
                database.add_event(event_string, timestamp)
                messagebox.showinfo(title="Success!", message=f"{event_string} added!")


class ViewUpcomingEvents(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.upcoming_events = ()

        self.upcoming_events_window = ttk.Frame(self)
        self.upcoming_events_window.grid(column=0, row=1, sticky="NSEW")

        upcoming_events_label = ttk.Label(
            self,
            text="Upcoming Events  --  ID: Event (Date)",
            font=("Segoe UI", 15, "bold", "underline")
        )
        display_events_button = ttk.Button(self, text="Click to display upcoming events", command=self.get_events)
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
        final_list = self.make_upcoming_event_list(events)
        return final_list

    def make_upcoming_event_list(self, events):
        event_list = []
        for _id, event, event_timestamp in events:
            event_time = datetime.datetime.fromtimestamp(event_timestamp)
            human_time = event_time.strftime("%b %d %Y")
            list_line = f"{_id}: {event} ({human_time})"
            event_list.append(list_line)
        event_tuple = tuple(event_list)
        self.upcoming_events = event_tuple + self.upcoming_events
        self.update_upcoming_events_widgets()
        print(self.upcoming_events)
        return self.upcoming_events

    def update_upcoming_events_widgets(self):
        for event in self.upcoming_events:
            event_label = ttk.Label(
                self.upcoming_events_window,
                text=event,
                anchor="w",
                justify="left"
            )

            event_label.grid(sticky="NSEW")


class ViewEventsChronologically(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.events_chronologically = ()

        self.events_chronologically_window = ttk.Frame(self)
        self.events_chronologically_window.grid(column=0, row=1, sticky="NSEW")

        events_chronologically_label = ttk.Label(
            self,
            text="All Events Chronologically  --  ID: Event (Date)",
            font=("Segoe UI", 15, "bold", "underline")
        )
        display_events_button = ttk.Button(self, text="Click to display events chronologically", command=self.get_events)
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
        final_list = self.make_events_chronologically_list(events)
        return final_list

    def make_events_chronologically_list(self, events):
        event_list = []
        for _id, event, event_timestamp in events:
            event_time = datetime.datetime.fromtimestamp(event_timestamp)
            human_time = event_time.strftime("%b %d %Y")
            list_line = f"{_id}: {event} ({human_time})"
            event_list.append(list_line)
        event_tuple = tuple(event_list)
        self.events_chronologically = event_tuple + self.events_chronologically
        self.update_events_chronologically_widgets()
        print(self.events_chronologically)
        return self.events_chronologically

    def update_events_chronologically_widgets(self):
        for event in self.events_chronologically:
            event_label = ttk.Label(
                self.events_chronologically_window,
                text=event,
                anchor="w",
                justify="left"
            )

            event_label.grid(sticky="NSEW")


class ViewEventsByID(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.events_by_id = ()

        self.events_by_id_window = ttk.Frame(self)
        self.events_by_id_window.grid(column=0, row=1, sticky="NSEW")

        events_by_id_label = ttk.Label(
            self,
            text="All Events by ID  --  ID: Event (Date)",
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
        final_list = self.make_events_by_id_list(events)
        return final_list

    def make_events_by_id_list(self, events):
        event_list = []
        for _id, event, event_timestamp in events:
            event_time = datetime.datetime.fromtimestamp(event_timestamp)
            human_time = event_time.strftime("%b %d %Y")
            list_line = f"{_id}: {event} ({human_time})"
            event_list.append(list_line)
        event_tuple = tuple(event_list)
        self.events_by_id = event_tuple + self.events_by_id
        self.update_events_by_id_widgets()
        print(self.events_by_id)
        return self.events_by_id

    def update_events_by_id_widgets(self):
        for event in self.events_by_id:
            event_label = ttk.Label(
                self.events_by_id_window,
                text=event,
                anchor="w",
                justify="left"
            )

            event_label.grid(sticky="NSEW")


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

        event_label.grid(column=0, row=0, sticky="W")
        event_label_input.grid(column=1, row=0, sticky="EW")
        person_label.grid(column=0, row=1, sticky="W")
        person_label_input.grid(column=1, row=1, sticky="EW")
        attend_event_button.grid(column=0, row=2, sticky="W")
        return_to_main_menu.grid(column=0, row=3, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=15)

    def attend_event(self, person, event_id):
        person_string = str(person)
        event_id_string = str(event_id)
        if len(person_string) == 0 or len(event_id_string) == 0:
            messagebox.showinfo(
                title="Oops!",
                message="Make sure you entered the information correctly."
            )
        else:
            database.attend_event(person_string, event_id_string)
            messagebox.showinfo(
                title="Success!",
                message=f"{person_string} has attended the event with ID: {event_id_string}"
            )


class ViewAttendedEvents(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.attended_events = ()

        self.attended_events_window = ttk.Frame(self)
        self.attended_events_window.grid(column=0, row=2, sticky="NSEW")

        self.person = tk.StringVar()
        self.person_value = tk.StringVar()
        self.events = tk.StringVar(value="No events attended")

        person_label = ttk.Label(self, text="Person's name:")
        person_label_input = ttk.Entry(self, width=50, textvariable=self.person_value, font=("Segoe UI", 15))
        header = ttk.Label(self, text="ID: Event (Date)", font=("Segoe UI", 15, "bold", "underline"))
        view_attended_events_button = ttk.Button(
            self,
            text="View Attended Events",
            command=self.view_attended_events)
        return_to_main_menu = ttk.Button(
            self,
            text="Return to Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        person_label.grid(column=0, row=0, sticky="EW")
        person_label_input.grid(column=1, row=0, sticky="EW")
        header.grid(column=0, row=1, sticky="W")
        view_attended_events_button.grid(column=0, row=3, sticky="EW")
        return_to_main_menu.grid(column=1, row=3, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=5)

    def view_attended_events(self):
        person = self.person_value.get()
        events = database.get_attended_events(person)
        final_list = self.make_attended_events_list(events)
        return final_list

    def make_attended_events_list(self, events):
        event_list = []
        for _id, event, event_timestamp in events:
            event_time = datetime.datetime.fromtimestamp(event_timestamp)
            human_time = event_time.strftime("%b %d %Y")
            list_line = f"{_id}: {event} ({human_time})"
            event_list.append(list_line)
        event_tuple = tuple(event_list)
        self.attended_events = event_tuple + self.attended_events
        self.update_attended_events_widgets()
        print(self.attended_events)
        return self.attended_events

    def update_attended_events_widgets(self):
        for event in self.attended_events:
            event_label = ttk.Label(
                self.attended_events_window,
                text=event,
                anchor="w",
                justify="left"
            )

            event_label.grid(sticky="NSEW")


class AddNewPerson(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.person = tk.StringVar()
        self.person_value = tk.StringVar()

        person_label = ttk.Label(self, text="New Person's Name:")
        person_label_input = ttk.Entry(self, width=50, textvariable=self.person_value, font=("Segoe UI", 15))
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

        person_label.grid(column=0, row=0, sticky="W")
        person_label_input.grid(column=0, row=1, sticky="EW")
        add_person_button.grid(column=0, row=2, sticky="EW")
        return_to_main_menu.grid(column=0, row=3, sticky="W")

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=15)

    def add_new_person(self, person):
        person_string = str(person)
        if len(person_string) == 0:
            messagebox.showinfo(
                title="Oops!",
                message="Make sure you entered the information correctly."
            )
        else:
            database.add_person(person_string)
            messagebox.showinfo(
                title="Success!",
                message=f"{person_string} added."
            )


root = EventAttendanceTracker()
root.geometry("800x425")
root.resizable(False, False)

font.nametofont("TkDefaultFont").configure(size=15)

root.columnconfigure(0, weight=1)

database.create_tables()

root.mainloop()
