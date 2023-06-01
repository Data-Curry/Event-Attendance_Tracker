import tkinter as tk
from tkinter import ttk


class ViewUpcomingEventsDisplayWindow(tk.Canvas):                          # This makes View Upcoming Events scrollable
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)  # removes the Canvas border

        self.display_frame = ttk.Frame(self)
        self.display_frame.columnconfigure(0, weight=1)                       # this frame takes up all available space

        self.scrollable_window = self.create_window((0, 0), window=self.display_frame, anchor="nw")

        def configure_scroll_region(event):
            self.configure(scrollregion=self.bbox("all"))

        def configure_window_size(event):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        self.display_frame.bind("<Configure>", configure_scroll_region)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        scrollbar.grid(column=1, row=1,  sticky="NS")

        self.configure(yscrollcommand=scrollbar.set)
        self.yview_moveto(1.0)

    def update_upcoming_events_widgets(self, upcoming_events):  # moved here from ViewUpcomingEvents class in app.py
        for event in upcoming_events:
            event_label = ttk.Label(
                self.display_frame,
                text=event,
                anchor="w",
                justify="left"
            )

            event_label.grid(sticky="NSEW")


class ViewEventsChronologicallyDisplayWindow(tk.Canvas):            # This makes View Events Chronologically scrollable
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)  # removes the Canvas border

        self.display_frame = ttk.Frame(self)
        self.display_frame.columnconfigure(0, weight=1)                       # this frame takes up all available space

        self.scrollable_window = self.create_window((0, 0), window=self.display_frame, anchor="nw")

        def configure_scroll_region(event):
            self.configure(scrollregion=self.bbox("all"))

        def configure_window_size(event):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        self.display_frame.bind("<Configure>", configure_scroll_region)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        scrollbar.grid(column=1, row=1, sticky="NS")

        self.configure(yscrollcommand=scrollbar.set)
        self.yview_moveto(1.0)

    def update_events_chronologically_widgets(self, events_chronologically):  # moved here from ViewEventsChronologically class in app.py
        for event in events_chronologically:
            event_label = ttk.Label(
                self.display_frame,
                text=event,
                anchor="w",
                justify="left"
            )

            event_label.grid(sticky="NSEW")


class ViewItemsByIDDisplayWindow(tk.Canvas):                             # This makes the ViewItemsByID class scrollable
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)  # removes the Canvas border

        self.display_frame = ttk.Frame(self)
        self.display_frame.columnconfigure(0, weight=1)                # this frame takes up all available space

        self.scrollable_window = self.create_window((0, 0), window=self.display_frame, anchor="nw")

        def configure_scroll_region(event):
            self.configure(scrollregion=self.bbox("all"))

        def configure_window_size(event):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        self.display_frame.bind("<Configure>", configure_scroll_region)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        scrollbar.grid(column=1, row=1, sticky="NS")

        self.configure(yscrollcommand=scrollbar.set)
        self.yview_moveto(1.0)

    def update_events_by_id_widgets(self, events_by_id):  # moved here from ViewEventsByID class in app.py
        for event in events_by_id:
            event_label = ttk.Label(
                self.display_frame,
                text=event,
                anchor="w",
                justify="left"
            )

            event_label.grid(sticky="NSEW")


class ViewAttendedEventsDisplayWindow(tk.Canvas):                          # this makes View Attended Events scrollable
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)  # removes the Canvas border

        self.display_frame = ttk.Frame(self)
        self.display_frame.columnconfigure(0, weight=1)                       # this frame takes up all available space

        self.scrollable_window = self.create_window((0, 0), window=self.display_frame, anchor="nw")

        def configure_scroll_region(event):
            self.configure(scrollregion=self.bbox("all"))

        def configure_window_size(event):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        self.display_frame.bind("<Configure>", configure_scroll_region)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        scrollbar.grid(column=1, row=2, sticky="NS")

        self.configure(yscrollcommand=scrollbar.set)
        self.yview_moveto(1.0)

    def update_attended_events_widgets(self, attended_events):  # moved here from UpdateAttendedEvents class in app.py
        for event in attended_events:
            event_label = ttk.Label(
                self.display_frame,
                text=event,
                anchor="w",
                justify="left"
            )

            event_label.grid(sticky="NSEW")


"""
# THIS IS THE BOILERPLATE WINDOW TO MAKE A SCROLLABLE WINDOW WITH A SCROLLBAR...

class DisplayWindow(tk.Canvas):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)    # removes the Canvas border

        self.display_frame = ttk.Frame(self)
        self.display_frame.columnconfigure(0, weight=1)                       # this frame takes up all available space

        self.scrollable_window = self.create_window((0, 0), window=self.display_frame, anchor="nw")  

        def configure_scroll_region(event):
            self.configure(scrollregion=self.bbox("all"))

        def configure_window_size(event):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        self.display_frame.bind("<Configure>", configure_scroll_region)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        scrollbar.grid(column=1, row=0, sticky="NS")

        self.configure(yscrollcommand=scrollbar.set)
        self.yview_moveto(1.0)


EXPLANATION...

    self.scrollable_window = self.create_window((0, 0), window=self.display_frame, anchor="nw")

This creates essentially an inner window inside the Canvas where components can be put.
The Canvas will not change in size.
Inside the Canvas is self.display_frame.  This will change size when components are added to it.
# pass in where the anchor point of the window is, (0, 0) is top left of canvas; 
what window to create; where the anchor point of the window is, northwest matches (0, 0)

    def configure_scroll_region(event):
        self.configure(scrollregion=self.bbox("all"))

This tells the Canvas how large the scroll region is.
When it is called, it says the scroll region is the bounding box of all elements inside the Canvas.
So, it tells the Canvas the amount of scrolling it can do is equal to the size of the display_frame.

    self.display_frame.bind("<Configure>", configure_scroll_region)

The configure_scroll_region method is bound to self.display_frame
Whenever a component grows, that's when the function bound to <Configure> gets called.
Whenever the Frame grows, configure_scroll_region gets called.

    scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
    scrollbar.grid(row=0, column=1, sticky="NS")

This places a scrollbar inside the same container as the Canvas so that they are side by side.
orient makes it vertical.  command is Canvas.yview, in this case self.yview...
...when you move the scrollbar, it changes the Y position of that Canvas relative to its inner window.

    self.configure(yscrollcommand=scrollbar.set)

yscrollcommand on the Canvas is what moves the scrollbar position, so that they will talk to each other.

    self.yview_moveto(1.0)

This moves the Canvas down to the bottom of the scrollable area,
so that the contents always start in the same place.

    def configure_window_size(event):
        self.itemconfig(self.scrollable_window, width=self.winfo_width())

This limits the width of the scrollable window to be at most the width of the canvas.
This avoids any scrolling on the x-axis.  Canvas allows scrolling on x and y axes by default.
This makes our displayed events constrained within the Canvas.
when self.itemconfig is called, it goes into the Canvas, finds an element with the id of self.scrollable_window,
and can change its properties, in this case changing the width.  
We're setting it to be equal to the winfo_width, which is the width of the Canvas.
To call this whenever the Canvas changes size...

    self.bind("<Configure>", configure_window_size)
"""