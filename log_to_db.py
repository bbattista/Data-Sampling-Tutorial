#!/usr/bin/python3

import json
import sqlite3

# SQLite DB Name
DB_Name =  "raw.db"

#===============================================================
# Database Manager Class

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class DatabaseManager():
    def __init__(self):
        self.conn = sqlite3.connect(DB_Name)
        self.conn.row_factory = dict_factory
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def add_del_update_devices(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        self.conn.commit()
        return

    def add_del_update_calibration(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        self.conn.commit()
        return

    def select_calibration(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        result = self.cur.fetchall()
        return result

    def add_del_update_config(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        self.conn.commit()
        return

    def select_config(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        result = self.cur.fetchall()
        return result

    def __del__(self):
        self.cur.close()
        self.conn.close()

#===============================================================
# Functions to Interact with Database

# Function to save data to DB Table
def Data_Handler(jsonData):

    #Parse Data
    json_Dict = json.loads(jsonData)
    dbObj = DatabaseManager()
    result = 0

    if json_Dict['_type'] == 'loadCal':
        # Read DB Calibration
        project = json_Dict['project']
        vessel = json_Dict['vessel']
        calibration = dbObj.select_calibration("SELECT project, vessel, length, width, height, cutterLength, cutterDraft, pinOffX, pinOffY, pinOffZ, gpsOffX, gpsOffY, gpsOffZ, hdgOffX, hdgOffY, hdgOffZ, flipAngleX, flipAngleY FROM calibration WHERE project=\"{project}\" and vessel=\"{vessel}\" ORDER BY datetime DESC limit 1".format(project=project, vessel=vessel))
        calibration = calibration[0]
        calibration['_type'] = 'importCal'
        result = calibration

    if json_Dict['_type'] == 'calibration':
        SensorID = json_Dict['tid']
        project = json_Dict['project']
        vessel = json_Dict['vessel']
        length = json_Dict['length']
        width = json_Dict['width']
        height = json_Dict['height']
        cutterLength = json_Dict['cutterLength']
        cutterDraft = json_Dict['cutterDraft']
        pinOffX = json_Dict['pinOffX']
        pinOffY = json_Dict['pinOffY']
        pinOffZ = json_Dict['pinOffZ']
        gpsOffX = json_Dict['gpsOffX']
        gpsOffY = json_Dict['gpsOffY']
        gpsOffZ = json_Dict['gpsOffZ']
        hdgOffX = json_Dict['hdgOffX']
        hdgOffY = json_Dict['hdgOffY']
        hdgOffZ = json_Dict['hdgOffZ']
        flipAngleX = json_Dict['flipAngleX']
        flipAngleY = json_Dict['flipAngleY']

        #Push into DB Table
        dbObj.add_del_update_calibration("insert into calibration (SensorID, project, vessel, length, width, height, cutterLength, cutterDraft, pinOffX, pinOffY, pinOffZ, gpsOffX, gpsOffY, gpsOffZ, hdgOffX, hdgOffY, hdgOffZ, flipAngleX, flipAngleY) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",[SensorID, project, vessel, length, width, height, cutterLength, cutterDraft, pinOffX, pinOffY, pinOffZ, gpsOffX, gpsOffY, gpsOffZ, hdgOffX, hdgOffY, hdgOffZ, flipAngleX, flipAngleY])
        print("Inserted Data into Calibration.")
        print("")

    if json_Dict['_type'] == 'loadConfig':
        # Read DB Calibration
        configuration = dbObj.select_config("SELECT company, project, vessel, projection, units, xteType FROM config ORDER BY datetime DESC limit 1")
        configuration = configuration[0]
        configuration['_type'] = 'importConfig'
        result = configuration

    if json_Dict['_type'] == 'configuration':
        SensorID = json_Dict['tid']
        company = json_Dict['company']
        project = json_Dict['project']
        vessel = json_Dict['vessel']
        projection = json_Dict['projection']
        units = json_Dict['units']
        xteType = json_Dict['xteType']

        #Push into DB Table
        dbObj.add_del_update_config("insert into config (SensorID, company, project, vessel, projection, units, xteType) values (?,?,?,?,?,?,?)",[SensorID, company, project, vessel, projection, units, xteType])
        print("Inserted Data into Config.")
        print("")

    if json_Dict['_type'] == 'location':
        SensorID = json_Dict['tid']
        tst = json_Dict['tst']
        lon = json_Dict['lon']
        lat = json_Dict['lat']
        #nmea = json_Dict['nmea']

        #Push into DB Table
        dbObj.add_del_update_devices("insert into devices (SensorID, tst, lon, lat, raw) values (?,?,?,?,?)",[SensorID, tst, lon, lat, jsonData])
        print("Inserted Data into Devices.")
        print("")

    del dbObj
    return result

#===============================================================
# Master Function to Select DB Funtion based on MQTT Topic

def device_Data_Handler(Topic, jsonData):
    result = Data_Handler(jsonData)
    return result
