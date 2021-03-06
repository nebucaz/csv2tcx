# csv2tcx
Converting ergometer data from CSV into TXC format to import into Strava

I collected some ergometer data from my Kettler Racer 9 over a serial connection over Bluetooth and stored them into a csv-file with the following columns:
* Power
* Energy
* Speed
* Duration
* Distance

In order to be able to upload the training session into my strava account, the data has to be converted in the tcx-format porposed by Garmin [XSD](https://www8.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd). The python script takes the csv and creates the corresponding tcx file, wich can be uploaded to strava (and probably other apps). Hovewer, only the time, distance, speed and calorie values of the csv are used to create the resulting file.

## Usage
Open the python script and change the name/path of the csv file to be converted (at the bottom). Also check the output filename/location at the top of the file.

## Notice
* This script was written to convert the values of a Kettler Racer 9. Due to limitations on the display, the *duration*  overflows at 5999 which has been compensated in the script. 
* The script assumes that the date time of the training session is encoded in the filename and can be extracted to create the id of the tcx-file (which is mandatory)
