# event, event_date, attended

CREATE_EVENTS_TABLE = """CREATE TABLE IS NOT EXISTS events (
    event TEXT,
    event_timestamp REAL,
    attended INTEGER
);"""

INSERT_EVENT = "INSERT INTO events (event, event_timestamp, attended) VALUES (?, ?, 0);"
SELECT_ALL_EVENTS = "SELECT * FROM events;"
SELECT_UPCOMING_EVENTS = "SELECT * FROM events WHERE event_timestamp > ?;"
SELECT_ATTENDED_EVENTS = "SELECT * FROM events WHERE attended = 1;"
