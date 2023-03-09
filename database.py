import datetime
import sqlite3


CREATE_EVENTS_TABLE = """CREATE TABLE IF NOT EXISTS events (
    _id INTEGER PRIMARY KEY,
    event TEXT,
    event_timestamp REAL
);"""
CREATE_ATTENDED_TABLE = """CREATE TABLE IF NOT EXISTS attended (
    person_name TEXT,
    event_id INTEGER,
    FOREIGN KEY(person_name) REFERENCES people(person_name),
    FOREIGN KEY(event_id) REFERENCES events(_id)
);"""
CREATE_PEOPLE_TABLE = """CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_name TEXT
);"""

INSERT_PERSON = "INSERT INTO people (person_name) VALUES (?);"
SELECT_PERSON = "SELECT * FROM people WHERE person_name = ?;"
INSERT_EVENT = "INSERT INTO events (event, event_timestamp) VALUES (?, ?);"
SELECT_EVENT = "SELECT _id FROM events WHERE _id = ?;"
SELECT_ALL_EVENTS = "SELECT * FROM events;"
SELECT_ALL_EVENTS_CHRONOLOGICALLY = "SELECT * FROM events ORDER BY event_timestamp ASC;"
SELECT_UPCOMING_EVENTS = "SELECT * FROM events WHERE event_timestamp > ? ORDER BY event_timestamp ASC;"
SELECT_ATTENDED_EVENTS = """SELECT _id, event, event_timestamp
    FROM events
    JOIN attended ON _id = attended.event_id
    JOIN people ON people.person_name = attended.person_name
    WHERE people.person_name = ?
    ORDER BY event_timestamp ASC;"""
INSERT_ATTENDED_EVENT = "INSERT INTO attended (person_name, event_id) VALUES (?, ?)"
SET_EVENT_ATTENDED = "UPDATE events SET attended = 1 WHERE event = ?;"
DELETE_EVENT = "DELETE FROM events WHERE event = ?;"


connection = sqlite3.connect("data.db")


def create_tables():
    with connection:
        connection.execute(CREATE_EVENTS_TABLE)
        connection.execute(CREATE_PEOPLE_TABLE)
        connection.execute(CREATE_ATTENDED_TABLE)


def add_person(person_name):
    with connection:
        connection.execute(INSERT_PERSON, (person_name,))


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


def get_events_chronologically():
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_ALL_EVENTS_CHRONOLOGICALLY)
        return cursor.fetchall()


def attend_event(person_name, event_id):
    with connection:
        connection.execute(INSERT_ATTENDED_EVENT, (person_name, event_id))


def get_attended_events(person):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_ATTENDED_EVENTS, (person,))
        return cursor.fetchall()


def get_person(person):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_PERSON, (person,))
        return cursor.fetchall()


def get_event(event_id):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_EVENT, (event_id,))
        return cursor.fetchall()
