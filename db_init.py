#!/usr/bin/python
import sqlite3

# SQLite DB Name
DB_Name =  "devices.db"

# SQLite DB Table Schema
deviceTableSchema="""
DROP TABLE IF EXISTS devices ;
CREATE TABLE devices (
  id integer primary key autoincrement,
  SensorID text,
  tst,
  datetime text,
  lon,
  lat,
  raw
);

CREATE TRIGGER IF NOT EXISTS format_datetime AFTER INSERT ON devices
  BEGIN
    UPDATE devices SET datetime = strftime('%Y-%m-%d %H:%M:%S', DATETIME(NEW.tst, 'unixepoch', 'localtime')) WHERE id=NEW.id;
  END;
"""

# SQLite DB Table Schema
configTableSchema="""
DROP TABLE IF EXISTS config ;
CREATE TABLE config (
  id integer primary key autoincrement,
  SensorID text,
  datetime text,
  company text,
  project text,
  vessel text,
  projection text,
  units text,
  xteType text
);

CREATE TRIGGER IF NOT EXISTS config_datetime AFTER INSERT ON config
  BEGIN
    UPDATE config SET datetime = datetime('now','localtime') WHERE id=NEW.id;
  END;
"""

# SQLite DB Table Schema
calibrateTableSchema="""
DROP TABLE IF EXISTS calibration ;
CREATE TABLE calibration (
  id integer primary key autoincrement,
  SensorID text,
  datetime text,
  project text,
  vessel text,
  length,
  width,
  height,
  cutterLength,
  cutterDraft,
  pinOffX,
  pinOffY,
  pinOffZ,
  gpsOffX,
  gpsOffY,
  gpsOffZ,
  hdgOffX,
  hdgOffY,
  hdgOffZ,
  flipAngleX,
  flipAngleY
);

CREATE TRIGGER IF NOT EXISTS cal_datetime AFTER INSERT ON calibration
  BEGIN
    UPDATE calibration SET datetime = datetime('now','localtime') WHERE id=NEW.id;
  END;
"""

#Connect or Create DB File
conn = sqlite3.connect(DB_Name)
curs = conn.cursor()

#Create Tables
sqlite3.complete_statement(deviceTableSchema)
curs.executescript(deviceTableSchema)

sqlite3.complete_statement(configTableSchema)
curs.executescript(configTableSchema)

sqlite3.complete_statement(calibrateTableSchema)
curs.executescript(calibrateTableSchema)

#Close DB
curs.close()
conn.close()
