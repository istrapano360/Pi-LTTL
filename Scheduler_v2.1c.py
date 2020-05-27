import pytz
import tzlocal
import datetime
import time
import os
import sys
from time import sleep
from picamera import PiCamera
from picam_preset_12 import*  # don'know if will work 	will import: pool, take_picture, camera_settings, start_day, stop_day, start_time, stop_time, interval


#TL = 1 															#Time lapse script index 
#TL_preset = 'picam_preset_'TL		#?????????????????????????  don'know if will work

#IMPORTANT camera script name: picam_preset_"X".py
#1 - 30 sec day, for automatic upload
#2 -  2 min ISO 100, WB auto, RAW
#3 -  5 min ISO 100, WB auto, bri 50, con -10

Processing_time = int(1 + camera.shutter_speed / 1000000)			#Time of executing the script, camera.shutter_speed is in micro secconds

def tl_script():
	#take_picture()
	print("svakih 5 sekundi")

x = datetime.datetime.utcnow()									#UTC time
Day_now = Moment_utc.strftime("%w")									#day of the week 0-6
Local_timezone = tzlocal.get_localzone()							#Time Zone
Moment_utc = x.replace(tzinfo=pytz.utc).astimezone(Local_timezone) 				#UTC Time Zone
Moment =(Moment_utc.strftime("%X"))								#time now in hh:mm:ss
Time_now_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], Moment.split(":"))))		#string time now in seconds
Start_time_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], Start_time.split(":"))))		#string time start now in seconds
Stop_time_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], Stop_time.split(":"))))		#string time stop now in seconds
Interval_int = int(sum(x * int(t) for x, t in zip([60, 1], Interval.split(":"))))		#string interval in seconds
	
def interval ():
	sleep(Interval_int - Processing_time) ## -time check time				##Schedule interval function

#--------------------------------- Day -------------------------------------------------
def today():											#F Return today day int
	global Day_now
	x = datetime.datetime.utcnow()									#UTC time
	Day_now = Moment_utc.strftime("%w")									#day of the week 0-6
	Local_timezone = tzlocal.get_localzone()							#Time Zone
	Moment_utc = x.replace(tzinfo=pytz.utc).astimezone(Local_timezone) 				#UTC Time Zone
	return Day_now
	print("today is today")

#-------------------------------- Clock -----------------------------------------------
def clock(): 											#F Return time in second string
	global Time_now_str
	x = datetime.datetime.utcnow()									#UTC time
	Local_timezone = tzlocal.get_localzone()							#Time Zone
	Moment_utc = x.replace(tzinfo=pytz.utc).astimezone(Local_timezone) 				#UTC Time Zone
	Moment =(Moment_utc.strftime("%X"))								#time now in hh:mm:ss
	Time_now_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], Moment.split(":"))))		#string time now in seconds
	Start_time_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], Start_time.split(":"))))		#string time start now in seconds
	Stop_time_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], Stop_time.split(":"))))		#string time stop now in seconds

	return Time_now_str
	print("now is current time ")

#-------------------------------- Timer ------------------------------------------------
def sch_time():											#V Operating_T True/ False
	global Operating_T, Time_now_str, Start_time_str, Stop_time_str
	if Start_time <= Stop_time:
		clock()
		#print(now)
		#sleep(1)
		if Time_now_str >= Start_time_str and Time_now_str <= Stop_time_str:
			if Time_now_str == Start_time_str:
				Operating_T = True
				#print("start time")
				#print("------")
			elif Time_now_str == Stop_time_str:
				Operating_T = False
				#print("stop time")
				#print("------")
			pass
	else:
		if not Time_now_str > Start_time_str or Time_now_str < Stop_time_str:
			Time_now_str
			#print(now)
			#sleep(1)
			if Time_now_str == Start_time_str:
				Operating_T = True
				#print("start time")
			elif Time_now_str == Stop_time_str:
				#print("stop time")
				Operating_T = False
			pass
	return Operating_T

#----------------------------- Day counter ---------------------------------------------
def sch_day():											#V Operating_D True/ False
	global Operating_D, Day_now, Start_day, Stop_day
	if Start_day <= Stop_day:
        	today()
       		#print(today)
		#sleep(2.4)
		if Day_now >= Start_day and Day_now <= Stop_day:
			if Day_now == Start_day:
				Operating_D = True
				#print("start day")
				#print("------")
			elif Day_now == Stop_day:
				Operating_D = False
				#print("stop day")
				#print("------")		
	else:
		if not Day_now > Start_day or Day_now < Stop_day:
			today()
			#print(today)
			#sleep(2.4)
			if Day_now == Start_day:
				Operating_D = True
				#print("start day")
			elif Day_now == Stop_day:
				#print("stop day")
				Operating_D = False
	return Operating_D

#----------------------------- 1st run scheduler  ----------------------------------------
def sch_start_time():
	global Operating_T, Operating_D, Time_now_str, Start_time_str, Stop_time_str, Start_day, Stop_day
	if Start_time <= Stop_time:
		clock()
		if Time_now_str >= Start_time_str and Time_now_str <= Stop_time_str:
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
	
def sch_start_day():	
	if Start_day <= Stop_day:
        today()
		if Day_now >= Start_day and Day_now <= Stop_day:
			Operating_D = True
		else:
			Operating_D = False			
	elif Start_day > Stop_day:
		today()
		if not Day_now > Start_day or Day_now < Stop_day:
			if Day_now > Start_day:
				Operating_D = True
			else:
				Operating_D = False
	return Operating_D





try:
	os.path.exists(Pool)
except:
	print("Good, folder allredy created")
else:
	os.makedirs(Pool)

Check = True
Operating_D = sch_start_day()
Operating_T = sch_start_time()
while True:
	sch_day()
	sch_time()
	if Operating_D == True and Operating_T == True:
		Chech = True
		tl_script()
		interval()
		sch_day()
		sch_time()
	elif Operating_T == False and Check == True:
		Check = False
		#return Check
		print("Working day but time is over, come tomorrow")
	elif Operating_D == False and Check == True:
		Chech = False
		print("Take a beer it's a free day!")
		#return Check
