import datetime
import sqlite3


CREATE_EVENTS_TABLE = """CREATE TABLE IF NOT EXISTS events (
    event TEXT,
    event_timestamp REAL,
    attended INTEGER
);"""

INSERT_EVENT = "INSERT INTO events (event, event_timestamp, attended) VALUES (?, ?, 0);"
SELECT_ALL_EVENTS = "SELECT * FROM events;"
SELECT_UPCOMING_EVENTS = "SELECT * FROM events WHERE event_timestamp > ?;"
SELECT_ATTENDED_EVENTS = "SELECT * FROM events WHERE attended = 1;"
SET_EVENT_ATTENDED = "UPDATE events SET attended = 1 WHERE event = ?;"


connection = sqlite3.connect("data.db")


def create_tables():
    with connection:
        connection.execute(CREATE_EVENTS_TABLE)


def add_event(event, event_timestamp):
    with connection:
        connection.execute(INSERT_EVENT, (event, event_timestamp))


def get_events(upcoming=False):
    with connection:
        cursor = connection.cursor()
        if upcoming:
            today_timestamp = datetime.datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_EVENTS, (today_timestamp,))
        else:
            cursor.execute(SELECT_ALL_EVENTS)
        return cursor.fetchall()


def attend_event(event):
    with connection:
        connection.execute(SET_EVENT_ATTENDED, (event,))


def get_attended_events():
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_ATTENDED_EVENTS)
        return cursor.fetchall()
