#!/usr/bin/env python3
import pytz
import tzlocal
import datetime
import time
import os
import sys
import picamera
from time import sleep
from picamera import PiCamera
from picam_preset_1.3 import* # will import: pool, take_picture, camera_settings, start_day, stop_day, start_time, stop_time, interval 
#To DO dynamic import 
#TL = "picam_preset_13"
#import importlib
#module1 = importlib.import_module(TL)
 
#IMPORTANT camera script name: picam_preset_"X".py
#1 - 30 sec day, for automatic upload
#2 -  2 min ISO 100, WB auto, RAW
#3 -  5 min ISO 100, WB auto, bri 50, con -10

x = datetime.datetime.utcnow()																#UTC time
Local_timezone = tzlocal.get_localzone()													#Time Zone
Moment_utc = x.replace(tzinfo=pytz.utc).astimezone(Local_timezone)							#UTC Time Zone
Day_now = int(Moment_utc.strftime("%w"))													#day of the week 0-6
Moment =(Moment_utc.strftime("%X"))															#time now in hh:mm:ss
Time_now_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], Moment.split(":"))))			#string time now in seconds
Start_time_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], Start_time.split(":"))))	#string time start now in seconds
Stop_time_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], Stop_time.split(":"))))		#string time stop now in seconds
Interval_int = int(sum(x * int(t) for x, t in zip([60, 1], Interval.split(":"))))			#string interval in seconds
Processing_time = int(1 + camera.shutter_speed / 1000000)									#Time of executing the script, camera.shutter_speed is in micro secconds
TL_interval = Interval_int - Processing_time												#Interval
Wait_time = Time_now_str

def tl_script():
	global Wait_time, TL_interval, Interval
	if Time_now_str == Wait_time:
		take_picture()
		Wait_time = int(Time_now_str + TL_interval + 1)
		print("take a picture")
		print(Wait_time)
		print(Time_now_str)
	return Time_now_str

#--------------------------------- Day -------------------------------------------------
def today():											#F Return today day int
	global x, Local_timezone, Moment_utc, Day_now
	x = datetime.datetime.utcnow()										#UTC time
	Local_timezone = tzlocal.get_localzone()							#Time Zone
	Moment_utc = x.replace(tzinfo=pytz.utc).astimezone(Local_timezone) 	#UTC Time Zone
	Day_now = int(Moment_utc.strftime("%w"))							#day of the week 0-6
	return Day_now

#-------------------------------- Clock -----------------------------------------------
def clock(): 												#F Return time in second string
	global x, Local_timezone, Moment_utc, Moment, Time_now_str, Start_time_str, Stop_time_str
	x = datetime.datetime.utcnow()																#UTC time
	Local_timezone = tzlocal.get_localzone()													#Time Zone
	Moment_utc = x.replace(tzinfo=pytz.utc).astimezone(Local_timezone) 							#UTC Time Zone
	Moment = Moment_utc.strftime("%X")															#time now in hh:mm:ss
	Time_now_str = sum(x * int(t) for x, t in zip([3600, 60, 1], Moment.split(":")))			#string time now in seconds
	Start_time_str = sum(x * int(t) for x, t in zip([3600, 60, 1], Start_time.split(":")))		#string time start now in seconds
	Stop_time_str = sum(x * int(t) for x, t in zip([3600, 60, 1], Stop_time.split(":")))		#string time stop now in seconds
	return Time_now_str

#-------------------------------scheduler  ---------------------------------------------
def sch_start_time(): 									#Operating_T True/ False
	global Operating_T, Time_now_str, Start_time_str, Stop_time_str
	if Start_time <= Stop_time:
		clock()
		if Time_now_str >= Start_time_str and Time_now_str < Stop_time_str:
			Operating_T = True
		else:
			Operating_T = False
	elif Start_time > Stop_time:
		clock()
		if not Time_now_str > Start_time_str or Time_now_str < Stop_time_str:
			Operating_T = True
		else:
			Operating_T = False
	return Operating_T
def sch_start_day(): 									#Operating_D True/ False
	global Operating_D, Time_now_str, Start_day, Stop_day
	if Start_day <= Stop_day:
		today()
		if Day_now >= Start_day and Day_now <= Stop_day:
			Operating_D = True
		else:
			Operating_D = False
	elif Start_day > Stop_day:
		today()
		if not Day_now >= Start_day or Day_now <= Stop_day:
			if Day_now > Start_day:
				Operating_D = True
			else:
				Operating_D = False
	return Operating_D

#------------------------------ making folder ---------------------------------------------	
def create_pool():
	global x, Local_timezone, Moment_utc, Moment, Time_now_str
	Pool = "Local/" + time.strftime("%y%m_%d")			#Capture folder name, differnt settings better different folders
	try:
		os.path.exists(Pool)
	except:
		ptint("vec postoji")
		pass
	else:
		os.makedir(Pool)
		
#create_pool()
Check_T = True
Check_D = True
while True:
	Operating_T = sch_start_time()
	Operating_D = sch_start_day()
	if Operating_T == True and Operating_D == True:
		Check_T = True
		tl_script()
		#print("TiMELAPSE Working")
	elif Operating_T == False and Check_T == True:
		Check_T = False
		Chech_D = True
		if Time_now_str >= Start_time_str:
			print("Working day but time is over, come tomorrow")
		else:
			print("Timelapse will start at: " + Start_time)
	elif Operating_D == False and Check_T == False and Chech_D == True:
		Chech_T = False
		Chech_D = False
		print("Take a beer it's a free day!")
