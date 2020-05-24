#gdrive upload script under construction
#replace word gdrive with cloud
import pytz
import tzlocal
import datetime
import time
import os
import sys
import socket
import subprocess
from time import sleep

from MAIN STARTING SCRIPT import Preset #working 
from Preset import start_day, stop_day, sync_to_cloud, save_to_cloud, stop_time, start_time
#from picam_reset_1 import start_day, stop_day, sync_to_cloud, save_to_cloud, stop_time, start_time 

#########  -  uncomment for manually run  -  #################
#start_day = 0#only import from preset
#stop_day = 6 #only import from preset
#sync_to_cloud = True/False #only import from preset
#save_to_cloud = True/False #only import from preset
#stop_time = "8:00" #only import from preset
#start_time = "18:00" #only import from preset

#############  -  Custom time  -  ###########################
time_upload = "20:00"
#############################################################

x = datetime.datetime.utcnow()															#UTC time 
local_timezone = tzlocal.get_localzone()							#Time Zone 
moment_utc = x.replace(tzinfo=pytz.utc).astimezone(local_timezone) 				#UTC Time Zone
moment =(moment_utc.strftime("%X"))								#time now in hh:mm:ss
start_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], start_time.split(":"))))		#string time start now in seconds
stop_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], stop_time.split(":"))))		#string time stop now in seconds
tine_now_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], moment.split(":"))))		#string time now in seconds
day_now= x.strftime("%w")																#day of the week 0-6

Schedule_day = False
Raspberry_online = True
cloud_online = False
error_upload = True

#################will be defined in picam_reset_1
def sync():
	os.system("rclone --ignore-existing sync 'Pool' gdrive -P -vv")
	sleep(300)
	
def upload():
	os.system("rclone --checksum --ignore-existing sync 'Pool' gdrive -P -vv")
	
def restart_cloud():############################# subprocces and check for other procces and kill it
	os.system("fusermount -u gdrive")
	sleep(5)
	os.system("rclone mount rpi-gdrive: gdrive")
	sleep(2)	
#########################################################################
	
def raspberry_online():
	try:
		socket.create_connection(('Google.com', 80))
		global Raspberry_online ###############################
		Raspberry_online = True
		return Raspberry_online
	except OSError:
		Raspberry_online = False
		return Raspberry_online

def cloud_check():
	if os.path.isdir("gdrive/Test") == True: #call variable directory from preset
		cloud_online = True
		return cloud_online
	else: #if error
		gdrive_online = False
		return gdrive_online
		print("Not mounted")
		
def	upload_check():
	if os.system(): #find a way to check the differences
		error_upload = True 
		return error_upload
	else:
		error_upload = False
		return error_upload
		
def day_check():
	for list_day in list(range(start_day, stop_day + 1)):
		if list_day == day_now:
			global Schedule_day
			Schedule_day = True
			return Schedule_day
		else:
			global Schedule_day
			Schedule_day = False
			return Schedule_day
		
#############################  - Main loop  -  ##########################
new_day = True
upload_complete = False
while new_day == True:
	raspberry_online()
	restart_cloud()
	upload()
	day_check()
	if Schedule_day == True
		raspberry_online()
		if Raspberry_online == True:
			new_day = False
			return new_day
			cloud_check()
			if sync_to_cloud == True and save_to_cloud == False and new_day == False and Raspberry_online == True:
				if cloud_online == True and new_day == False and Raspberry_online == True:
					if time_now <= stop_time and new_day == False and Raspberry_online == True:  #working time is not over 
						sync() #no  --checksum, faster upload, if is done before stop time just wait 2 min and resart
						sleep(60)
						if time_now > stop_time and new_day == False and Raspberry_online == True: 	 #working time is over no new picture will be taken
							cloud_check()
							if cloud_online == True and new_day == False and Raspberry_online == True:
								upload_check()	#vrati error, to je sigurno ako nije završio s uploadom 
								if error_upload == True and new_day == False and Raspberry_online == True:
									seelp(2)
									print("Repeating upload!")
									upload()
									upload_check() #if is ok - set error_upload to False
									cloud_check()
									raspberry_online()
								elif new_day == False and Raspberry_online == True:
									seelp(2)
									print("Upload exsecuted succesfuly, no need to repeat!")
									new_day == True 
									return new_day
									cloud_check()
									raspberry_online()
								pass	#form frst time her go back to main lool if  
							elif cloud_online == False and Raspberry_online == True:
								restart_cloud()
								sleep(5)
							pass
						pass
					pass
				elif cloud_online == False and Raspberry_online == True:
					restart_cloud()
					sleep(5)
			if sync_to_cloud == False and save_to_cloud == True and new_day == False and Raspberry_online == True:
				if cloud_online == True and new_day == False and Raspberry_online == True:
					upload_check()
					if time_upload > stop_time or time_upload < start_time and error_upload == True and Raspberry_online == True:
						upload() #moguće da ostane bez interneta dok traje
						upload_check()
						raspberry_online()
						if error_upload == True and cloud_online == True and Raspberry_online == True and new_day == False:
							print("Uploading again!")
							upload()
							upload_check()
						elif error_upload == False:
							print("Succes upload, new upload schedule tomorrow!")
							new_day == True 
							return new_day
							sleep(120)
						elif cloud_online == False:
							restart_drive()
							upload_check()
							sleep(120)
						pass
					pass
				pass
			pass
		pass	
	else:
		raspberry_online() # raspberry nije online
		sleep(300)
else:
	chack_day()
