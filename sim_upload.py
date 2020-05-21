#gdrive upload script
import pytz
import tzlocal
import datetime
import time
import os
import sys
import schedule
import subprocess
from time import sleep
from picam_preset_1 import *

#sync_to_gdrive = True                      #True / False emediatly save on gdrive
#save_to_gdrive = False                      #True / False save on gdrive after stop_time
#interval = "2:00"
#processing_time = (1 + camera.shutter_speed / 1000000)          #Time of executing the script, camera.shutter_speed is in micro secconds

def unmount():
	os.system("fusermount -u gdrive")
def mount():
	os.system("rclone mount rpi-gdrive: gdrive")

x = datetime.datetime.utcnow()															#UTC time 
day_now= x.strftime("%w")																#day of the week 0-6
local_timezone = tzlocal.get_localzone()												#Time Zone 
moment_utc = x.replace(tzinfo=pytz.utc).astimezone(local_timezone) 						#UTC Time Zone
moment =(moment_utc.strftime("%X"))														#time now in hh:mm:ss
tine_now_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], moment.split(":"))))		#string time now in seconds
start_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], start_time.split(":"))))		#string time start now in seconds
stop_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], stop_time.split(":"))))		#string time stop now in seconds
interval_int = int(sum(x * int(t) for x, t in zip([60, 1], interval.split(":"))))		#string interval in seconds
sync = os.system("rclone --ignore-existing sync 'Pool' gdrive -P -vv")					#rclone sync every interval + 1 second
upload = os.system("rclone --checksum --ignore-existing sync 'Pool' gdrive -P -vv")		#rclone upload after tl job complete
schedule.every(interval_int - processing_time + 1).minutes.do(sync)

if not os.path.exists("gdrive/Test"):
	print("drive is not moutned")
	subprocess.call(unmount)
	sleep(1)
	subprocess.call(mount)
	print("gdrive is mounted")
	sleep(1)
else:
	print("gdrive is redy")
	sleep(2)
while True:
    if sync_to_gdrive == True and save_to_gdrive == False: 
		if day_now >= start_day and day_now <= stop_day:
			if tine_now_str >= start_str and tine_now_str <= stop_str + 2:
				schedule.run_pending()
	if sync_to_gdrive == False and save_to_gdrive == True:
		if day_now >= start_day and day_now <= stop_day:
			if tine_now_str < start_str and tine_now_str > stop_str:
				schedule.every(3).hour.do(upload)
	if sync_to_gdrive == save_to_gdrive:
		print("Not uploading!")
		time.sleep(5)







