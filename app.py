#!/usr/bin/python
import sqlite3
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS


def connect_to_db():
    conn = sqlite3.connect('database.db')
    conn.execute("PRAGMA foreign_keys = 1")
    return conn


def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE meters (
                meter_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                label VARCHAR(20) NOT NULL
            );
        ''')
        conn.execute('''
            CREATE TABLE meter_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                meter_id INTEGER NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                value INTEGER NOT NULL,
                FOREIGN KEY (meter_id) REFERENCES meters (meter_id)
            );
        ''')

        conn.commit()
    except:
        conn.rollback()
    finally:
        conn.close()


def insert_meter(label):
    try:
        conn = connect_to_db()
        conn.execute("INSERT INTO meters (label) VALUES (?)", (label,))
        conn.commit()
    except:
        conn.rollback()
    finally:
        conn.close()

def insert_meter_data(meter_id, timestamp, value):
    try:
        conn = connect_to_db()
        conn.execute("INSERT INTO meter_data (meter_id, timestamp, value) VALUES (?, ?, ?)", (meter_id, timestamp, value))
        conn.commit()
    except:
        conn.rollback()
    finally:
        conn.close()

create_db_table()

insert_meter("meter1")
insert_meter("meter2")
insert_meter("meter3")
insert_meter("meter4")
insert_meter("meter5")

insert_meter_data(5, datetime.datetime.now(), 4)
insert_meter_data(2, datetime.datetime.now(), 3)
insert_meter_data(4, datetime.datetime.now(), 11)
insert_meter_data(3, datetime.datetime.now(), 5)
insert_meter_data(1, datetime.datetime.now(), 9)

insert_meter_data(2, datetime.datetime.now(), 10)
insert_meter_data(1, datetime.datetime.now(), 20)
insert_meter_data(4, datetime.datetime.now(), 12)
insert_meter_data(5, datetime.datetime.now(), 3)
insert_meter_data(3, datetime.datetime.now(), 8)

insert_meter_data(1, datetime.datetime.now(), 3)
insert_meter_data(5, datetime.datetime.now(), 16)
insert_meter_data(2, datetime.datetime.now(), 2)
insert_meter_data(3, datetime.datetime.now(), 3)
insert_meter_data(4, datetime.datetime.now(), 16)

insert_meter_data(5, datetime.datetime.now(), 15)
insert_meter_data(1, datetime.datetime.now(), 6)
insert_meter_data(3, datetime.datetime.now(), 7)
insert_meter_data(2, datetime.datetime.now(), 8)
insert_meter_data(4, datetime.datetime.now(), 17)

insert_meter_data(2, datetime.datetime.now(), 14)
insert_meter_data(4, datetime.datetime.now(), 10)
insert_meter_data(1, datetime.datetime.now(), 17)
insert_meter_data(5, datetime.datetime.now(), 19)
insert_meter_data(3, datetime.datetime.now(), 5)


def get_meters():
    meters = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT label, timestamp, value FROM meters, meter_data where meters.meter_id = meter_data.meter_id")
        rows = cur.fetchall()

        for i in rows:
            meters[i["label"]] = []
        for i in rows:
            details = {}
            details["timestamp"] = i["timestamp"]
            details["value"] = i["value"]
            meters[i["label"]].append(details)
    except:
        conn.rollback()
    finally:
        conn.close()

    return meters

def get_meter_by_id(meter_id):
    meter_data_details = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM meter_data WHERE meter_id = ? ORDER BY timestamp ASC", meter_id)
        rows = cur.fetchall()

        for i in rows:
            meter_data = {}
            meter_data["id"] = i["id"]
            meter_data["meter_id"] = i["meter_id"]
            meter_data["timestamp"] = i["timestamp"]
            meter_data["value"] = i["value"]
            meter_data_details.append(meter_data)
    except:
        conn.rollback()
    finally:
        conn.close()

    return meter_data_details

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/meters', methods=['GET'])
def api_get_meters():
    return jsonify(get_meters())

@app.route('/meters/<meter_id>', methods=['GET'])
def api_get_meter_by_id(meter_id):
    return jsonify(get_meter_by_id(meter_id))

if __name__ == "__main__":
    app.run()
