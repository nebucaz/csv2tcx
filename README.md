# csv2tcx
Converting Ergometer Data from CSV into TXC format to import into Strava

I collected some ergometer data from my Kettler Racer 9 over a serial connection over Bluetooth and stored them into a csv-file with the followinf columns:
* Power
* Energy
* Speed
* Duration
* Distance

In order to be able to upload the training session into my strava account, the data has to be converted in the tcx-format porposed by Garmin. The python script takes the csv and creates the corresponding tcx file, wich can be uploaded to strava (and probably other Apps). Hovewer, only the time, distance, speed and calorie values of the csv are used to create the reesulting file.

## usage
Open the python script and change the name/path of the csv file to be converted (at the bottom). Also check the output filename/location at the top of the file.
