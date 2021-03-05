from datetime import datetime, timedelta
import pprint
import time
from influxdb import InfluxDBClient
from copy import deepcopy
import pandas as pd

host = 'ec2-54-146-80-82.compute-1.amazonaws.com'
port = 8086
user = 'root'
passwd = 'root'
dbName = 'Covid19'

# Connect to InfluxDB
def connect_InfluxDB(db, host='localhost', port=8086, user='root', passwd='root'):
    # Create an object include information for connect to the InfluxDB
    client = InfluxDBClient(host, port, user, passwd, db)

    try:
        # Try to Create database
        client.create_database(db)

        # If you can create database or have a database
        # there is no problem connecting to the InfluxDB
        print('Connection Successful')
        print('=======================')
        print('     Connection Info')
        print('=======================')
        print('host :', host)
        print('port :', port)
        print('username :', user)
        print('database :', db)
    except:
        # Generate error if you can't create database (can't connect to ifdb)
        print('Connection Failed')
        pass

    return client

# 보건복지부_코로나19 감염_현황
def save_Covid19_KR(ifdb):
    tablename = 'Covid19_KR'

    # Read csv data
    data = pd.read_csv('data/Covid19_KR.csv')
    columns = data.columns.tolist()
    fields = columns[1:]

    # save points in the json_body
    json_body = []
    point = {
        "measurement": tablename,
        "tags": {
            "nationNm": "한국",
            "nationNmEn" : "South Korea"
        },
        "fields": {
            # Initialize data to zero
            "Confirmed" : 0, 
            "Deaths" : 0,
            "Recovered" : 0,
            "Tested" : 0,
            "Testing" : 0, 
            "Negative" : 0
        },
        "time": None,
    }

    for _, row in data.iterrows():
        # InfluxDB is based on UTC
        # so it should be timed with KCT
        time = row['time']
        dt = datetime(int(time[0:4]), int(time[4:6]), int(time[6:8]), int(time[9:11]), int(time[12:14]), int(time[15:17]))
        
        np = deepcopy(point)
        np['time'] = dt
        for idx in range(1, len(row)):
            np['fields'][fields[idx-1]] = row[fields[idx-1]]
        
        json_body.append(np)

    # Write the data for 10 seconds on the influxDB at once
    ifdb.write_points(json_body)
    
    # result = ifdb.query('select * from %s' % tablename)
    # pprint.pprint(result.raw)

# 보건복지부_코로나19 시·도발생_현황
def save_Covid19_KR_Sido(ifdb):
    tablename = 'Covid19_KR_Sido'

    # Read csv data
    data = pd.read_csv('data/Covid19_KR_Sido.csv')
    columns = data.columns.tolist()
    fields = columns[1:]

    # save points in the json_body
    json_body = []
    point = {
        "measurement": tablename,
        "tags": {
            "City": 0
        },
        "fields": {
            # Initialize data to zero
            "Confirmed" : 0, 
            "Death" : 0,
            "Recovered" : 0,
            "Incidence" : 0
        },
        "time": None,
    }

    for _, row in data.iterrows():
        # InfluxDB is based on UTC
        # so it should be timed with KCT
        time = row['time']
        dt = datetime(int(time[0:4]), int(time[4:6]), int(time[6:8]), int(time[9:11]), int(time[12:14]), int(time[15:17]))
        
        np = deepcopy(point)
        np['time'] = dt
        np['tags']['City'] = row['City']
        for idx in range(2, len(row)):
            np['fields'][fields[idx-1]] = row[fields[idx-1]]
        
        json_body.append(np)

    # Write the data for 10 seconds on the influxDB at once
    ifdb.write_points(json_body)
    
    # result = ifdb.query('select * from %s' % tablename)
    # pprint.pprint(result.raw)

# 보건복지부_코로나19해외발생_현황
def save_Covid19_GB(ifdb):
    tablename = 'Covid19_GB'

    # Read csv data
    data = pd.read_csv('data/Covid19_GB.csv')
    columns = data.columns.tolist()
    fields = columns[3:]
    
    # save points in the json_body
    json_body = []
    point = {
        "measurement": tablename,
        "tags": {
            "nationNm": 0,
            "nationNmEn" : 0
        },
        "fields": {
            # Initialize data to zero
            "natDefCnt" : 0, 
            "natDeathCnt" : 0,
            "natDeathRate" : 0
        },
        "time": None,
    }

    for _, row in data.iterrows():
        # InfluxDB is based on UTC
        # so it should be timed with KCT
        time = row['time']
        dt = datetime(int(time[0:4]), int(time[4:6]), int(time[6:8]), int(time[9:11]), int(time[12:14]), int(time[15:17]))
        
        np = deepcopy(point)
        np['time'] = dt
        np['tags']['nationNm'] = row['nationNm']
        np['tags']['nationNmEn'] = row['nationNmEn']
        for idx in range(3, len(row)):
            np['fields'][fields[idx-3]] = row[fields[idx-3]]
        json_body.append(np)
        
    # Write the data for 10 seconds on the influxDB at once
    ifdb.write_points(json_body)

    # result = ifdb.query('select * from %s' % tablename)
    # pprint.pprint(result.raw)

# 보건복지부_코로나19 연령별·성별감염_현황
def save_Covid19_KR_GenAge(ifdb):
    tablename = 'Covid19_KR_GenAge'

    # Read csv data
    data = pd.read_csv('data/Covid19_KR_GenAge.csv')
    columns = data.columns.tolist()
    fields = columns[1:]

    # save points in the json_body
    json_body = []
    point = {
        "measurement": tablename,
        "tags": {
            "gubun": 0
        },
        "fields": {
            # Initialize data to zero
            "confCase" : 0, 
            "confCaseRate" : 0,
            "death" : 0, 
            "deathRate" : 0,
            "criticalRate" : 0
        },
        "time": None,
    }

    for _, row in data.iterrows():
        # InfluxDB is based on UTC
        # so it should be timed with KCT
        time = row['time']
        dt = datetime(int(time[0:4]), int(time[4:6]), int(time[6:8]), int(time[9:11]), int(time[12:14]), int(time[15:17]))
        
        np = deepcopy(point)
        np['time'] = dt
        np['tags']['gubun'] = row['gubun']
        for idx in range(2, len(row)):
            np['fields'][fields[idx-1]] = row[fields[idx-1]]
        
        json_body.append(np)

    # Write the data for 10 seconds on the influxDB at once
    ifdb.write_points(json_body)
    
    # result = ifdb.query('select * from %s' % tablename)
    # pprint.pprint(result.raw)

if __name__ == '__main__':

    # Connect to InfluxDB
    mydb = connect_InfluxDB(db=dbName, host=host, port=port, user=user, passwd=passwd)

    # Write data to mydb
    save_Covid19_KR(mydb)           # 보건복지부_코로나19 감염_현황
    save_Covid19_KR_Sido(mydb)      # 보건복지부_코로나19 시·도발생_현황
    save_Covid19_GB(mydb)           # 보건복지부_코로나19해외발생_현황
    save_Covid19_KR_GenAge(mydb)    # 보건복지부_코로나19 연령별·성별감염_현황