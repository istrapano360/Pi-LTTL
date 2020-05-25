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

#TO BE DONE import from the main file "Start_timelapse.py" a variable that define witch variables will be imported
#from specified preset 
from Start_timelapse import Preset  #Preset = Picam-preset_1
from Preset import start_day, stop_day, sync_to_cloud, save_to_cloud, stop_time, start_time


#########  -  uncomment for manually run  -  #################
#from picam_preset_1 import start_day, stop_day, sync_to_cloud, save_to_cloud, stop_time, start_time 
#start_day = 0#only import from preset
#stop_day = 6 #only import from preset
#sync_to_cloud = True/False #only import from preset
#save_to_cloud = True/False #only import from preset
#stop_time = "8:00" #only import from preset
#start_time = "18:00" #only import from preset

#############  -  Custom time  -  only for 2. option ########
time_upload = "20:00"		#manually
#time_upload => stop_time	#auto
#############################################################

x = datetime.datetime.utcnow()															#UTC time 
local_timezone = tzlocal.get_localzone()							#Time Zone 
moment_utc = x.replace(tzinfo=pytz.utc).astimezone(local_timezone) 				#UTC Time Zone
moment =(moment_utc.strftime("%X"))								#time now in hh:mm:ss
start_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], start_time.split(":"))))		#string time start now in seconds
stop_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], stop_time.split(":"))))		#string time stop now in seconds
tine_now_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], moment.split(":"))))		#string time now in seconds
day_now= moment_utc.strftime("%w")														#day of the week 0-6 in the time zone

Schedule_day = False
Raspberry_online = True
cloud_online = False
error_upload = True

################# will be defined in picam_reset_1  ######################
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
#check if Raspberry is on internet
def raspberry_online():
	global Raspberry_online ############################### need to check this function
	try:
		socket.create_connection(('Google.com', 80))
		Raspberry_online = True
		return Raspberry_online
	except OSError:
		Raspberry_online = False
		return Raspberry_online
	
#check if cloud is on mounted in a folder
def cloud_check():
	global cloud_online
	if os.path.isdir("gdrive/Test") == True: #TO DO: call variable directory from preset, in the preset will be defined the dir
		cloud_online = True
		return cloud_online
	else: #if error
		cloud_online = False
		return cloud_online
		print("Not mounted")
		
#TO BE DONE rclone does have upload --checksum --dry-run, only don't know yet how to return a value  ##################
def upload_check():
	global error_upload
	if os.system(): #find a way to check the differences
		error_upload = True 
		return error_upload
	else:# all good 
		error_upload = False
		return error_upload
	
#returns today in timestamp format 
def today():
	return day_now

#return true or false if is a working day 
def day_check():
	global Schedule_day
	today()
	if start_day <= stop_day:
		for list_day in list(range(start_day, stop_day + 1)):
			if list_day == day_now:
				Schedule_day = True
				return Schedule_day
			else:
				Schedule_day = False
				return Schedule_day
	elif start_day > stop_day:
		x1 = list(range(start_day, 7))
            	x2 = list(range(0, stop_day + 1))
            	day_now =x1 + x2
		for list_day in list(range(start_day, stop_day - 1)):
			if list_day == day_now:
				Schedule_day = True
				return Schedule_day
			else:
				Schedule_day = False
				return Schedule_day


#############################  - Main loop  -  ##########################
new_day = True
upload_complete = False
Schedule_day = False
day_check()
while new_day == True:
	raspberry_online()
	restart_cloud()
	upload()
	day_check()
	if Schedule_day == True:
		day_check()
		raspberry_online()
		cloud_check()
		new_day = False
		if Raspberry_online == True and new_day == False:
			# Sinc on cloud option right after taking a picture
			if sync_to_cloud == True and save_to_cloud == False and new_day == False and Raspberry_online == True:
				if cloud_online == True and new_day == False and Raspberry_online == True:
					if time_now <= stop_time and new_day == False and Raspberry_online == True:  #working time is not over 
						sync() #no  --checksum, faster upload, if is done before stop time just wait 2 min and resart
						sleep(60)
						if time_now > stop_time and new_day == False and Raspberry_online == True: 	 #working time is over no new picture will be taken
							cloud_check()
							if cloud_online == True and new_day == False and Raspberry_online == True:
								upload_check()	
								if error_upload == True and new_day == False and Raspberry_online == True:
									seelp(2)
									print("Repeating upload!")
									upload()
									upload_check() #if is ok - set error_upload to False
									raspberry_online()
									cloud_check()
								elif new_day == False and Raspberry_online == True:
									seelp(2)
									print("Upload exsecuted succesfuly, no need to repeat!")
									new_day == True 
									cloud_check()
									raspberry_online()
								return new_day
								pass	#form frst time her go back to main lool if   Schedule_day == True:
							elif cloud_online == False and Raspberry_online == True:
								restart_cloud()
								sleep(5)
							pass
						pass
					pass
				elif cloud_online == False and Raspberry_online == True:
					restart_cloud()
					sleep(5)
				pass
			# Upload to cloud after working day is over and stops before time lapse starts
			if sync_to_cloud == False and save_to_cloud == True and new_day == False and Raspberry_online == True:
				if cloud_online == True and new_day == False and Raspberry_online == True:
					upload_check()
					if time_upload > stop_time or time_upload < start_time and error_upload == True and Raspberry_online == True:
						upload() #it's possible disconnected 
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
		elif Raspberry_online == False:
			raspberry_online() # raspberry not online
			sleep(300)
		pass
		#ther is a problem, if a time lapse ends in 23:50 and the next day is a non working day 
		#the upload will have only 10 minutes to run and it will not be completed, the upload will 
		#coninue next working day again after 23:50, but will have two days of files to upload .
		#to overcome this probelm the next stsment will overwrite the Shedule_day to make it work one more day
		#this is for fail safe safety
		elif Schedule_day == False and stop_time > 82800: #23:00
		print("Not a working day, if fail will continue next working day")
		if error_upload == True and cloud_online == True and Raspberry_online == True: 
			print("Uploading in a non working day...")
			upload()
			upload_check()
			raspberry_online()
		elif error_upload == False:
			print("Succes upload, new upload schedule next scheduled day!")
		pass
	else:
		print("Upload will continue next scheduled day")
		day_check()
