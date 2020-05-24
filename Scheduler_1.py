import pytz
import tzlocal
import datetime
import time
import os
import sys
import schedule
from time import sleep
from picamera import PiCamera
from picam_preset_1 import *  #will import: pool, take_picture, camera_settings, start_day, stop_day, start_time, stop_time, interval
processing_time = (1 + camera.shutter_speed / 1000000)    #Time of executing the script, camera.shutter_speed is in micro secconds

#IMPORTANT camera script name: picam_preset_"X".py 
#1 -  2 min ISO 800, for automatic upload
#2 -  2 min ISO 100, WB auto, RAW
#3 -  5 min ISO 100, WB auto, bri 50, con -10

tl_0 = True
def tl_script():
    global tl_0
    print("schedule take picture - dry run")
    #take_picture() #uncomment 
    tl_0 = False
    return tl_0
	
done = True
def terminated(): 
    global done
    print("Done for today")
    done = False
    return done
	
x = datetime.datetime.utcnow()                                                          #UTC time 
day_now = x.strftime("%w")                                                              #day of the week 0-6
local_timezone = tzlocal.get_localzone()                                                #Time Zone 
moment_utc = x.replace(tzinfo=pytz.utc).astimezone(local_timezone)                      #UTC Time Zone
moment =(moment_utc.strftime("%X"))                                                     #time now in hh:mm:ss
tine_now_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], moment.split(":"))))      #string time now in seconds
start_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], start_time.split(":"))))     #string time start now in seconds
stop_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], stop_time.split(":"))))       #string time stop now in seconds
interval_int = int(sum(x * int(t) for x, t in zip([60, 1], interval.split(":"))))       #string interval in seconds
schedule.every(interval_int - processing_time).seconds.do(tl_script)                    #Schedule interval function

day_variable = False
def check_day():																		#Return True or False for the working day
    global x
    x = datetime.datetime.utcnow()														#UTC time 
    day_now = x.strftime("%w")															#day of the week 0-6
    if day_now >= start_day and day_now <= stop_day:
        global day_variable
        day_variable = True
    else:
        day_variable = False
        
time_variable = False
def check_time():																		#Return True or False for the working time
    global x
    x = datetime.datetime.utcnow()                                                     	#day of the week 0-6
    local_timezone = tzlocal.get_localzone()                                            #Time Zone 
    moment_utc = x.replace(tzinfo=pytz.utc).astimezone(local_timezone)			#UTC Time Zone
    moment =(moment_utc.strftime("%X"))							#time now in hh:mm:ss
    global tine_now_str
    tine_now_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], moment.split(":"))))  #print(tine_now_str)
    if tine_now_str >= start_str and tine_now_str <= stop_str:
        global time_variable
        time_variable = True
    else:
        time_variable = False

if not os.path.exists("Pool"):															#Create capture folder name if don't exist
    os.makedirs("Pool")

#Main loop
while True:
    check_day()
    check_time()
    if day_variable == True and time_variable == True:
        if tl_0 == True:
            tl_script()																	#Run schedule job immediately ones before schedule,
            print("1St time run. Working day and working time")
        schedule.run_pending()
        check_day()
        check_time()
    elif day_variable == True and time_variable == False:
        if done == True:
            terminated()						#workiong on	
		#print("Working day but time is over, come tomorrow")
        sleep(1)        
    elif day_variable == False and time_variable == False:
		done()							#workiong on
		print("Take a beer it's a free day!")
		sleep(3600)						#workiong on
		
		
