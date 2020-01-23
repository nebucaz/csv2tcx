#
# Schema: https://www8.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd
#
# © 2020 nebucaz

import csv
import re
import datetime
import pytz
from pytz import timezone
import xml.etree.ElementTree as ET

def convert(filename):
    # 0=Power,1=Energy,2=Speed,3=Duration,4=Distance,5=rpm,6=bpm,7=Requested Power
    # Kettler duration overflows @ 5999s

    overflow = 0
    totalTime = 0
    totalDistance = 0
    totalEnergy = 0
    maximumSpeed = 0

    m = re.match('([a-zA-z0-9\_\-]+)\.csv', filename)
    sessionName = m.group(1)
    xmlFilename = sessionName + ".tcx"
    print(sessionName)

    # get ID from filename
    cet = timezone("CET")
    m = re.match('kracer9_(\d+)\-(\d+)\-(\d+)_(\d{2})(\d{2})\.csv', filename)
    startTime = datetime.datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)),0,0,tzinfo=cet)

    root = ET.Element("TrainingCenterDatabase", xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2")
    tree = ET.ElementTree(root)

    activities = ET.Element("Activities")
    activity = ET.Element("Activity", Sport="Biking")

    ET.SubElement(activity, "Id").text = startTime.isoformat()
    lap = ET.SubElement(activity, "Lap", StartTime=startTime.isoformat())
    ET.SubElement(lap,"TotalTimeSeconds").text='0.0'
    ET.SubElement(lap,"DistanceMeters").text='0.0'
    ET.SubElement(lap,"MaximumSpeed").text='0.0'
    ET.SubElement(lap,"Calories").text='0'
    ET.SubElement(lap,"Intensity").text='Active'
    ET.SubElement(lap,"TriggerMethod").text='Manual'

    track = ET.Element("Track")

    with open('data/' + filename, 'rb') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        rows = list(reader)

        for row in rows:
            if overflow:
                row['Duration'] = int(row['Duration']) + overflow * 6000

            if int(row['Duration']) == 5999:
                overflow += 1

            # skip 0 rows
            if int(row['Energy']) == 0 and int(row['Distance']) == 0:
                continue

            # skip end/pause
            if int(row['Power']) < 7 and int(row['rpm']) == 0:
                continue

            totalTime = max(totalTime, int(row['Duration']))
            totalDistance = max(totalDistance, int(row['Distance']))
            totalEnergy = max(totalEnergy, int(row['Energy']))
            maximumSpeed = max(maximumSpeed, int(row['Speed']))

            trackpoint = ET.SubElement(track,"Trackpoint")
            time = startTime + datetime.timedelta(seconds=int(row['Duration']))
            ET.SubElement(trackpoint,"Time").text = time.isoformat()
            ET.SubElement(trackpoint,"DistanceMeters").text = str(float(int(row['Distance']) * 100))


    lap.find('TotalTimeSeconds').text = str(float(totalTime))
    lap.find('DistanceMeters').text = str(float(totalDistance * 100))
    lap.find('MaximumSpeed').text = str(float(maximumSpeed)/10)
    lap.find('Calories').text = str(int(totalEnergy))

    lap.append(track)
    activities.append(activity)
    root.append(activities)

    tree.write(xmlFilename, encoding='utf-8', xml_declaration=True)


convert('kracer9_2020-01-12_1442.csv')
